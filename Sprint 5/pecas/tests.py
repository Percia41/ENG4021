from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Peca, Vendedor


def criar_peca(**extra):
    vendedor = extra.pop("vendedor", None) or Vendedor.objects.create(
        nome="Aroma Studio", nota=Decimal("4.3"), total_avaliacoes=28
    )
    dados = dict(
        vendedor=vendedor,
        nome="Camisa de linho listrada",
        tamanho="M",
        tecido="100% linho",
        cor="areia",
        preco_original=Decimal("189.90"),
        tipo_defeito=1,
        localizacao_defeito=1,
        extensao_defeito=1,
        local_detalhe="forro interno",
        medida_cm=Decimal("1.5"),
        descricao_defeito="Mancha pequena na barra interna.",
    )
    dados.update(extra)
    return Peca.objects.create(**dados)


class CalculoDaPecaTests(TestCase):
    def test_defeito_leve_tem_15_por_cento(self):
        peca = criar_peca()
        self.assertEqual(peca.severidade, Decimal("1.00"))
        self.assertEqual(peca.faixa, "leve")
        self.assertEqual(peca.desconto_percentual, 15)
        self.assertEqual(peca.preco_final, Decimal("161.42"))

    def test_defeito_alto_tem_50_por_cento(self):
        peca = criar_peca(tipo_defeito=3, localizacao_defeito=3, extensao_defeito=3)
        self.assertEqual(peca.severidade, Decimal("3.00"))
        self.assertEqual(peca.faixa, "alta")
        self.assertEqual(peca.desconto_percentual, 50)

    def test_defeito_moderado(self):
        peca = criar_peca(tipo_defeito=2, localizacao_defeito=2, extensao_defeito=2)
        self.assertEqual(peca.severidade, Decimal("2.00"))
        self.assertEqual(peca.faixa, "moderada")
        self.assertEqual(peca.desconto_percentual, 35)  # 32,5% arredonda para 35%


class ViewsTests(TestCase):
    def test_lista_le_pecas_do_banco(self):
        criar_peca(nome="Peça do banco A")
        response = self.client.get(reverse("pecas:lista"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pecas/lista.html")
        self.assertContains(response, "Peça do banco A")

    def test_lista_vazia_mostra_aviso(self):
        response = self.client.get(reverse("pecas:lista"))
        self.assertContains(response, "Nenhuma peça cadastrada")

    def test_produto_mostra_dados_da_peca(self):
        peca = criar_peca()
        response = self.client.get(reverse("pecas:produto", args=[peca.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pecas/produto.html")
        self.assertContains(response, "Camisa de linho listrada")
        self.assertContains(response, "Aroma Studio")
        self.assertContains(response, "15% off")
        self.assertContains(response, "R$ 161,42")
        self.assertContains(response, "Severidade 1,00")

    def test_produto_inexistente_retorna_404(self):
        response = self.client.get(reverse("pecas:produto", args=[999]))
        self.assertEqual(response.status_code, 404)


class FiltroSeveridadeTests(TestCase):
    def setUp(self):
        self.leve = criar_peca(nome="Peça Leve")  # severidade 1,00
        self.moderada = criar_peca(  # 2,00
            nome="Peça Moderada", tipo_defeito=2, localizacao_defeito=2, extensao_defeito=2
        )
        self.alta = criar_peca(  # 3,00
            nome="Peça Alta", tipo_defeito=3, localizacao_defeito=3, extensao_defeito=3
        )

    def nomes(self, faixa=None):
        url = reverse("pecas:lista")
        response = self.client.get(url, {"faixa": faixa} if faixa is not None else {})
        self.assertEqual(response.status_code, 200)
        return {p.nome for p in response.context["pecas"]}

    def test_sem_filtro_mostra_todas(self):
        self.assertEqual(self.nomes(), {"Peça Leve", "Peça Moderada", "Peça Alta"})

    def test_filtra_cada_faixa(self):
        self.assertEqual(self.nomes("leve"), {"Peça Leve"})
        self.assertEqual(self.nomes("moderada"), {"Peça Moderada"})
        self.assertEqual(self.nomes("alta"), {"Peça Alta"})

    def test_faixa_invalida_mostra_todas(self):
        self.assertEqual(self.nomes("qualquer"), {"Peça Leve", "Peça Moderada", "Peça Alta"})

    def test_limites_exatos_das_faixas(self):
        limite_leve = criar_peca(  # 1,70 -> Leve
            nome="Limite Leve", tipo_defeito=1, localizacao_defeito=3, extensao_defeito=1
        )
        limite_moderada = criar_peca(  # 2,30 -> Moderada
            nome="Limite Moderada", tipo_defeito=3, localizacao_defeito=1, extensao_defeito=3
        )
        self.assertEqual(limite_leve.severidade, Decimal("1.70"))
        self.assertEqual(limite_moderada.severidade, Decimal("2.30"))
        self.assertIn("Limite Leve", self.nomes("leve"))
        self.assertIn("Limite Moderada", self.nomes("moderada"))
        self.assertNotIn("Limite Moderada", self.nomes("alta"))

    def test_filtro_do_banco_bate_com_a_faixa_do_modelo(self):
        for t in (1, 2, 3):
            for loc in (1, 2, 3):
                for ext in (1, 2, 3):
                    criar_peca(tipo_defeito=t, localizacao_defeito=loc, extensao_defeito=ext)
        for faixa in ("leve", "moderada", "alta"):
            do_banco = {p.pk for p in Peca.objects.com_faixa(faixa)}
            esperado = {p.pk for p in Peca.objects.all() if p.faixa == faixa}
            self.assertEqual(do_banco, esperado, faixa)

    def test_faixa_sem_pecas_mostra_aviso(self):
        Peca.objects.filter(pk=self.alta.pk).delete()
        response = self.client.get(reverse("pecas:lista"), {"faixa": "alta"})
        self.assertContains(response, "Nenhuma peça nessa faixa")

    def test_filtro_aparece_na_vitrine_com_faixa_ativa(self):
        response = self.client.get(reverse("pecas:lista"), {"faixa": "moderada"})
        self.assertContains(response, 'href="?faixa=leve"')
        self.assertContains(response, 'class="chip moderada active"')
