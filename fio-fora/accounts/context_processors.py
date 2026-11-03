from .decorators import is_buyer, is_seller


def roles(request):
    """Disponibiliza is_buyer e is_seller em todos os templates."""
    return {'is_buyer': is_buyer(request.user), 'is_seller': is_seller(request.user)}
