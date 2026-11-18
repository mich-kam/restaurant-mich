from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from restaurant.models import Event

class Command(BaseCommand):
    help = 'Populate database with sample events'

    def handle(self, *args, **options):
        # Supprimer les événements existants
        Event.objects.all().delete()
        
        # Créer des événements d'exemple
        events_data = [
            {
                'title': 'Dégustation de Vins Français',
                'description': 'Une soirée exceptionnelle pour découvrir les meilleurs vins français. Notre sommelier expert vous guidera à travers une sélection unique de vins rouges, blancs et rosés, accompagnés de fromages affinés et de charcuteries artisanales.',
                'category': 'degustation',
                'date': date.today() + timedelta(days=7),
                'time': '19:00',
                'location': 'Salle privée du restaurant',
                'price': 85.00,
                'max_capacity': 20,
                'current_bookings': 12,
                'is_featured': True,
            },
            {
                'title': 'Cours de Cuisine Italienne',
                'description': 'Apprenez à préparer les plats traditionnels italiens avec notre chef spécialisé. Vous découvrirez les secrets de la pasta fraîche, des sauces authentiques et des desserts italiens classiques.',
                'category': 'cours',
                'date': date.today() + timedelta(days=14),
                'time': '14:00',
                'location': 'Cuisine pédagogique',
                'price': 120.00,
                'max_capacity': 15,
                'current_bookings': 8,
                'is_featured': True,
            },
            {
                'title': 'Soirée Thématique Japon',
                'description': 'Une immersion totale dans la culture culinaire japonaise. Dégustez des sushis, sashimis, tempuras et autres spécialités préparées par notre chef japonais. Ambiance zen garantie !',
                'category': 'soiree',
                'date': date.today() + timedelta(days=21),
                'time': '20:00',
                'location': 'Restaurant principal',
                'price': 95.00,
                'max_capacity': 30,
                'current_bookings': 25,
                'is_featured': False,
            },
            {
                'title': 'Dîner Romantique Saint-Valentin',
                'description': 'Célébrez l\'amour avec notre menu spécial Saint-Valentin. Un dîner aux chandelles avec champagne, chocolats artisanaux et musique live pour une soirée inoubliable.',
                'category': 'soiree',
                'date': date.today() + timedelta(days=28),
                'time': '19:30',
                'location': 'Terrasse privée',
                'price': 150.00,
                'max_capacity': 25,
                'current_bookings': 18,
                'is_featured': True,
            },
            {
                'title': 'Atelier Pâtisserie Française',
                'description': 'Maîtrisez l\'art de la pâtisserie française ! Apprenez à préparer des croissants, éclairs, macarons et autres délices dans notre atelier dédié.',
                'category': 'cours',
                'date': date.today() + timedelta(days=35),
                'time': '10:00',
                'location': 'Laboratoire pâtisserie',
                'price': 140.00,
                'max_capacity': 12,
                'current_bookings': 6,
                'is_featured': False,
            },
            {
                'title': 'Dégustation de Fromages d\'Exception',
                'description': 'Découvrez une sélection rare de fromages français et internationaux, accompagnés de vins d\'exception. Une expérience sensorielle unique pour les amateurs de fromage.',
                'category': 'degustation',
                'date': date.today() + timedelta(days=42),
                'time': '18:30',
                'location': 'Cave à fromages',
                'price': 75.00,
                'max_capacity': 18,
                'current_bookings': 15,
                'is_featured': False,
            },
            {
                'title': 'Soirée Mariage - Dégustation Menu',
                'description': 'Préparez votre mariage en dégustant nos menus spécialement conçus pour les grandes occasions. Notre équipe vous accompagnera dans le choix parfait pour votre jour J.',
                'category': 'mariage',
                'date': date.today() + timedelta(days=49),
                'time': '19:00',
                'location': 'Salle de réception',
                'price': 65.00,
                'max_capacity': 40,
                'current_bookings': 22,
                'is_featured': False,
            },
            {
                'title': 'Événement Corporate - Team Building',
                'description': 'Renforcez l\'esprit d\'équipe avec notre événement corporate culinaire. Compétition amicale de cuisine, dégustations et networking dans un cadre professionnel.',
                'category': 'corporate',
                'date': date.today() + timedelta(days=56),
                'time': '17:00',
                'location': 'Espace événementiel',
                'price': 110.00,
                'max_capacity': 50,
                'current_bookings': 35,
                'is_featured': False,
            },
        ]
        
        for event_data in events_data:
            Event.objects.create(**event_data)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(events_data)} sample events')
        )

