# products — catálogo e área do vendedor

Vitrine, página da peça, cadastro de peças pelo vendedor e simulador de desconto.

[← Voltar para a documentação principal](../README.md)

## Páginas

| URL | Página | Quem acessa |
|---|---|---|
| `/vitrine/` | Vitrine, com filtro `?faixa=leve`, `moderada` ou `alta` | Todos |
| `/produtos/<id>/` | Página da peça | Todos |
| `/simulador/` | Simulador de desconto | Todos |
| `/minhas-pecas/` | Peças do vendedor logado | Vendedor e marca |
| `/produtos/novo/` | Cadastrar peça | Vendedor e marca |
| `/produtos/<id>/editar/` | Editar peça | Dono da peça |
| `/produtos/<id>/remover/` | Remover peça | Dono da peça |

> **[PRINT]** Vitrine com o filtro "Moderada" ativo.

> **[PRINT]** Página de uma peça, mostrando a ficha do defeito, o preço riscado e o % de desconto.

## Models

| Model | Guarda |
|---|---|
| `Product` | Peça: nome, descrição, preço original, preço final, estoque, vendedor, categoria |
| `Defeito` | Tipo, localização e extensão do defeito (de 1 a 3 cada), ligado 1-para-1 à peça |
| `Category` | Categoria da peça |
| `ProductImage` | Uma foto enviada da peça e se ela mostra o defeito |

## Severidade e desconto

Tudo é calculado em `models.py`, numa fórmula única:

```text
Severidade = 0,45 × Tipo + 0,35 × Localização + 0,20 × Extensão
```

| Faixa | Severidade |
|---|---|
| Leve | até 1,70 |
| Moderada | até 2,30 |
| Alta | acima de 2,30 |

O desconto vai de 15% (severidade 1) a 50% (severidade 3), arredondado de 5 em
5. O preço final é sempre calculado; o vendedor informa só o preço original.

## Arquivos principais

| Arquivo | O que tem |
|---|---|
| `models.py` | Models, fórmula de severidade e o filtro `Product.objects.with_severity_band()` |
| `forms.py` | `ProductForm` (cadastrar e editar) e `DiscountSimulationForm` |
| `views.py` | Vitrine, página da peça, simulador e área do vendedor |
| `templates/products/includes/card_info.html` | Informações comuns aos cards de peça |
| `templates/products/includes/price.html` | Preço original, preço final e % de desconto |
| `management/commands/popular_banco.py` | Cria usuários, peças, carrinho e pedido de exemplo |

> **[PRINT]** Tela "Minhas peças" com os botões Editar e Remover.

> **[PRINT]** Simulador de desconto com um resultado calculado.

## Fotos da peça

As fotos são arquivos enviados pelo vendedor (`ImageField`), guardados em
`MEDIA_ROOT/products/<id da peça>/` com nome sorteado. O nome do arquivo
original não entra no caminho para não vazar informação do vendedor.

A **foto do defeito é obrigatória**: sem ela o cadastro não é aceito. Na
galeria e nas miniaturas ela aparece primeiro, porque é a imagem que explica o
desconto. Peça sem foto da peça continua aparecendo, com um espaço no lugar da
capa.

Antes de salvar, `services.py` confere cada arquivo abrindo a imagem com o
Pillow (e não pela extensão, que o navegador escreve):

| Regra | Valor |
|---|---|
| Formatos aceitos | JPG, PNG, WebP |
| Tamanho máximo | 5 MB por arquivo |
| Lado menor | pelo menos 600 px |
| Fotos da peça | até 6, além da foto do defeito |

A imagem aprovada é girada pelo EXIF, reduzida a 2000 px no maior lado e tem
os metadados descartados — foto de celular carrega a coordenada de GPS de onde
foi tirada.

> **[PRINT]** Formulário de cadastro com os campos de foto da peça e foto do defeito.

> **[PRINT]** Galeria da página da peça, com a foto do defeito em destaque.
