from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='dishes/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')
    is_popular = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Dishes"
    
    def __str__(self):
        return self.name

class Chef(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='chefs/')
    experience_years = models.PositiveIntegerField(default=0)
    specialties = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Chefs"
    
    def __str__(self):
        return f"{self.name} - {self.position}"

class Testimonial(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_image = models.ImageField(upload_to='testimonials/', blank=True)
    review = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"{self.customer_name} - {self.rating} stars"

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.name

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Reservations"
    
    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Newsletters"
    
    def __str__(self):
        return self.email

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default="Bites")
    hero_title = models.CharField(max_length=200, default="We Serve The Test You Love 😋")
    hero_description = models.TextField(default="Discover the most delicious and authentic flavors from around the world.")
    hero_image = models.ImageField(upload_to='site/', blank=True)
    
    # Images Hero dynamiques pour chaque page
    menu_hero_image = models.ImageField(upload_to='site/hero/', blank=True, verbose_name="Image Hero Menu")
    events_hero_image = models.ImageField(upload_to='site/hero/', blank=True, verbose_name="Image Hero Événements")
    delivery_hero_image = models.ImageField(upload_to='site/hero/', blank=True, verbose_name="Image Hero Livraison")
    faq_hero_image = models.ImageField(upload_to='site/hero/', blank=True, verbose_name="Image Hero FAQ")
    loyalty_hero_image = models.ImageField(upload_to='site/hero/', blank=True, verbose_name="Image Hero Fidélité")
    opening_hours_hero_image = models.ImageField(upload_to='site/hero/', blank=True, verbose_name="Image Hero Horaires")
    about_hero_image = models.ImageField(upload_to='site/hero/', blank=True, verbose_name="Image Hero À propos")
    contact_hero_image = models.ImageField(upload_to='site/hero/', blank=True, verbose_name="Image Hero Contact")
    
    about_title = models.CharField(max_length=200, default="We Are More Than Multiple Survice")
    about_description = models.TextField(blank=True)
    reservation_title = models.CharField(max_length=200, default="Do You Have Any Dinner Plan Today? Reserve Your Table")
    reservation_description = models.TextField(blank=True)
    mobile_app_title = models.CharField(max_length=200, default="Never Feel Hungry! Download Our Mobile App Enjoy Delicious Foods")
    mobile_app_description = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
    
    def get_hero_image(self, page_type='home'):
        """Récupère l'image Hero pour une page spécifique avec fallback"""
        image_mapping = {
            'home': self.hero_image,
            'menu': self.menu_hero_image,
            'events': self.events_hero_image,
            'delivery': self.delivery_hero_image,
            'faq': self.faq_hero_image,
            'loyalty': self.loyalty_hero_image,
            'opening_hours': self.opening_hours_hero_image,
            'about': self.about_hero_image,
            'contact': self.contact_hero_image,
        }
        
        # Retourne l'image spécifique à la page, sinon l'image par défaut
        return image_mapping.get(page_type, self.hero_image)
    
    def get_hero_image_url(self, page_type='home'):
        """Récupère l'URL de l'image Hero avec fallback vers Unsplash"""
        hero_image = self.get_hero_image(page_type)
        
        if hero_image and hero_image.url:
            return hero_image.url
        
        # Fallback vers des images Unsplash par page
        fallback_images = {
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
        
        return fallback_images.get(page_type, fallback_images['home'])

# Advanced Models for Enhanced Functionality

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    favorite_dishes = models.ManyToManyField(Dish, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Cart(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.session_key}"
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity}x {self.dish.name}"
    
    def get_total_price(self):
        return self.dish.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    ORDER_TYPE_CHOICES = [
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
        ('dine_in', 'Dine In'),
    ]
    
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='pickup')
    delivery_address = models.TextField(blank=True)
    special_instructions = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x {self.dish.name}"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    image = models.ImageField(upload_to='blog/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('degustation', 'Dégustation'),
        ('soiree', 'Soirée thématique'),
        ('cours', 'Cours de cuisine'),
        ('anniversaire', 'Anniversaire'),
        ('mariage', 'Mariage'),
        ('corporate', 'Événement corporate'),
        ('autre', 'Autre'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='autre')
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200, default='Notre restaurant')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Prix par personne (optionnel)')
    max_capacity = models.PositiveIntegerField(null=True, blank=True, help_text='Nombre maximum de participants')
    current_bookings = models.PositiveIntegerField(default=0, help_text='Nombre de réservations actuelles')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text='Mettre en avant sur la page d\'accueil')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.title} - {self.date}"
    
    @property
    def is_full(self):
        """Vérifie si l'événement est complet"""
        if self.max_capacity:
            return self.current_bookings >= self.max_capacity
        return False
    
    @property
    def available_spots(self):
        """Retourne le nombre de places disponibles"""
        if self.max_capacity:
            return max(0, self.max_capacity - self.current_bookings)
        return None
    
    @property
    def booking_percentage(self):
        """Retourne le pourcentage de réservation"""
        if self.max_capacity and self.max_capacity > 0:
            return (self.current_bookings / self.max_capacity) * 100
        return 0

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Gallery"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
