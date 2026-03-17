from django.contrib import admin
from django.urls import path
from main.views import index, products, track_redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('products/', products, name='products'),
    path('track/<str:link_type>/<int:link_id>/', track_redirect, name='track_redirect'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
