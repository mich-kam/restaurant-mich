from django import template
from django.template.defaultfilters import floatformat
from restaurant.models import SiteSettings

register = template.Library()

@register.simple_tag
def get_dynamic_image_url(category, index=0):
    """Retourne une URL d'image dynamique basée sur la catégorie et l'index"""
    dynamic_urls = {
        'dishes': [
            'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1504674900240-9c1c0c0c0c0c?w=800&h=600&fit=crop',
        ],
        'events': [
            'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=1000&h=600&fit=crop',
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=1000&h=600&fit=crop',
        ],
        'chefs': [
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=400&fit=crop',
        ],
        'blog': [
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=1000&h=600&fit=crop',
            'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=1000&h=600&fit=crop',
        ]
    }
    
    urls = dynamic_urls.get(category, dynamic_urls['dishes'])
    return urls[index % len(urls)]

@register.filter
def get_image_url(instance, category='dishes'):
    """Retourne l'URL de l'image d'une instance ou une URL de fallback"""
    if instance.image and instance.image.url:
        return instance.image.url
    else:
        # Utiliser l'ID de l'instance comme index pour la variété
        index = getattr(instance, 'id', 0) or 0
        return get_dynamic_image_url(category, index)

@register.simple_tag
def get_fallback_image(category='dishes'):
    """Retourne une URL d'image de fallback pour une catégorie"""
    return get_dynamic_image_url(category, 0)

@register.simple_tag
def get_hero_image_url(page_type='home'):
    """Récupère l'URL de l'image Hero pour une page spécifique"""
    try:
        settings = SiteSettings.get_settings()
        return settings.get_hero_image_url(page_type)
    except:
        return get_fallback_hero_image(page_type)

def get_fallback_hero_image(page_type):
    """Retourne une image Hero de fallback selon le type de page"""
    fallback_hero_images = {
        'home': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
        'menu': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
        'events': 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
        'delivery': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
        'faq': 'https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
        'loyalty': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
        'opening_hours': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
        'about': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
        'contact': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
    }
    return fallback_hero_images.get(page_type, fallback_hero_images['home'])
