from django.contrib import admin
from .models import MenuItem
from typing import List, Tuple


class MenuItemAdmin(admin.ModelAdmin):
    """Админ-панель для управления пунктами меню"""

    # Поля для отображения в списке
    list_display: Tuple[str, ...] = ('name', 'menu_name', 'parent', 'order')

    # Фильтры в правой панели
    list_filter: Tuple[str, ...] = ('menu_name',)

    # Поля для поиска
    search_fields: Tuple[str, ...] = ('name', 'menu_name')

    # Поля в форме редактирования
    fields: Tuple[str, ...] = ('name', 'menu_name', 'parent', 'order', 'named_url', 'explicit_url')


admin.site.register(MenuItem, MenuItemAdmin)
