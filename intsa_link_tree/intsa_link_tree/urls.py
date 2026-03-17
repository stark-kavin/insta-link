from django.contrib import admin
from django.urls import path
from main.views import index, products, track_redirect, admin_dashboard, admin_manage, admin_api_clicks, admin_api_sources, admin_api_timeline
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin-panel/', admin_dashboard, name='admin_dashboard'),
    path('admin-panel/manage/<str:model_name>/', admin_manage, name='admin_manage'),
    path('admin-panel/api/clicks/', admin_api_clicks, name='admin_api_clicks'),
    path('admin-panel/api/sources/', admin_api_sources, name='admin_api_sources'),
    path('admin-panel/api/timeline/', admin_api_timeline, name='admin_api_timeline'),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('products/', products, name='products'),
    path('track/<str:link_type>/<int:link_id>/', track_redirect, name='track_redirect'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
