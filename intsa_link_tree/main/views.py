from django.shortcuts import render, redirect, get_object_or_404
from .models import SiteConfig, RedirectLink, ProductLink, LinkClick

def index(request):
    site_config = SiteConfig.load()
    redirect_links = RedirectLink.objects.all()
    product_links = ProductLink.objects.all()
    
    context = {
        'site_config': site_config,
        'redirect_links': redirect_links,
        'product_links': product_links,
    }
    return render(request, 'index.html', context)

def products(request):
    site_config = SiteConfig.load()
    product_links = ProductLink.objects.all()
    context = {
        'site_config': site_config,
        'product_links': product_links,
    }
    return render(request, 'products.html', context)


def track_redirect(request, link_type, link_id):
    if link_type == 'redirect':
        link = get_object_or_404(RedirectLink, id=link_id)
    elif link_type == 'product':
        link = get_object_or_404(ProductLink, id=link_id)
    else:
        return redirect('index')

    referer = request.META.get('HTTP_REFERER', '')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    source = 'other'
    if 'instagram.com' in referer.lower():
        source = 'instagram'

    LinkClick.objects.create(
        referer=referer if referer else None,
        user_agent=user_agent,
        source=source,
        link_type=link_type,
        link_id=link_id
    )

    return redirect(link.url)