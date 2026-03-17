from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
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


# Admin Dashboard Views
def admin_dashboard(request):
    """Main admin dashboard"""
    # Statistics
    total_clicks = LinkClick.objects.count()
    redirect_clicks = LinkClick.objects.filter(link_type='redirect').count()
    product_clicks = LinkClick.objects.filter(link_type='product').count()
    instagram_clicks = LinkClick.objects.filter(source='instagram').count()
    
    # Redirect and Product links count
    redirect_links_count = RedirectLink.objects.count()
    product_links_count = ProductLink.objects.count()
    
    # Recent clicks
    recent_clicks = LinkClick.objects.all().order_by('-timestamp')[:10]
    
    context = {
        'total_clicks': total_clicks,
        'redirect_clicks': redirect_clicks,
        'product_clicks': product_clicks,
        'instagram_clicks': instagram_clicks,
        'redirect_links_count': redirect_links_count,
        'product_links_count': product_links_count,
        'recent_clicks': recent_clicks,
    }
    
    return render(request, 'admin/dashboard.html', context)


def admin_manage(request, model_name):
    """Manage specific models"""
    if model_name == 'redirectlinks':
        items = RedirectLink.objects.all()
        template = 'admin/manage_redirectlinks.html'
    elif model_name == 'productlinks':
        items = ProductLink.objects.all()
        template = 'admin/manage_productlinks.html'
    elif model_name == 'clicks':
        items = LinkClick.objects.all().order_by('-timestamp')
        template = 'admin/manage_clicks.html'
    else:
        return redirect('admin_dashboard')
    
    context = {'items': items, 'model_name': model_name}
    return render(request, template, context)


def admin_api_clicks(request):
    """API for click type distribution"""
    data = LinkClick.objects.values('link_type').annotate(count=Count('id'))
    return JsonResponse({
        'labels': [item['link_type'].replace('redirect', 'Redirect').replace('product', 'Product') for item in data],
        'data': [item['count'] for item in data],
    })


def admin_api_sources(request):
    """API for source distribution"""
    data = LinkClick.objects.values('source').annotate(count=Count('id'))
    return JsonResponse({
        'labels': [item['source'].replace('instagram', 'Instagram').replace('other', 'Other') for item in data],
        'data': [item['count'] for item in data],
    })


def admin_api_timeline(request):
    """API for timeline (last 30 days)"""
    thirty_days_ago = timezone.now() - timedelta(days=30)
    clicks = LinkClick.objects.filter(timestamp__gte=thirty_days_ago).extra(
        select={'date': 'DATE(timestamp)'}
    ).values('date').annotate(count=Count('id')).order_by('date')
    
    return JsonResponse({
        'labels': [item['date'].strftime('%m/%d') for item in clicks],
        'data': [item['count'] for item in clicks],
    })


