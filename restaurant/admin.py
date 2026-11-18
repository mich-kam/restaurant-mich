from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Category, Dish, Chef, Testimonial, Service, Reservation, Newsletter, SiteSettings,
    UserProfile, Cart, CartItem, Order, OrderItem, BlogPost, Event, Gallery
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'dish_count']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']
    
    def dish_count(self, obj):
        count = obj.dish_set.count()
        return format_html('<span style="color: #28a745; font-weight: bold;">{}</span>', count)
    dish_count.short_description = 'Nombre de plats'
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            dish_count=Count('dish')
        )

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_display', 'image_preview', 'is_popular', 'is_available', 'created_at']
    list_filter = ['category', 'is_popular', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_popular', 'is_available']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'category', 'description', 'price')
        }),
        ('Image et statut', {
            'fields': ('image', 'is_popular', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        return format_html('<span style="color: #ff6b35; font-weight: bold;">{:.2f} €</span>', obj.price)
    price_display.short_description = 'Prix'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 5px;" />', obj.image.url)
        return format_html('<span style="color: #999;">Aucune image</span>')
    image_preview.short_description = 'Image'
    
    actions = ['make_popular', 'make_available', 'make_unavailable']
    
    def make_popular(self, request, queryset):
        updated = queryset.update(is_popular=True)
        self.message_user(request, f'{updated} plat(s) marqué(s) comme populaire(s).')
    make_popular.short_description = "Marquer comme populaire"
    
    def make_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} plat(s) marqué(s) comme disponible(s).')
    make_available.short_description = "Marquer comme disponible"
    
    def make_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} plat(s) marqué(s) comme indisponible(s).')
    make_unavailable.short_description = "Marquer comme indisponible"

@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'experience_years', 'image_preview']
    list_filter = ['position', 'experience_years']
    search_fields = ['name', 'position', 'specialties']
    list_editable = ['position', 'experience_years']
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('name', 'position', 'bio', 'image')
        }),
        ('Expérience', {
            'fields': ('experience_years', 'specialties')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 50%;" />', obj.image.url)
        return format_html('<span style="color: #999;">Aucune photo</span>')
    image_preview.short_description = 'Photo'
    
    actions = ['activate_chefs', 'deactivate_chefs']
    
    def activate_chefs(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} chef(s) activé(s).')
    activate_chefs.short_description = "Activer les chefs sélectionnés"
    
    def deactivate_chefs(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} chef(s) désactivé(s).')
    deactivate_chefs.short_description = "Désactiver les chefs sélectionnés"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating_stars', 'review_preview', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['customer_name', 'review']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations client', {
            'fields': ('customer_name', 'customer_image')
        }),
        ('Avis', {
            'fields': ('rating', 'review')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: #ffc107; font-size: 16px;">{}</span>', stars)
    rating_stars.short_description = 'Note'
    
    def review_preview(self, obj):
        return obj.review[:100] + '...' if len(obj.review) > 100 else obj.review
    review_preview.short_description = 'Aperçu de l\'avis'
    
    actions = ['approve_testimonials', 'reject_testimonials']
    
    def approve_testimonials(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} avis approuvé(s).')
    approve_testimonials.short_description = "Approuver les avis sélectionnés"
    
    def reject_testimonials(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} avis rejeté(s).')
    reject_testimonials.short_description = "Rejeter les avis sélectionnés"

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'description_preview', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['name']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'description', 'icon')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )
    
    def description_preview(self, obj):
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
    description_preview.short_description = 'Description'
    
    actions = ['activate_services', 'deactivate_services']
    
    def activate_services(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} service(s) activé(s).')
    activate_services.short_description = "Activer les services sélectionnés"
    
    def deactivate_services(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} service(s) désactivé(s).')
    deactivate_services.short_description = "Désactiver les services sélectionnés"

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date', 'time', 'guests', 'status', 'created_at']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['name', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
    ordering = ['-date', '-time']
    
    fieldsets = (
        ('Informations client', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Réservation', {
            'fields': ('date', 'time', 'guests', 'special_requests')
        }),
        ('Statut', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    

    
    actions = ['confirm_reservations', 'cancel_reservations', 'mark_completed']
    
    def confirm_reservations(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} réservation(s) confirmée(s).')
    confirm_reservations.short_description = "Confirmer les réservations sélectionnées"
    
    def cancel_reservations(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} réservation(s) annulée(s).')
    cancel_reservations.short_description = "Annuler les réservations sélectionnées"
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} réservation(s) marquée(s) comme terminée(s).')
    mark_completed.short_description = "Marquer comme terminées"

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['is_active']
    readonly_fields = ['subscribed_at']

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone', 'email', 'hero_image_preview']
    readonly_fields = ['hero_image_preview', 'menu_hero_preview', 'events_hero_preview', 
                      'delivery_hero_preview', 'faq_hero_preview', 'loyalty_hero_preview',
                      'opening_hours_hero_preview', 'about_hero_preview', 'contact_hero_preview']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('site_name', 'phone', 'email', 'address')
        }),
        ('Section Hero principale', {
            'fields': ('hero_title', 'hero_description', 'hero_image', 'hero_image_preview')
        }),
        ('Images Hero par page', {
            'fields': (
                ('menu_hero_image', 'menu_hero_preview'),
                ('events_hero_image', 'events_hero_preview'),
                ('delivery_hero_image', 'delivery_hero_preview'),
                ('faq_hero_image', 'faq_hero_preview'),
                ('loyalty_hero_image', 'loyalty_hero_preview'),
                ('opening_hours_hero_image', 'opening_hours_hero_preview'),
                ('about_hero_image', 'about_hero_preview'),
                ('contact_hero_image', 'contact_hero_preview'),
            ),
            'description': 'Images Hero spécifiques pour chaque page du site. Si aucune image n\'est définie, une image de fallback sera utilisée.'
        }),
        ('Section À propos', {
            'fields': ('about_title', 'about_description')
        }),
        ('Section Réservation', {
            'fields': ('reservation_title', 'reservation_description')
        }),
        ('Section Application Mobile', {
            'fields': ('mobile_app_title', 'mobile_app_description')
        }),
        ('Réseaux sociaux', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one site settings instance
        return not SiteSettings.objects.exists()
    
    def hero_image_preview(self, obj):
        if obj.hero_image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 200px; border-radius: 8px; border: 2px solid #ddd;" />', obj.hero_image.url)
        return format_html('<span style="color: #999; font-style: italic;">Aucune image (fallback activé)</span>')
    hero_image_preview.short_description = 'Aperçu Hero principal'
    
    def menu_hero_preview(self, obj):
        if obj.menu_hero_image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 150px; border-radius: 6px; border: 1px solid #ddd;" />', obj.menu_hero_image.url)
        return format_html('<span style="color: #999; font-size: 12px;">Fallback</span>')
    menu_hero_preview.short_description = 'Aperçu'
    
    def events_hero_preview(self, obj):
        if obj.events_hero_image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 150px; border-radius: 6px; border: 1px solid #ddd;" />', obj.events_hero_image.url)
        return format_html('<span style="color: #999; font-size: 12px;">Fallback</span>')
    events_hero_preview.short_description = 'Aperçu'
    
    def delivery_hero_preview(self, obj):
        if obj.delivery_hero_image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 150px; border-radius: 6px; border: 1px solid #ddd;" />', obj.delivery_hero_image.url)
        return format_html('<span style="color: #999; font-size: 12px;">Fallback</span>')
    delivery_hero_preview.short_description = 'Aperçu'
    
    def faq_hero_preview(self, obj):
        if obj.faq_hero_image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 150px; border-radius: 6px; border: 1px solid #ddd;" />', obj.faq_hero_image.url)
        return format_html('<span style="color: #999; font-size: 12px;">Fallback</span>')
    faq_hero_preview.short_description = 'Aperçu'
    
    def loyalty_hero_preview(self, obj):
        if obj.loyalty_hero_image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 150px; border-radius: 6px; border: 1px solid #ddd;" />', obj.loyalty_hero_image.url)
        return format_html('<span style="color: #999; font-size: 12px;">Fallback</span>')
    loyalty_hero_preview.short_description = 'Aperçu'
    
    def opening_hours_hero_preview(self, obj):
        if obj.opening_hours_hero_image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 150px; border-radius: 6px; border: 1px solid #ddd;" />', obj.opening_hours_hero_image.url)
        return format_html('<span style="color: #999; font-size: 12px;">Fallback</span>')
    opening_hours_hero_preview.short_description = 'Aperçu'
    
    def about_hero_preview(self, obj):
        if obj.about_hero_image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 150px; border-radius: 6px; border: 1px solid #ddd;" />', obj.about_hero_image.url)
        return format_html('<span style="color: #999; font-size: 12px;">Fallback</span>')
    about_hero_preview.short_description = 'Aperçu'
    
    def contact_hero_preview(self, obj):
        if obj.contact_hero_image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 150px; border-radius: 6px; border: 1px solid #ddd;" />', obj.contact_hero_image.url)
        return format_html('<span style="color: #999; font-size: 12px;">Fallback</span>')
    contact_hero_preview.short_description = 'Aperçu'

# Advanced Models Admin

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    filter_horizontal = ['favorite_dishes']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'get_total_price', 'get_total_items', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'dish', 'quantity', 'get_total_price', 'added_at']
    list_filter = ['added_at']
    search_fields = ['dish__name', 'cart__session_key']
    readonly_fields = ['added_at']
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'order_type', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'order_type', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations client', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Détails de la commande', {
            'fields': ('order_type', 'delivery_address', 'special_instructions', 'total_amount')
        }),
        ('Statut', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    

    
    actions = ['confirm_orders', 'mark_preparing', 'mark_ready', 'mark_delivered', 'cancel_orders']
    
    def confirm_orders(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} commande(s) confirmée(s).')
    confirm_orders.short_description = "Confirmer les commandes sélectionnées"
    
    def mark_preparing(self, request, queryset):
        updated = queryset.update(status='preparing')
        self.message_user(request, f'{updated} commande(s) en préparation.')
    mark_preparing.short_description = "Marquer en préparation"
    
    def mark_ready(self, request, queryset):
        updated = queryset.update(status='ready')
        self.message_user(request, f'{updated} commande(s) prête(s).')
    mark_ready.short_description = "Marquer comme prêtes"
    
    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} commande(s) livrée(s).')
    mark_delivered.short_description = "Marquer comme livrées"
    
    def cancel_orders(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} commande(s) annulée(s).')
    cancel_orders.short_description = "Annuler les commandes sélectionnées"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'dish', 'quantity', 'price']
    list_filter = ['order__status']
    search_fields = ['dish__name', 'order__customer_name']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'is_active']
    list_filter = ['is_active', 'date']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    date_hierarchy = 'date'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    readonly_fields = ['created_at']
