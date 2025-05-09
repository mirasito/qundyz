from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1) подключаем allauth
    path('accounts/', include('allauth.urls')),

    # 2) ваш собственный “аккаунтный” апи (если нужно)
    path('accounts/profile/', include('apps.accounts.urls')),

    path('',           include('apps.estimates.urls')),
    path('estimates/', include('apps.estimates.urls')),
    path('projects/',  include('apps.projects.urls')),
    path('api/chat/',  include('apps.chat.urls')),
    path('api/ai/',    include('apps.ai_integration.urls')),

    path(
      'estimate_input/',
      TemplateView.as_view(template_name="estimates/input_form.html"),
      name='estimate_input'
    ),
    path(
      'my_budget/',
      TemplateView.as_view(template_name="budget/my_budget.html"),
      name='my_budget'
    ),
    path(
      'marketplace/',
      TemplateView.as_view(template_name="marketplace/index.html"),
      name='marketplace'
    ),
    # если вам нужен прямой рендер профиля
    path(
      'profile/',
      TemplateView.as_view(template_name="accounts/profile.html"),
      name='user_profile'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)