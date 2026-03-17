from django.contrib import admin
from .models import SiteConfig, RedirectLink, ProductLink, LinkClick

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    pass

@admin.register(RedirectLink)
class RedirectLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

@admin.register(ProductLink)
class ProductLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

@admin.register(LinkClick)
class LinkClickAdmin(admin.ModelAdmin):
    list_display = ('link_type', 'link_id', 'source', 'timestamp', 'referer')
    list_filter = ('link_type', 'source', 'timestamp')
    readonly_fields = ('timestamp', 'referer', 'user_agent', 'source', 'link_type', 'link_id')
