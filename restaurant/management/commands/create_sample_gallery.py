from django.core.management.base import BaseCommand
from restaurant.models import Gallery

class Command(BaseCommand):
    help = 'Crée des éléments de galerie de test pour le restaurant'

    def handle(self, *args, **options):
        # Supprimer les éléments existants
        Gallery.objects.all().delete()
        
        # Créer des éléments de galerie de test
        gallery_data = [
            {
                'title': 'Plat Signature - Coq au Vin',
                'description': 'Notre plat signature préparé avec des ingrédients frais et locaux.',
                'is_featured': True,
            },
            {
                'title': 'Ambiance du Restaurant',
                'description': 'L\'atmosphère chaleureuse et élégante de notre établissement.',
                'is_featured': True,
            },
            {
                'title': 'Terrasse en Soirée',
                'description': 'Profitez de nos plats sur notre terrasse avec vue imprenable.',
                'is_featured': False,
            },
            {
                'title': 'Chef en Action',
                'description': 'Notre chef étoilé prépare vos plats avec passion et expertise.',
                'is_featured': True,
            },
            {
                'title': 'Dessert Maison',
                'description': 'Nos desserts artisanaux préparés quotidiennement.',
                'is_featured': False,
            },
            {
                'title': 'Cave à Vins',
                'description': 'Découvrez notre sélection de vins d\'exception.',
                'is_featured': False,
            },
        ]
        
        for item_data in gallery_data:
            Gallery.objects.create(**item_data)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ {len(gallery_data)} éléments de galerie créés avec succès !')
        )











