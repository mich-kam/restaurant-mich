from django.core.management.base import BaseCommand
from django.utils import timezone
from restaurant.models import Event
from datetime import date, time, timedelta

class Command(BaseCommand):
    help = 'Crée des événements de test pour le restaurant'

    def handle(self, *args, **options):
        # Supprimer les événements existants
        Event.objects.all().delete()
        
        # Créer des événements de test
        events_data = [
            {
                'title': 'Dégustation de Vins Premium',
                'description': 'Découvrez notre sélection de vins d\'exception avec notre sommelier expert. Une soirée inoubliable pour les amateurs de vin.',
                'category': 'degustation',
                'date': date.today() + timedelta(days=7),
                'time': time(19, 30),
                'location': 'Cave à vin privée',
                'price': 85.00,
                'max_capacity': 20,
                'current_bookings': 12,
                'is_featured': True,
            },
            {
                'title': 'Cours de Cuisine Française',
                'description': 'Apprenez les secrets de la cuisine française avec notre chef étoilé. Préparation de plats traditionnels.',
                'category': 'cours',
                'date': date.today() + timedelta(days=14),
                'time': time(14, 0),
                'location': 'Cuisine pédagogique',
                'price': 120.00,
                'max_capacity': 15,
                'current_bookings': 8,
                'is_featured': True,
            },
            {
                'title': 'Soirée Jazz & Dîner',
                'description': 'Une soirée élégante avec musique jazz live et menu gastronomique spécialement créé pour l\'occasion.',
                'category': 'soiree',
                'date': date.today() + timedelta(days=21),
                'time': time(20, 0),
                'location': 'Salle principale',
                'price': 95.00,
                'max_capacity': 50,
                'current_bookings': 35,
                'is_featured': False,
            },
            {
                'title': 'Événement Corporate - Team Building',
                'description': 'Organisez votre événement d\'entreprise dans un cadre unique. Menu personnalisé et service premium.',
                'category': 'corporate',
                'date': date.today() + timedelta(days=30),
                'time': time(18, 30),
                'location': 'Salle privée',
                'price': 65.00,
                'max_capacity': 40,
                'current_bookings': 25,
                'is_featured': False,
            },
            {
                'title': 'Célébration d\'Anniversaire',
                'description': 'Fêtez votre anniversaire en toute intimité. Décoration personnalisée et gâteau d\'anniversaire inclus.',
                'category': 'anniversaire',
                'date': date.today() + timedelta(days=10),
                'time': time(19, 0),
                'location': 'Salon privé',
                'price': 75.00,
                'max_capacity': 25,
                'current_bookings': 18,
                'is_featured': False,
            },
            {
                'title': 'Dégustation de Fromages Artisanaux',
                'description': 'Découvrez une sélection unique de fromages français accompagnés de vins d\'exception.',
                'category': 'degustation',
                'date': date.today() + timedelta(days=17),
                'time': time(20, 30),
                'location': 'Terrasse privée',
                'price': 55.00,
                'max_capacity': 30,
                'current_bookings': 22,
                'is_featured': True,
            },
        ]
        
        for event_data in events_data:
            Event.objects.create(**event_data)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ {len(events_data)} événements créés avec succès !')
        )













