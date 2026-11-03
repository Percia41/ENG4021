from decimal import Decimal
from itertools import product as combinacoes

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Defeito, Favorite, Product, ProductImage, UserProfile


def criar_peca(nome, tipo=1, localizacao=1, extensao=1, **campos):
    campos.setdefault('price', Decimal('80'))
    peca = Product.objects.create(name=nome, description='Fio puxado na barra', **campos)
    Defeito.objects.create(product=peca, tipo=tipo, localizacao=localizacao, extensao=extensao)
    return peca


class FiltroSeveridadeTests(TestCase):
    def setUp(self):
        self.leve = criar_peca('Camisa leve', 1, 1, 1)            # 1,00
        self.moderada = criar_peca('Calça moderada', 2, 2, 2)     # 2,00
        self.alta = criar_peca('Vestido alto', 3, 3, 3)           # 3,00
        self.sem_defeito = Product.objects.create(name='Saia sem ficha', description='x', price=Decimal('50'))

    def nomes(self, faixa=None):
        url = reverse('home') + (f'?faixa={faixa}' if faixa else '')
        return {p.name for p in self.client.get(url).context['products']}

    def test_sem_filtro_mostra_todas_as_pecas_ativas(self):
        self.assertEqual(self.nomes(), {'Camisa leve', 'Calça moderada', 'Vestido alto', 'Saia sem ficha'})

    def test_cada_faixa_mostra_so_as_suas_pecas(self):
        self.assertEqual(self.nomes('leve'), {'Camisa leve'})
        self.assertEqual(self.nomes('moderada'), {'Calça moderada'})
        self.assertEqual(self.nomes('alta'), {'Vestido alto'})

    def test_faixa_desconhecida_mostra_todas(self):
        self.assertEqual(len(self.nomes('qualquer')), 4)

    def test_filtro_no_banco_concorda_com_o_model_em_todas_as_27_notas(self):
        Product.objects.all().delete()
        for tipo, local, extensao in combinacoes((1, 2, 3), repeat=3):
            criar_peca(f'{tipo}{local}{extensao}', tipo, local, extensao)
        for faixa in ('leve', 'moderada', 'alta'):
            filtradas = Product.objects.with_severity_band(faixa)
            self.assertTrue(filtradas.exists())
            for peca in filtradas:
                self.assertEqual(peca.severity_band, faixa)
        self.assertEqual(sum(Product.objects.with_severity_band(f).count() for f in ('leve', 'moderada', 'alta')), 27)

    def test_limites_entram_na_faixa_de_baixo(self):
        Product.objects.all().delete()
        limite_leve = criar_peca('1,70', 1, 3, 1)       # 0,45 + 1,05 + 0,20 = 1,70 → leve
        logo_acima = criar_peca('1,75', 1, 2, 3)        # 0,45 + 0,70 + 0,60 = 1,75 → moderada
        limite_moderada = criar_peca('2,30', 3, 1, 3)   # 1,35 + 0,35 + 0,60 = 2,30 → moderada
        acima = criar_peca('2,45', 3, 2, 2)             # 1,35 + 0,70 + 0,40 = 2,45 → alta
        self.assertQuerySetEqual(Product.objects.with_severity_band('leve'), [limite_leve])
        self.assertCountEqual(Product.objects.with_severity_band('moderada'), [logo_acima, limite_moderada])
        self.assertQuerySetEqual(Product.objects.with_severity_band('alta'), [acima])

    def test_faixa_vazia_tem_mensagem_e_link_para_todas(self):
        self.alta.delete()
        response = self.client.get(reverse('home') + '?faixa=alta')
        self.assertContains(response, 'Nenhuma peça nessa faixa')
        self.assertContains(response, f'href="{reverse("home")}"')

    def test_chip_ativo_e_card_com_selo_e_link_para_a_peca(self):
        response = self.client.get(reverse('home') + '?faixa=moderada')
        self.assertContains(response, 'aria-current="true"><span class="severity-dot severity-dot--moderada">')
        self.assertContains(response, 'severity-badge--moderada')
        self.assertContains(response, reverse('product_detail', args=[self.moderada.pk]))


class PaginaProdutoTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.vendedor = User.objects.create_user('loja@example.com', password='Strong-test-524!')
        UserProfile.objects.create(user=self.vendedor, role=UserProfile.Role.BRAND,
                                   store_name='Ateliê Linha', location='Rio de Janeiro, RJ')
        self.comprador = User.objects.create_user('ana@example.com', password='Strong-test-524!')
        self.peca = criar_peca('Calça de linho', 2, 2, 2, price=Decimal('130'), original_price=Decimal('200'),
                               seller=self.vendedor, brand='Ateliê Linha', size='38', condition='Nova com defeito',
                               defect_measure_cm=Decimal('4'), visible_when_worn=True)
        ProductImage.objects.create(product=self.peca, image_path='core/images/demo-piece.svg', alt_text='Peça inteira')
        ProductImage.objects.create(product=self.peca, image_path='core/images/demo-defect.svg',
                                    alt_text='Close da mancha', is_defect=True)
        self.url = reverse('product_detail', args=[self.peca.pk])

    def test_mostra_ficha_do_defeito_preco_e_vendedor(self):
        response = self.client.get(self.url)
        for texto in ['Calça de linho', 'Severidade 2,00 · Moderada', 'Reparável', 'Funcional reparável',
                      'Semivisível', 'Média', '4,0 cm medidos', 'O defeito aparece quando',
                      'R$ 200,00', 'R$ 130,00', '35% off', 'Tamanho', '38', 'Ateliê Linha',
                      'Rio de Janeiro, RJ', 'Close do defeito', 'alt="Close da mancha"']:
            self.assertContains(response, texto)

    def test_defeito_nao_reparavel_nao_mostra_selo(self):
        self.peca.defeito.tipo = 3
        self.peca.defeito.save()
        self.assertNotContains(self.client.get(self.url), 'repair-badge')

    def test_peca_sem_fotos_nem_defeito_ainda_abre(self):
        peca = Product.objects.create(name='Blusa simples', description='Botão solto', price=Decimal('40'))
        response = self.client.get(reverse('product_detail', args=[peca.pk]))
        self.assertContains(response, 'Sem fotos desta peça ainda')
        self.assertNotContains(response, 'severity-badge')
        self.assertNotContains(response, '% off')

    def test_peca_inativa_ou_inexistente_da_404(self):
        self.peca.is_active = False
        self.peca.save()
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.assertEqual(self.client.get(reverse('product_detail', args=[9999])).status_code, 404)

    def test_visitante_ve_convite_para_entrar(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Entrar para comprar')
        self.assertNotContains(response, reverse('cart_add', args=[self.peca.pk]))

    def test_comprador_adiciona_ao_carrinho_e_favorita_voltando_para_a_peca(self):
        self.client.force_login(self.comprador)
        self.assertContains(self.client.get(self.url), reverse('cart_add', args=[self.peca.pk]))
        response = self.client.post(reverse('favorite_add', args=[self.peca.pk]), {'next': self.url})
        self.assertRedirects(response, self.url)
        self.assertTrue(Favorite.objects.filter(user=self.comprador, product=self.peca).exists())
        self.assertContains(self.client.get(self.url), 'Favoritada')

    def test_peca_esgotada_nao_oferece_carrinho(self):
        self.peca.stock = 0
        self.peca.save()
        self.client.force_login(self.comprador)
        response = self.client.get(self.url)
        self.assertContains(response, 'Peça esgotada')
        self.assertNotContains(response, reverse('cart_add', args=[self.peca.pk]))
