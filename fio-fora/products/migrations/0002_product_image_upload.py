"""A foto do produto deixa de ser um caminho fixo e passa a ser um arquivo enviado.

As fotos antigas eram ilustrações estáticas (demo-piece.svg) apontadas por um
texto. Elas não existem como arquivo enviado, então as linhas antigas são
apagadas aqui; o popular_banco recria as de demonstração.
"""
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import products.models


def remover_fotos_antigas(apps, schema_editor):
    apps.get_model("products", "ProductImage").objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(remover_fotos_antigas, migrations.RunPython.noop),
        migrations.RemoveConstraint(
            model_name="productimage",
            name="unique_product_image",
        ),
        migrations.RemoveField(
            model_name="productimage",
            name="image_path",
        ),
        migrations.AddField(
            model_name="productimage",
            name="image",
            field=models.ImageField(
                default="",
                upload_to=products.models.product_image_path,
                verbose_name="foto",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="productimage",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="enviada em",
            ),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name="productimage",
            options={
                "ordering": ["-is_defect", "id"],
                "verbose_name": "foto de produto",
                "verbose_name_plural": "fotos de produtos",
            },
        ),
        migrations.AddConstraint(
            model_name="productimage",
            constraint=models.UniqueConstraint(
                fields=("product", "image"), name="unique_product_image"
            ),
        ),
    ]
