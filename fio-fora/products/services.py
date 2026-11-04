"""Validação e preparo das fotos enviadas pelo vendedor.

Fica fora do forms.py porque a mesma regra vale para o formulário, para o
admin e para os testes.

A checagem abre a imagem com o Pillow em vez de olhar a extensão do arquivo:
a extensão e o content-type são escritos pelo navegador e qualquer um troca.
"""
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageOps, UnidentifiedImageError

FORMATS = {'JPEG': 'jpg', 'PNG': 'png', 'WEBP': 'webp'}
FORMAT_NAMES = 'JPG, PNG ou WebP'

MAX_BYTES = 5 * 1024 * 1024
MIN_SIDE = 600
MAX_SIDE = 2000
QUALITY = 85

MAX_PHOTOS = 6


def validate_image(upload, label='A imagem'):
    """Valida um arquivo enviado e devolve a versão que vai para o disco.

    As mensagens falam com o vendedor, não com o programador: quem cadastra
    uma peça não sabe o que é EXIF.
    """
    if upload.size > MAX_BYTES:
        raise ValidationError(
            f'{label} tem {upload.size / (1024 * 1024):.1f} MB. '
            f'O limite é {MAX_BYTES // (1024 * 1024)} MB.'
        )

    try:
        image = Image.open(upload)
        image.verify()  # pega arquivo truncado ou que não é imagem
        upload.seek(0)
        image = Image.open(upload)
    except (UnidentifiedImageError, OSError):
        raise ValidationError(f'{label} não pôde ser lida. Envie um arquivo {FORMAT_NAMES}.')

    if image.format not in FORMATS:
        raise ValidationError(
            f'{label} está em {image.format or "formato desconhecido"}. Use {FORMAT_NAMES}.'
        )

    if min(image.size) < MIN_SIDE:
        raise ValidationError(
            f'{label} tem {image.width}×{image.height} px. O menor lado precisa ter '
            f'pelo menos {MIN_SIDE} px, senão o defeito não aparece no zoom.'
        )

    return _prepare(image, upload.name)


def validate_images(uploads, label='As fotos'):
    """Valida a lista de fotos da peça e devolve todas prontas.

    Junta os erros em vez de parar no primeiro: quem mandou seis fotos quer
    saber quais deram problema de uma vez só.
    """
    uploads = list(uploads)
    if len(uploads) > MAX_PHOTOS:
        raise ValidationError(f'{label}: são {len(uploads)} arquivos e o limite é {MAX_PHOTOS}.')

    prepared, errors = [], []
    for position, upload in enumerate(uploads, start=1):
        try:
            prepared.append(validate_image(upload, f'A foto {position}'))
        except ValidationError as error:
            errors.extend(error.messages)
    if errors:
        raise ValidationError(errors)
    return prepared


def _prepare(image, name):
    """Gira pelo EXIF, reduz se for grande demais e descarta os metadados.

    Girar importa porque foto de celular vem deitada e o defeito apareceria de
    lado. Descartar metadados importa porque foto de celular carrega a
    coordenada de GPS de onde foi tirada, que costuma ser a casa do vendedor.
    """
    image = ImageOps.exif_transpose(image)
    image_format = image.format or 'JPEG'

    if max(image.size) > MAX_SIDE:
        image.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
    if image_format == 'JPEG' and image.mode not in ('RGB', 'L'):
        image = image.convert('RGB')

    # Copiar os pixels para uma imagem nova deixa os metadados para trás.
    clean = Image.new(image.mode, image.size)
    clean.putdata(list(image.getdata()))

    buffer = BytesIO()
    if image_format == 'JPEG':
        clean.save(buffer, 'JPEG', quality=QUALITY, optimize=True)
    elif image_format == 'PNG':
        clean.save(buffer, 'PNG', optimize=True)
    else:
        clean.save(buffer, 'WEBP', quality=QUALITY)
    size = buffer.tell()
    buffer.seek(0)

    base = name.rsplit('.', 1)[0][:40] or 'foto'
    return InMemoryUploadedFile(
        buffer, 'image', f'{base}.{FORMATS[image_format]}',
        f'image/{FORMATS[image_format]}', size, None,
    )
