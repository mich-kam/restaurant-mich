from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from restaurant.models import (
    Category, Dish, Chef, Testimonial, Service, SiteSettings,
    BlogPost, Event, Gallery
)

class Command(BaseCommand):
    help = 'Populate the database with sample restaurant data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Drinks', 'icon': 'fas fa-wine-glass'},
            {'name': 'Main Course', 'icon': 'fas fa-utensils'},
            {'name': 'Desserts', 'icon': 'fas fa-ice-cream'},
            {'name': 'Appetizers', 'icon': 'fas fa-cheese'},
            {'name': 'Salads', 'icon': 'fas fa-leaf'},
            {'name': 'Pizza', 'icon': 'fas fa-pizza-slice'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'icon': cat_data['icon']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create dishes
        dishes_data = [
            {
                'name': 'Margherita Pizza',
                'description': 'Classic pizza with tomato sauce, mozzarella, and fresh basil',
                'price': 18.99,
                'category': 'Pizza',
                'is_popular': True
            },
            {
                'name': 'Caesar Salad',
                'description': 'Fresh romaine lettuce with Caesar dressing, croutons, and parmesan',
                'price': 12.99,
                'category': 'Salads',
                'is_popular': True
            },
            {
                'name': 'Grilled Salmon',
                'description': 'Fresh Atlantic salmon grilled to perfection with seasonal vegetables',
                'price': 28.99,
                'category': 'Main Course',
                'is_popular': True
            },
            {
                'name': 'Chocolate Lava Cake',
                'description': 'Warm chocolate cake with molten center, served with vanilla ice cream',
                'price': 9.99,
                'category': 'Desserts',
                'is_popular': True
            },
            {
                'name': 'Bruschetta',
                'description': 'Toasted bread topped with tomatoes, garlic, and fresh basil',
                'price': 8.99,
                'category': 'Appetizers'
            },
            {
                'name': 'Pasta Carbonara',
                'description': 'Spaghetti with eggs, cheese, pancetta, and black pepper',
                'price': 16.99,
                'category': 'Main Course'
            },
            {
                'name': 'Fresh Fruit Smoothie',
                'description': 'Blend of seasonal fruits with yogurt and honey',
                'price': 6.99,
                'category': 'Drinks'
            },
            {
                'name': 'Tiramisu',
                'description': 'Classic Italian dessert with coffee-soaked ladyfingers and mascarpone',
                'price': 11.99,
                'category': 'Desserts'
            },
            {
                'name': 'Garlic Bread',
                'description': 'Crusty bread brushed with garlic butter and herbs',
                'price': 5.99,
                'category': 'Appetizers'
            },
            {
                'name': 'Beef Burger',
                'description': 'Juicy beef patty with lettuce, tomato, and special sauce',
                'price': 14.99,
                'category': 'Main Course'
            },
            {
                'name': 'Greek Salad',
                'description': 'Mixed greens with feta cheese, olives, and Mediterranean dressing',
                'price': 13.99,
                'category': 'Salads'
            },
            {
                'name': 'Iced Coffee',
                'description': 'Cold brewed coffee with cream and sugar',
                'price': 4.99,
                'category': 'Drinks'
            }
        ]
        
        for dish_data in dishes_data:
            dish, created = Dish.objects.get_or_create(
                name=dish_data['name'],
                defaults={
                    'description': dish_data['description'],
                    'price': dish_data['price'],
                    'category': categories[dish_data['category']],
                    'is_popular': dish_data.get('is_popular', False)
                }
            )
            if created:
                self.stdout.write(f'Created dish: {dish.name}')
        
        # Create chefs
        chefs_data = [
            {
                'name': 'Chef Maria Rodriguez',
                'position': 'Head Chef',
                'bio': 'With over 15 years of experience in fine dining, Chef Maria brings passion and creativity to every dish.',
                'experience_years': 15,
                'specialties': 'Mediterranean cuisine, seafood, pasta'
            },
            {
                'name': 'Chef James Chen',
                'position': 'Sous Chef',
                'bio': 'Specializing in Asian fusion and modern techniques, Chef James creates innovative flavor combinations.',
                'experience_years': 10,
                'specialties': 'Asian fusion, molecular gastronomy, desserts'
            },
            {
                'name': 'Chef Sarah Johnson',
                'position': 'Pastry Chef',
                'bio': 'A master of sweet creations, Chef Sarah crafts beautiful and delicious desserts that are works of art.',
                'experience_years': 12,
                'specialties': 'Pastries, cakes, chocolate work, bread making'
            },
            {
                'name': 'Chef Antonio Rossi',
                'position': 'Pizza Chef',
                'bio': 'Born in Naples, Chef Antonio brings authentic Italian pizza-making techniques to our kitchen.',
                'experience_years': 8,
                'specialties': 'Neapolitan pizza, wood-fired cooking, Italian cuisine'
            }
        ]
        
        for chef_data in chefs_data:
            chef, created = Chef.objects.get_or_create(
                name=chef_data['name'],
                defaults={
                    'position': chef_data['position'],
                    'bio': chef_data['bio'],
                    'experience_years': chef_data['experience_years'],
                    'specialties': chef_data['specialties']
                }
            )
            if created:
                self.stdout.write(f'Created chef: {chef.name}')
        
        # Create testimonials
        testimonials_data = [
            {
                'customer_name': 'Emily Thompson',
                'review': 'Amazing food and excellent service! The atmosphere is perfect for a romantic dinner.',
                'rating': 5
            },
            {
                'customer_name': 'Michael Davis',
                'review': 'Best restaurant in town! The pizza is absolutely delicious and the staff is very friendly.',
                'rating': 5
            },
            {
                'customer_name': 'Lisa Wang',
                'review': 'Great experience! The food was fresh, flavorful, and beautifully presented.',
                'rating': 4
            },
            {
                'customer_name': 'Robert Johnson',
                'review': 'Outstanding service and incredible flavors. Will definitely come back!',
                'rating': 5
            },
            {
                'customer_name': 'Amanda Smith',
                'review': 'Perfect for family dinners. The kids loved the pasta and we enjoyed the wine selection.',
                'rating': 4
            }
        ]
        
        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                customer_name=testimonial_data['customer_name'],
                defaults={
                    'review': testimonial_data['review'],
                    'rating': testimonial_data['rating']
                }
            )
            if created:
                self.stdout.write(f'Created testimonial from: {testimonial.customer_name}')
        
        # Create services
        services_data = [
            {
                'name': 'Online Ordering',
                'description': 'Order your favorite dishes online and enjoy quick delivery or pickup',
                'icon': 'fas fa-shopping-cart'
            },
            {
                'name': 'Catering Services',
                'description': 'Perfect catering for your special events and celebrations',
                'icon': 'fas fa-users'
            },
            {
                'name': 'Private Dining',
                'description': 'Exclusive private dining rooms for intimate gatherings',
                'icon': 'fas fa-door-open'
            },
            {
                'name': 'Wine Pairing',
                'description': 'Expert wine recommendations to complement your meal',
                'icon': 'fas fa-wine-glass-alt'
            }
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'description': service_data['description'],
                    'icon': service_data['icon']
                }
            )
            if created:
                self.stdout.write(f'Created service: {service.name}')
        
        # Create site settings
        settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Bites',
                'hero_title': 'We Serve The Test You Love 😋',
                'hero_description': 'Discover the most delicious and authentic flavors from around the world. Our expert chefs create memorable dining experiences with fresh, locally-sourced ingredients.',
                'about_title': 'We Are More Than Multiple Service',
                'about_description': 'At Bites, we believe that great food brings people together. Our passion for culinary excellence drives us to create dishes that not only taste amazing but also tell a story. From traditional recipes to modern innovations, every dish is crafted with love and attention to detail.',
                'reservation_title': 'Do You Have Any Dinner Plan Today? Reserve Your Table',
                'reservation_description': 'Join us for an unforgettable dining experience. Reserve your table today and let us take care of the rest.',
                'mobile_app_title': 'Never Feel Hungry! Download Our Mobile App Enjoy Delicious Foods',
                'mobile_app_description': 'Order your favorite dishes on the go with our mobile app. Get exclusive offers and track your orders in real-time.',
                'phone': '+1 (555) 123-4567',
                'email': 'info@bites-restaurant.com',
                'address': '123 Main Street, Downtown, City, State 12345',
                'facebook_url': 'https://facebook.com/bitesrestaurant',
                'twitter_url': 'https://twitter.com/bitesrestaurant',
                'instagram_url': 'https://instagram.com/bitesrestaurant',
                'youtube_url': 'https://youtube.com/bitesrestaurant'
            }
        )
        if created:
            self.stdout.write('Created site settings')
        
        # Create blog posts
        blog_posts_data = [
            {
                'title': 'The Art of Pizza Making',
                'slug': 'art-of-pizza-making',
                'content': '''
                Pizza making is truly an art form that combines tradition with creativity. At Bites, we take pride in our authentic Neapolitan-style pizzas, crafted with love and attention to detail.

                Our journey begins with the perfect dough - a carefully balanced mixture of flour, water, salt, and yeast that's allowed to ferment slowly for optimal flavor development. The dough is then hand-stretched to create that characteristic thin, crispy base that Neapolitan pizza is famous for.

                The sauce is made from San Marzano tomatoes, grown in the volcanic soil of Mount Vesuvius, giving it a unique sweetness and acidity. We use only the finest mozzarella di bufala, which melts beautifully and adds a rich, creamy texture to each bite.

                Toppings are selected with care, focusing on quality and freshness. From classic Margherita to innovative combinations, each pizza tells a story of tradition and innovation.

                The final step is cooking in our wood-fired oven at high temperatures, which creates the perfect char and brings out the natural flavors of all ingredients. The result is a pizza that's crispy on the outside, soft on the inside, and bursting with authentic Italian flavors.

                Join us to experience the true art of pizza making, where every slice is a masterpiece of flavor and tradition.
                ''',
                'excerpt': 'Discover the secrets behind our authentic Neapolitan-style pizzas and the traditional techniques we use to create the perfect pie.',
                'is_published': True
            },
            {
                'title': 'Seasonal Ingredients: Spring Edition',
                'slug': 'seasonal-ingredients-spring',
                'content': '''
                Spring brings a bounty of fresh, vibrant ingredients that inspire our seasonal menu. This time of year, we focus on light, refreshing dishes that celebrate the renewal of nature.

                Asparagus, with its tender stalks and delicate flavor, takes center stage in our spring risotto. We pair it with fresh herbs like chives and tarragon, creating a dish that's both comforting and bright.

                Fresh peas add sweetness and texture to our spring pasta dishes, while baby spinach provides a nutritious base for our seasonal salads. We also incorporate spring onions and garlic scapes, which offer a milder, more nuanced flavor than their mature counterparts.

                For desserts, we feature rhubarb and strawberries, creating tarts and compotes that capture the essence of spring. Our pastry chef creates beautiful, light desserts that complement the season perfectly.

                We believe in supporting local farmers and using ingredients at their peak freshness. This commitment to seasonal cooking not only results in better-tasting dishes but also supports sustainable agriculture practices.

                Come experience the flavors of spring with us, where every dish celebrates the season's bounty and the joy of fresh, local ingredients.
                ''',
                'excerpt': 'Explore how we incorporate fresh spring ingredients into our seasonal menu, creating dishes that celebrate the season\'s bounty.',
                'is_published': True
            },
            {
                'title': 'Wine Pairing Guide: Red Wines',
                'slug': 'wine-pairing-red-wines',
                'content': '''
                Wine pairing is an essential part of the dining experience, and red wines offer incredible versatility when it comes to food matching. At Bites, our sommelier has carefully curated a selection of red wines that complement our menu perfectly.

                Cabernet Sauvignon, with its full body and rich tannins, pairs beautifully with our grilled meats and aged cheeses. The wine's black fruit flavors and herbal notes create a harmonious balance with hearty dishes like our beef tenderloin or lamb chops.

                Pinot Noir, known for its elegance and complexity, is perfect with our salmon dishes and mushroom-based pasta. Its bright acidity and red fruit flavors enhance the natural flavors of the food without overwhelming them.

                Merlot, with its softer tannins and plum flavors, works wonderfully with our pizza selections and roasted chicken dishes. It's also an excellent choice for those who are new to red wine, as it's generally more approachable.

                For our Italian dishes, we recommend Chianti or Sangiovese, which have the perfect acidity to cut through rich tomato sauces and complement the herbs and spices used in traditional Italian cooking.

                Our wine list is constantly evolving, and we're always excited to introduce our guests to new and interesting wines that enhance their dining experience.
                ''',
                'excerpt': 'Learn about the art of wine pairing and discover which red wines complement our dishes perfectly.',
                'is_published': True
            }
        ]
        
        # Get or create a user for blog posts
        user, created = User.objects.get_or_create(
            username='site-author',
            defaults={
                'email': 'site-author@example.invalid',
            }
        )
        if created:
            user.set_unusable_password()
            user.save()
            self.stdout.write('Created a non-staff blog author')
        
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
            if created:
                self.stdout.write(f'Created blog post: {post.title}')
        
        # Create events
        events_data = [
            {
                'title': 'Wine Tasting Evening',
                'description': 'Join us for an exclusive wine tasting event featuring premium wines from around the world. Includes appetizers and expert guidance from our sommelier.',
                'date': '2024-03-15',
                'time': '19:00'
            },
            {
                'title': 'Chef\'s Table Experience',
                'description': 'An intimate dining experience where you\'ll watch our head chef prepare a special multi-course meal right in front of you.',
                'date': '2024-03-22',
                'time': '18:30'
            },
            {
                'title': 'Pizza Making Workshop',
                'description': 'Learn the art of pizza making from our expert pizza chef. Includes hands-on experience and dinner with your own creation.',
                'date': '2024-03-29',
                'time': '17:00'
            }
        ]
        
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults={
                    'description': event_data['description'],
                    'date': event_data['date'],
                    'time': event_data['time']
                }
            )
            if created:
                self.stdout.write(f'Created event: {event.title}')
        
        # Create gallery items
        gallery_data = [
            {
                'title': 'Margherita Pizza',
                'description': 'Our classic Margherita pizza with fresh basil and buffalo mozzarella'
            },
            {
                'title': 'Grilled Salmon',
                'description': 'Fresh Atlantic salmon with seasonal vegetables and herb butter'
            },
            {
                'title': 'Chocolate Lava Cake',
                'description': 'Warm chocolate cake with molten center and vanilla ice cream'
            },
            {
                'title': 'Restaurant Interior',
                'description': 'Our cozy dining room with warm lighting and comfortable seating'
            },
            {
                'title': 'Chef at Work',
                'description': 'Our head chef preparing a signature dish with passion and precision'
            },
            {
                'title': 'Wine Selection',
                'description': 'Our carefully curated wine list featuring premium selections'
            }
        ]
        
        for gallery_data_item in gallery_data:
            gallery_item, created = Gallery.objects.get_or_create(
                title=gallery_data_item['title'],
                defaults={
                    'description': gallery_data_item['description'],
                    'is_featured': True
                }
            )
            if created:
                self.stdout.write(f'Created gallery item: {gallery_item.title}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))
        self.stdout.write('You can now access the admin panel at /admin/')