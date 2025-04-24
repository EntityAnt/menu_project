from django import template
from django.urls import reverse, resolve, NoReverseMatch
from django.http import HttpRequest
from typing import Dict, List, Optional, Any
from ..models import MenuItem

register = template.Library()


@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context: Dict[str, Any], menu_name: str) -> Dict[str, Any]:
    """
    Тег для отрисовки древовидного меню.

    Args:
        context: Контекст шаблона Django
        menu_name: Имя меню для отрисовки

    Returns:
        Словарь с данными для рендеринга меню
    """
    request: HttpRequest = context['request']
    current_url: str = request.path_info

    # Пытаемся определить именованный URL текущей страницы
    try:
        resolved_url = resolve(current_url)
        resolved_url_name: Optional[str] = resolved_url.url_name
    except:
        resolved_url_name = None

    # Получаем все пункты меню за один запрос к БД
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')

    def build_menu_tree(items: List[MenuItem], parent: Optional[MenuItem] = None) -> List[Dict[str, Any]]:
        """
        Рекурсивно строит дерево меню.

        Args:
            items: Все пункты меню
            parent: Родительский пункт (None для корневых элементов)

        Returns:
            Список словарей с данными пунктов меню и их детей
        """
        tree: List[Dict[str, Any]] = []
        for item in items:
            if item.parent == parent:
                children: List[Dict[str, Any]] = build_menu_tree(items, parent=item)
                item_url: str = item.get_url()

                # Определяем активен ли текущий пункт меню
                is_active: bool = False
                if resolved_url_name and item.named_url == resolved_url_name:
                    is_active = True
                elif item_url == current_url:
                    is_active = True

                # Проверяем есть ли активные дети
                has_active_child: bool = any(
                    child['is_active'] or child['has_active_child']
                    for child in children
                )

                tree.append({
                    'item': item,
                    'children': children,
                    'is_active': is_active,
                    'has_active_child': has_active_child,
                    'url': item_url,
                })
        return tree

    # Строим дерево меню
    menu_tree: List[Dict[str, Any]] = build_menu_tree(menu_items)

    # Помечаем какие ветки должны быть развернуты
    for item in menu_tree:
        item['should_expand'] = item['is_active'] or item['has_active_child']
        if item['should_expand']:
            for child in item['children']:
                child['should_expand'] = child['is_active'] or child['has_active_child']

    return {
        'menu_tree': menu_tree,
        'menu_name': menu_name,
        'current_url': current_url,
    }