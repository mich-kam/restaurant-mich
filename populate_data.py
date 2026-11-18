#!/usr/bin/env python
"""
Script pour peupler la base de données avec des données de test
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bites_restaurant.settings')
django.setup()

from django.contrib.auth.models import User
from restaurant.models import (
    Category, Dish, Chef, Testimonial, Service, 
    SiteSettings, BlogPost, Event, Gallery
)

def create_site_settings():
    """Créer les paramètres du site"""
    settings, created = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'Bites Restaurant',
            'hero_title': 'We Serve The Test You Love 😋',
            'hero_description': 'Discover the most delicious and authentic flavors from around the world.',
            'about_title': 'We Are More Than Multiple Service',
            'about_description': 'Our restaurant offers an exceptional dining experience with the finest ingredients and expert chefs.',
            'reservation_title': 'Do You Have Any Dinner Plan Today? Reserve Your Table',
            'reservation_description': 'Book your table now and enjoy our delicious cuisine in a warm and welcoming atmosphere.',
            'mobile_app_title': 'Never Feel Hungry! Download Our Mobile App Enjoy Delicious Foods',
            'mobile_app_description': 'Order your favorite dishes with just a few taps on your phone.',
            'phone': '+33 1 23 45 67 89',
            'email': 'contact@bites-restaurant.com',
            'address': '123 Rue de la Gastronomie, 75001 Paris, France',
            'facebook_url': 'https://facebook.com/bitesrestaurant',
            'twitter_url': 'https://twitter.com/bitesrestaurant',
            'instagram_url': 'https://instagram.com/bitesrestaurant',
            'youtube_url': 'https://youtube.com/bitesrestaurant',
        }
    )
    print(f"Site settings {'created' if created else 'already exists'}")

def create_categories():
    """Créer les catégories de plats"""
    categories_data = [
        {'name': 'Entrées', 'icon': 'fas fa-leaf', 'description': 'Délicieuses entrées pour commencer votre repas'},
        {'name': 'Plats Principaux', 'icon': 'fas fa-utensils', 'description': 'Nos plats signature préparés avec soin'},
        {'name': 'Desserts', 'icon': 'fas fa-ice-cream', 'description': 'Desserts gourmands pour terminer en beauté'},
        {'name': 'Boissons', 'icon': 'fas fa-wine-glass', 'description': 'Boissons rafraîchissantes et vins sélectionnés'},
        {'name': 'Salades', 'icon': 'fas fa-carrot', 'description': 'Salades fraîches et équilibrées'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        print(f"Category '{category.name}' {'created' if created else 'already exists'}")

def create_dishes():
    """Créer des plats de test"""
    dishes_data = [
        {
            'name': 'Salade César',
            'description': 'Salade romaine, parmesan, croûtons, sauce césar maison',
            'price': 12.50,
            'category_name': 'Salades',
            'is_popular': True
        },
        {
            'name': 'Steak Frites',
            'description': 'Steak de bœuf grillé, frites maison, sauce au poivre',
            'price': 24.90,
            'category_name': 'Plats Principaux',
            'is_popular': True
        },
        {
            'name': 'Pasta Carbonara',
            'description': 'Spaghetti, lardons, œuf, parmesan, poivre noir',
            'price': 18.50,
            'category_name': 'Plats Principaux',
            'is_popular': True
        },
        {
            'name': 'Tiramisu',
            'description': 'Dessert italien classique avec mascarpone et café',
            'price': 8.90,
            'category_name': 'Desserts',
            'is_popular': True
        },
        {
            'name': 'Soupe à l\'Oignon',
            'description': 'Soupe traditionnelle française gratinée au fromage',
            'price': 9.50,
            'category_name': 'Entrées'
        },
        {
            'name': 'Poulet Rôti',
            'description': 'Poulet fermier rôti aux herbes de Provence',
            'price': 22.00,
            'category_name': 'Plats Principaux'
        },
        {
            'name': 'Crème Brûlée',
            'description': 'Crème vanille caramélisée à la torche',
            'price': 7.50,
            'category_name': 'Desserts'
        },
        {
            'name': 'Vin Rouge',
            'description': 'Verre de vin rouge de la maison',
            'price': 6.50,
            'category_name': 'Boissons'
        }
    ]
    
    for dish_data in dishes_data:
        category = Category.objects.get(name=dish_data['category_name'])
        dish, created = Dish.objects.get_or_create(
            name=dish_data['name'],
            defaults={
                'description': dish_data['description'],
                'price': dish_data['price'],
                'category': category,
                'is_popular': dish_data.get('is_popular', False)
            }
        )
        print(f"Dish '{dish.name}' {'created' if created else 'already exists'}")

def create_chefs():
    """Créer des chefs de test"""
    chefs_data = [
        {
            'name': 'Chef Marie Dubois',
            'position': 'Chef Principal',
            'bio': 'Avec plus de 15 ans d\'expérience dans la gastronomie française, Chef Marie apporte sa passion et son expertise à chaque plat.',
            'experience_years': 15,
            'specialties': 'Cuisine française traditionnelle, pâtisserie fine'
        },
        {
            'name': 'Chef Marco Rossi',
            'position': 'Chef Pizzaiolo',
            'bio': 'Originaire de Naples, Chef Marco maîtrise l\'art de la pizza traditionnelle italienne.',
            'experience_years': 12,
            'specialties': 'Pizza napolitaine, cuisine italienne'
        },
        {
            'name': 'Chef Sarah Johnson',
            'position': 'Chef Pâtissier',
            'bio': 'Spécialisée dans la pâtisserie française, Chef Sarah crée des desserts d\'exception.',
            'experience_years': 10,
            'specialties': 'Pâtisserie française, chocolaterie'
        }
    ]
    
    for chef_data in chefs_data:
        chef, created = Chef.objects.get_or_create(
            name=chef_data['name'],
            defaults=chef_data
        )
        print(f"Chef '{chef.name}' {'created' if created else 'already exists'}")

def create_testimonials():
    """Créer des témoignages de test"""
    testimonials_data = [
        {
            'customer_name': 'Sophie Martin',
            'review': 'Excellente expérience culinaire ! Les plats sont délicieux et le service impeccable.',
            'rating': 5
        },
        {
            'customer_name': 'Pierre Durand',
            'review': 'Un restaurant exceptionnel avec une ambiance chaleureuse. Je recommande vivement !',
            'rating': 5
        },
        {
            'customer_name': 'Emma Wilson',
            'review': 'La meilleure salade César que j\'ai jamais mangée. Le personnel est très accueillant.',
            'rating': 4
        }
    ]
    
    for testimonial_data in testimonials_data:
        testimonial, created = Testimonial.objects.get_or_create(
            customer_name=testimonial_data['customer_name'],
            defaults=testimonial_data
        )
        print(f"Testimonial from '{testimonial.customer_name}' {'created' if created else 'already exists'}")

def create_services():
    """Créer des services de test"""
    services_data = [
        {
            'name': 'Réservation en ligne',
            'description': 'Réservez votre table en quelques clics sur notre site web',
            'icon': 'fas fa-calendar-check'
        },
        {
            'name': 'Livraison à domicile',
            'description': 'Profitez de nos plats chez vous avec notre service de livraison',
            'icon': 'fas fa-truck'
        },
        {
            'name': 'Événements privés',
            'description': 'Organisez vos événements spéciaux dans notre restaurant',
            'icon': 'fas fa-glass-cheers'
        },
        {
            'name': 'Cours de cuisine',
            'description': 'Apprenez à cuisiner avec nos chefs expérimentés',
            'icon': 'fas fa-graduation-cap'
        }
    ]
    
    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        print(f"Service '{service.name}' {'created' if created else 'already exists'}")

def create_blog_posts():
    """Créer des articles de blog de test"""
    # Créer un utilisateur pour les articles
    user, created = User.objects.get_or_create(
        username='site-author',
        defaults={
            'email': 'site-author@example.invalid',
        }
    )
    if created:
        user.set_unusable_password()
        user.save()
    
    blog_posts_data = [
        {
            'title': 'Les secrets de la cuisine française',
            'slug': 'secrets-cuisine-francaise',
            'content': 'Découvrez les techniques traditionnelles qui font la renommée de la cuisine française...',
            'excerpt': 'Un voyage culinaire au cœur de la gastronomie française',
            'is_published': True
        },
        {
            'title': 'Comment choisir le bon vin',
            'slug': 'choisir-bon-vin',
            'content': 'Guide complet pour accorder vos plats avec les vins appropriés...',
            'excerpt': 'Maîtrisez l\'art de l\'accord mets-vins',
            'is_published': True
        }
    ]
    
    for post_data in blog_posts_data:
        post, created = BlogPost.objects.get_or_create(
            slug=post_data['slug'],
            defaults={
                'title': post_data['title'],
                'content': post_data['content'],
                'excerpt': post_data['excerpt'],
                'author': user,
                'is_published': post_data['is_published']
            }
        )
        print(f"Blog post '{post.title}' {'created' if created else 'already exists'}")

def create_events():
    """Créer des événements de test"""
    from datetime import date, time, timedelta
    
    events_data = [
        {
            'title': 'Soirée Dégustation Vins',
            'description': 'Découvrez notre sélection de vins d\'exception avec nos sommeliers',
            'category': 'degustation',
            'date': date.today() + timedelta(days=7),
            'time': time(19, 0),
            'price': 45.00,
            'max_capacity': 20,
            'is_featured': True
        },
        {
            'title': 'Cours de Cuisine Italienne',
            'description': 'Apprenez à préparer des plats italiens authentiques',
            'category': 'cours',
            'date': date.today() + timedelta(days=14),
            'time': time(14, 0),
            'price': 35.00,
            'max_capacity': 15,
            'is_featured': True
        }
    ]
    
    for event_data in events_data:
        event, created = Event.objects.get_or_create(
            title=event_data['title'],
            defaults=event_data
        )
        print(f"Event '{event.title}' {'created' if created else 'already exists'}")

def main():
    """Fonction principale pour peupler la base de données"""
    print("=== Peuplement de la base de données ===")
    
    create_site_settings()
    create_categories()
    create_dishes()
    create_chefs()
    create_testimonials()
    create_services()
    create_blog_posts()
    create_events()
    
    print("\n=== Peuplement terminé avec succès ! ===")
    print("Vous pouvez maintenant accéder au site avec les données de test.")

if __name__ == '__main__':
    main()
