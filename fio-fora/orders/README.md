# orders — checkout e pedidos

Finalização da compra (simulada) e histórico de pedidos.

[← Voltar para a documentação principal](../README.md)

## Páginas

| URL | Página |
|---|---|
| `/checkout/` | Revisar o carrinho e confirmar o pedido |
| `/pedidos/` | Histórico de pedidos do comprador |
| `/pedidos/<id>/` | Detalhe de um pedido |

Todas as páginas são só para compradores.

> **[PRINT]** Tela de checkout com o resumo do pedido.

## Models

- **`Order`**: pedido, com código de referência e status (pendente, pago,
    enviado, cancelado).
- **`OrderItem`**: item do pedido, com uma **cópia** do nome e do preço da peça
    no momento da compra.

## Regras

- A compra é demonstrativa: não há pagamento nem entrega.
- Ao confirmar, o estoque é conferido de novo e descontado, tudo de uma vez
    (se um item falhar, nada é gravado).
- O carrinho é esvaziado depois do pedido.
- O histórico não muda se a peça for alterada ou apagada depois.

## Arquivos principais

| Arquivo | O que tem |
|---|---|
| `services.py` | `checkout_cart()`: cria o pedido e desconta o estoque |
| `views.py` | Checkout, lista e detalhe dos pedidos |

> **[PRINT]** Página de detalhe de um pedido confirmado.
