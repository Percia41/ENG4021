from decimal import ROUND_HALF_UP, Decimal

from django.db import models
from django.db.models import ExpressionWrapper, F, IntegerField


class PecaQuerySet(models.QuerySet):
    def com_faixa(self, faixa):
        """Filtra no banco pela faixa de severidade ("leve", "moderada" ou "alta").

        Usa a mesma fórmula e os mesmos limites de `Peca.severidade` e `Peca.faixa`,
        em centésimos (inteiros), para não haver erro de arredondamento.
        """
        peca = self.model
        centesimos = ExpressionWrapper(
            F("tipo_defeito") * int(peca.PESO_TIPO * 100)
            + F("localizacao_defeito") * int(peca.PESO_LOCAL * 100)
            + F("extensao_defeito") * int(peca.PESO_EXTENSAO * 100),
            output_field=IntegerField(),
        )
        qs = self.annotate(severidade_centesimos=centesimos)
        limite_leve = int(peca.LIMITE_LEVE * 100)
        limite_moderada = int(peca.LIMITE_MODERADA * 100)
        if faixa == "leve":
            return qs.filter(severidade_centesimos__lte=limite_leve)
        if faixa == "moderada":
            return qs.filter(
                severidade_centesimos__gt=limite_leve,
                severidade_centesimos__lte=limite_moderada,
            )
        if faixa == "alta":
            return qs.filter(severidade_centesimos__gt=limite_moderada)
        return self


class Vendedor(models.Model):
    """Marca ou loja verificada. No FioFora não existe vendedor pessoa física anônima."""

    nome = models.CharField(max_length=100)
    nota = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal("0.0"))
    total_avaliacoes = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "vendedores"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    @property
    def estrelas(self):
        cheias = int(self.nota.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        return "★" * cheias + "☆" * (5 - cheias)


class Peca(models.Model):
    """Peça com defeito à venda. A severidade e o desconto são calculados, nunca digitados."""

    TIPO_CHOICES = [
        (1, "Estético"),
        (2, "Funcional reparável"),
        (3, "Funcional não reparável"),
    ]
    LOCALIZACAO_CHOICES = [
        (1, "Escondido"),
        (2, "Semivisível"),
        (3, "Visível"),
    ]
    EXTENSAO_CHOICES = [
        (1, "Pequena"),
        (2, "Média"),
        (3, "Grande"),
    ]

    # Pesos da fórmula oficial: S = 0,45 x Tipo + 0,35 x Local + 0,20 x Extensão
    PESO_TIPO = Decimal("0.45")
    PESO_LOCAL = Decimal("0.35")
    PESO_EXTENSAO = Decimal("0.20")

    # Faixas: Leve até 1,70 · Moderada até 2,30 · Alta acima de 2,30
    LIMITE_LEVE = Decimal("1.70")
    LIMITE_MODERADA = Decimal("2.30")
    FAIXA_CHOICES = [
        ("leve", "Leve"),
        ("moderada", "Moderada"),
        ("alta", "Alta"),
    ]

    objects = PecaQuerySet.as_manager()

    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name="pecas")
    nome = models.CharField(max_length=150)
    tamanho = models.CharField(max_length=10)
    tecido = models.CharField(max_length=80)
    cor = models.CharField(max_length=40)
    preco_original = models.DecimalField(max_digits=8, decimal_places=2)

    tipo_defeito = models.PositiveSmallIntegerField(choices=TIPO_CHOICES)
    localizacao_defeito = models.PositiveSmallIntegerField(choices=LOCALIZACAO_CHOICES)
    extensao_defeito = models.PositiveSmallIntegerField(choices=EXTENSAO_CHOICES)
    local_detalhe = models.CharField("onde fica o defeito", max_length=80, blank=True)
    medida_cm = models.DecimalField("medida do defeito (cm)", max_digits=5, decimal_places=1)
    descricao_defeito = models.TextField()
    aparece_vestida = models.BooleanField("defeito aparece com a peça vestida", default=False)
    reparavel = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.nome} ({self.vendedor})"

    @property
    def severidade(self):
        s = (
            self.PESO_TIPO * self.tipo_defeito
            + self.PESO_LOCAL * self.localizacao_defeito
            + self.PESO_EXTENSAO * self.extensao_defeito
        )
        return s.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def faixa(self):
        s = self.severidade
        if s <= self.LIMITE_LEVE:
            return "leve"
        if s <= self.LIMITE_MODERADA:
            return "moderada"
        return "alta"

    @property
    def faixa_label(self):
        return self.faixa.capitalize()

    @property
    def desconto_percentual(self):
        """Interpola de 15% (severidade 1) a 50% (severidade 3) e arredonda de 5 em 5."""
        bruto = Decimal("15") + (self.severidade - 1) / Decimal("2") * Decimal("35")
        return int((bruto / 5).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * 5)

    @property
    def preco_final(self):
        fator = Decimal(100 - self.desconto_percentual) / Decimal(100)
        return (self.preco_original * fator).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
