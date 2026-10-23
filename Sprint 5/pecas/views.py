from django.shortcuts import get_object_or_404, render

from .models import Peca


def lista_pecas(request):
    """Vitrine: lê as peças do banco e permite filtrar por faixa de severidade (?faixa=leve)."""
    faixa = request.GET.get("faixa", "")
    if faixa not in dict(Peca.FAIXA_CHOICES):
        faixa = ""  # valor desconhecido: mostra todas as peças

    pecas = Peca.objects.select_related("vendedor").com_faixa(faixa)
    contexto = {
        "pecas": pecas,
        "faixa_ativa": faixa,
        "faixas": Peca.FAIXA_CHOICES,
    }
    return render(request, "pecas/lista.html", contexto)


def produto(request, pk):
    """Página do produto: busca uma peça no banco pelo id (404 se não existir)."""
    peca = get_object_or_404(Peca.objects.select_related("vendedor"), pk=pk)
    return render(request, "pecas/produto.html", {"peca": peca})
