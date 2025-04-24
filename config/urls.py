

from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('test-menu/', TemplateView.as_view(template_name='test_menu.html'), name='test_menu'),
    path('', TemplateView.as_view(template_name='test_menu.html'), name='home'),
]
