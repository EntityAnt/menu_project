from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.text import slugify


class MenuItem(models.Model):
    """Модель для хранения пунктов древовидного меню"""

    name = models.CharField(max_length=50, verbose_name='Название пункта меню')
    named_url = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Named URL',
        help_text='Именованный URL-шаблон, например: "product_list"'
    )
    explicit_url = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Явный URL',
        help_text='Явный URL (если нет named URL), например: "/products/"'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE,
        verbose_name='Родительский пункт'
    )
    menu_name = models.CharField(
        max_length=50,
        verbose_name='Имя меню',
        help_text='Идентификатор меню, например "main_menu"'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order']

    def __str__(self) -> str:
        """Строковое представление пункта меню"""
        return self.name

    def get_url(self) -> str:
        """
        Возвращает URL для пункта меню.
        Приоритет: named_url > explicit_url > заглушка '#'
        """
        if self.named_url:
            try:
                url = reverse(self.named_url)
            except NoReverseMatch:
                url = self.named_url
            return url
        elif self.explicit_url:
            return self.explicit_url
        return '#'

    def save(self, *args, **kwargs) -> None:
        """Переопределение save для автоматического создания named_url при необходимости"""
        if not self.explicit_url and not self.named_url:
            self.named_url = slugify(self.name)
        super().save(*args, **kwargs)
