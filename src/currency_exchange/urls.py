from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings

from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),

    path('currency/', include('currency.urls')),
    path('account/', include('account.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#     import debug_toolbar
#
#     urlpatterns = [
#                       path('__debug__/', include(debug_toolbar.urls)),
#                   ] + urlpatterns
