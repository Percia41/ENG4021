from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin de usuários, usado também para gerenciar marcas/lojas (role=brand)."""

    list_display = ["user", "role", "store_name", "legal_name", "location", "phone"]
    list_filter = ["role", "segment"]
    search_fields = ["user__username", "user__email", "store_name", "legal_name", "document"]
    list_select_related = ["user"]
