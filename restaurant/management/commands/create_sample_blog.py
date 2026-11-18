from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from restaurant.models import BlogPost
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Crée des articles de blog de test pour le restaurant'

    def handle(self, *args, **options):
        # Supprimer les articles existants
        BlogPost.objects.all().delete()
        
        # Create a non-staff author if needed.
        user, created = User.objects.get_or_create(
            username='site-author',
            defaults={
                'email': 'site-author@example.invalid',
                'first_name': 'Admin',
                'last_name': 'Restaurant',
            }
        )
        if created:
            user.set_unusable_password()
            user.save()
        
        # Créer des articles de blog de test
        blog_data = [
            {
                'title': 'Les Secrets de la Cuisine Française',
                'content': '''
                <p>La cuisine française est reconnue dans le monde entier pour sa sophistication et sa richesse. Dans cet article, nous vous révélons les secrets qui font de la gastronomie française un art à part entière.</p>
                
                <h3>L'importance des ingrédients frais</h3>
                <p>La base de toute cuisine française authentique réside dans la qualité des ingrédients. Nos chefs sélectionnent avec soin chaque produit, privilégiant les fournisseurs locaux et les produits de saison.</p>
                
                <h3>Les techniques traditionnelles</h3>
                <p>De la sauce au beurre à la cuisson sous vide, les techniques françaises sont le fruit de siècles de perfectionnement. Chaque méthode a été développée pour révéler le meilleur de chaque ingrédient.</p>
                
                <h3>L'art de la présentation</h3>
                <p>En France, manger est une expérience sensorielle complète. La présentation des plats est aussi importante que leur goût, créant une harmonie visuelle qui prépare le palais à la dégustation.</p>
                ''',
                'excerpt': 'Découvrez les secrets qui font de la cuisine française un art reconnu mondialement.',
                'is_published': True,
            },
            {
                'title': 'Notre Sélection de Vins d\'Exception',
                'content': '''
                <p>Notre cave à vins abrite une collection soigneusement sélectionnée de vins français et internationaux. Chaque bouteille a été choisie pour sa qualité exceptionnelle et sa capacité à sublimer nos plats.</p>
                
                <h3>Les vins de Bordeaux</h3>
                <p>Les vins de Bordeaux, avec leur complexité et leur élégance, sont parfaits pour accompagner nos plats de viande rouge et nos fromages affinés.</p>
                
                <h3>Les vins de Bourgogne</h3>
                <p>Les vins blancs de Bourgogne, avec leur finesse et leur minéralité, s\'accordent parfaitement avec nos plats de poisson et nos entrées raffinées.</p>
                
                <h3>Les vins du Rhône</h3>
                <p>Les vins du Rhône, avec leur puissance et leurs arômes de fruits mûrs, sont idéaux pour nos plats en sauce et nos viandes grillées.</p>
                ''',
                'excerpt': 'Explorez notre collection de vins d\'exception, sélectionnés pour sublimer votre expérience gastronomique.',
                'is_published': True,
            },
            {
                'title': 'L\'Art de la Pâtisserie Française',
                'content': '''
                <p>La pâtisserie française est un art qui allie précision technique et créativité artistique. Nos pâtissiers perpétuent les traditions séculaires tout en apportant leur touche personnelle.</p>
                
                <h3>Les bases de la pâtisserie</h3>
                <p>Chaque pâtisserie commence par des bases solides : pâte feuilletée, pâte à choux, crème pâtissière... Ces techniques fondamentales sont la base de toutes nos créations.</p>
                
                <h3>Les classiques revisités</h3>
                <p>Nous réinventons les classiques de la pâtisserie française en respectant leur essence tout en apportant une touche moderne et personnelle.</p>
                
                <h3>La saisonnalité</h3>
                <p>Nos pâtisseries évoluent au fil des saisons, utilisant les fruits et ingrédients les plus frais pour créer des saveurs uniques et authentiques.</p>
                ''',
                'excerpt': 'Découvrez l\'art de la pâtisserie française, où tradition et innovation se rencontrent.',
                'is_published': True,
            },
        ]
        
        for item_data in blog_data:
            # Créer le slug à partir du titre
            slug = slugify(item_data['title'])
            item_data['slug'] = slug
            item_data['author'] = user
            
            BlogPost.objects.create(**item_data)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ {len(blog_data)} articles de blog créés avec succès !')
        )












