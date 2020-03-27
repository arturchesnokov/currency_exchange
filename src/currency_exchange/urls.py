from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings

from django.views.generic.base import TemplateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

API_PREFIX = 'api/v1'

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),

    path('currency/', include('currency.urls')),
    path('account/', include('account.urls')),

    # API
    path(f'{API_PREFIX}/currency/', include('currency.api.urls')),

    path(f'{API_PREFIX}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{API_PREFIX}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
# SWAGGER
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='DOCS')

urlpatterns.append(path(f'{API_PREFIX}/docs/', schema_view))

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
