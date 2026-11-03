"""Quem pode fazer o quê. Usado pelas views (decorators) e pelos templates (context processor)."""
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import UserProfile


def has_role(user, *roles):
    """A equipe (staff) passa em qualquer verificação, para facilitar os testes manuais."""
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    profile = getattr(user, 'profile', None)
    return profile is not None and profile.role in roles


def is_buyer(user):
    return has_role(user, UserProfile.Role.BUYER)


def is_seller(user):
    return has_role(user, UserProfile.Role.SELLER, UserProfile.Role.BRAND)


def role_required(check, message):
    def decorator(view):
        @login_required
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if not check(request.user):
                raise PermissionDenied(message)
            return view(request, *args, **kwargs)
        return wrapped
    return decorator


buyer_required = role_required(is_buyer, 'Esta área é exclusiva para contas de comprador.')
seller_required = role_required(is_seller, 'Esta área é exclusiva para vendedores e marcas.')
