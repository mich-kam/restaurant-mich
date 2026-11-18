from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Q
from .models import (
    Category, Dish, Chef, Testimonial, Service, 
    Reservation, Newsletter, SiteSettings, Cart, CartItem,
    Order, OrderItem, BlogPost, Event, Gallery, UserProfile
)
from .forms import (
    ReservationForm, NewsletterForm, OrderForm, UserRegistrationForm,
    UserProfileForm, ContactForm, SearchForm, ReviewForm
)

# ===== DASHBOARD MODERNE =====

from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse

def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff_or_superuser)
def dashboard_view(request):
    """Dashboard moderne pour la gestion du restaurant"""
    
    # Statistiques générales
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(status='completed').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Statistiques du jour
    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today).count()
    today_revenue = Order.objects.filter(
        created_at__date=today, 
        status='completed'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Statistiques de la semaine
    week_ago = today - timedelta(days=7)
    week_orders = Order.objects.filter(created_at__date__gte=week_ago).count()
    week_revenue = Order.objects.filter(
        created_at__date__gte=week_ago,
        status='completed'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Commandes récentes
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    
    # Plats populaires
    popular_dishes = Dish.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')[:5]
    
    # Statut des commandes
    order_status_stats = Order.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # Données pour les graphiques
    chart_data = get_chart_data()
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'today_orders': today_orders,
        'today_revenue': today_revenue,
        'week_orders': week_orders,
        'week_revenue': week_revenue,
        'recent_orders': recent_orders,
        'popular_dishes': popular_dishes,
        'order_status_stats': order_status_stats,
        'chart_data': chart_data,
        'settings': SiteSettings.get_settings(),
    }
    
    return render(request, 'restaurant/dashboard.html', context)

def get_chart_data():
    """Génère les données pour les graphiques du dashboard"""
    
    # Données des 7 derniers jours
    dates = []
    orders_data = []
    revenue_data = []
    
    for i in range(7):
        date = timezone.now().date() - timedelta(days=i)
        dates.insert(0, date.strftime('%d/%m'))
        
        # Commandes du jour
        day_orders = Order.objects.filter(created_at__date=date).count()
        orders_data.insert(0, day_orders)
        
        # Revenus du jour
        day_revenue = Order.objects.filter(
            created_at__date=date,
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        revenue_data.insert(0, float(day_revenue))
    
    # Données des catégories de plats
    category_data = Dish.objects.values('category__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    return {
        'dates': dates,
        'orders_data': orders_data,
        'revenue_data': revenue_data,
        'category_data': list(category_data),
    }

@login_required
@user_passes_test(is_staff_or_superuser)
def dashboard_api(request):
    """API pour les données en temps réel du dashboard"""
    
    # Statistiques en temps réel
    pending_orders = Order.objects.filter(status='pending').count()
    
    # Commandes récentes (dernières 5 minutes)
    five_minutes_ago = timezone.now() - timedelta(minutes=5)
    recent_activity = Order.objects.filter(
        created_at__gte=five_minutes_ago
    ).count()
    
    return JsonResponse({
        'pending_orders': pending_orders,
        'recent_activity': recent_activity,
        'timestamp': timezone.now().isoformat(),
    })

@login_required
@user_passes_test(is_staff_or_superuser)
def order_management_view(request):
    """Gestion des commandes"""
    
    orders = Order.objects.select_related('user').order_by('-created_at')
    
    # Filtres
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status_filter,
        'settings': SiteSettings.get_settings(),
    }
    
    return render(request, 'restaurant/order_management.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def update_order_status(request, order_id):
    """Mise à jour du statut d'une commande via AJAX"""
    
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id)
            new_status = request.POST.get('status')
            
            if new_status in dict(Order.STATUS_CHOICES):
                order.status = new_status
                order.save()
                
                return JsonResponse({'success': True, 'message': 'Statut mis à jour'})
            else:
                return JsonResponse({'success': False, 'message': 'Statut invalide'})
                
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Commande non trouvée'})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})

@login_required
@user_passes_test(is_staff_or_superuser)
def analytics_view(request):
    """Vue d'analyse détaillée"""
    
    # Période d'analyse
    period = request.GET.get('period', 'week')
    
    if period == 'month':
        start_date = timezone.now().date() - timedelta(days=30)
    elif period == 'week':
        start_date = timezone.now().date() - timedelta(days=7)
    else:
        start_date = timezone.now().date() - timedelta(days=1)
    
    # Statistiques détaillées
    orders_in_period = Order.objects.filter(created_at__date__gte=start_date)
    total_orders_period = orders_in_period.count()
    total_revenue_period = orders_in_period.filter(
        status='completed'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Moyenne par commande
    avg_order_value = total_revenue_period / total_orders_period if total_orders_period > 0 else 0
    
    # Top clients
    top_customers = Order.objects.filter(
        created_at__date__gte=start_date
    ).values('user__username').annotate(
        total_orders=Count('id'),
        total_spent=Sum('total_amount')
    ).order_by('-total_spent')[:10]
    
    # Heures de pointe
    peak_hours = Order.objects.filter(
        created_at__date__gte=start_date
    ).extra(
        select={'hour': "EXTRACT(hour FROM created_at)"}
    ).values('hour').annotate(
        count=Count('id')
    ).order_by('-count')[:6]
    
    context = {
        'period': period,
        'total_orders_period': total_orders_period,
        'total_revenue_period': total_revenue_period,
        'avg_order_value': avg_order_value,
        'top_customers': top_customers,
        'peak_hours': peak_hours,
        'settings': SiteSettings.get_settings(),
    }
    
    return render(request, 'restaurant/analytics.html', context)

def admin_view(request):
    """Vue pour la page d'administration"""
    if not request.user.is_authenticated:
        return redirect('restaurant:home')
    
    # Vérifier si l'utilisateur est admin (exemple simple)
    if not request.user.is_staff:
        return redirect('restaurant:dashboard')
    
    context = {
        'settings': SiteSettings.get_settings(),
        'total_orders': 156,
        'total_revenue': 2450.50,
        'total_customers': 89,
        'pending_reservations': 5,
    }
    return render(request, 'restaurant/admin.html', context)

def home(request):
    """Home page view with all restaurant data"""
    # Get popular dishes (most ordered or featured)
    popular_dishes = Dish.objects.filter(is_popular=True, is_available=True)[:6]
    if not popular_dishes.exists():
        popular_dishes = Dish.objects.filter(is_available=True)[:6]
    
    # Get upcoming events
    upcoming_events = Event.objects.filter(is_active=True, date__gte=timezone.now().date())[:3]
    
    context = {
        'settings': SiteSettings.get_settings(),
        'categories': Category.objects.all(),
        'popular_dishes': popular_dishes,
        'all_dishes': Dish.objects.filter(is_available=True)[:8],
        'chefs': Chef.objects.all()[:4],
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
        'services': Service.objects.filter(is_active=True),
        'upcoming_events': upcoming_events,
        'featured_events': Event.objects.filter(is_active=True, is_featured=True)[:3],
        'gallery': Gallery.objects.filter(is_featured=True)[:6],
    }
    return render(request, 'restaurant/home_modern.html', context)

def menu(request):
    """Menu page with all dishes and search functionality"""
    search_form = SearchForm(request.GET)
    dishes = Dish.objects.filter(is_available=True)
    
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')
        
        if query:
            dishes = dishes.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
        
        if category:
            dishes = dishes.filter(category=category)
    
    # Pagination
    dishes = dishes.order_by('name')  # Ajouter un ordre pour éviter l'avertissement
    paginator = Paginator(dishes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'settings': SiteSettings.get_settings(),
        'categories': Category.objects.all(),
        'dishes': page_obj,
        'search_form': search_form,
        'selected_category': request.GET.get('category'),
    }
    return render(request, 'restaurant/menu.html', context)

def about(request):
    """About page with chefs and services"""
    context = {
        'settings': SiteSettings.get_settings(),
        'chefs': Chef.objects.all(),
        'services': Service.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True),
    }
    return render(request, 'restaurant/about.html', context)

def contact(request):
    """Contact page with reservation form"""
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        contact_form = ContactForm(request.POST)
        
        if form.is_valid():
            reservation = form.save()
            messages.success(request, 'Reservation submitted successfully! We will contact you soon.')
            return redirect('restaurant:contact')
        elif contact_form.is_valid():
            # Handle contact form submission
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('restaurant:contact')
    else:
        form = ReservationForm()
        contact_form = ContactForm()
    
    context = {
        'settings': SiteSettings.get_settings(),
        'form': form,
        'contact_form': contact_form,
    }
    return render(request, 'restaurant/contact.html', context)

def blog(request):
    """Blog page with published posts"""
    posts = BlogPost.objects.filter(is_published=True)
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'settings': SiteSettings.get_settings(),
        'posts': page_obj,
    }
    return render(request, 'restaurant/blog.html', context)

def events(request):
    """Events page with active events"""
    events_list = Event.objects.all().order_by('-created_at')
    paginator = Paginator(events_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Données pour les filtres
    categories = [
        ('general', 'Général'),
        ('food', 'Cuisine'),
        ('music', 'Musique'),
        ('wine', 'Dégustation'),
        ('special', 'Événements spéciaux')
    ]
    
    context = {
        'settings': SiteSettings.get_settings(),
        'events': page_obj,
        'categories': categories,
        'selected_category': request.GET.get('category', ''),
        'selected_date': request.GET.get('date', ''),
        'search_query': request.GET.get('search', ''),
        'upcoming_events': Event.objects.all()[:3],  # 3 prochains événements
    }
    return render(request, 'restaurant/events.html', context)

# ===== NOUVELLES VUES POUR LES PAGES MANQUANTES =====

def blog_detail(request, slug):
    """Vue pour afficher un article de blog"""
    try:
        post = BlogPost.objects.get(slug=slug, is_published=True)
        recent_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id)[:3]
    except BlogPost.DoesNotExist:
        return redirect('restaurant:blog')
    
    context = {
        'post': post,
        'recent_posts': recent_posts,
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/blog_detail.html', context)

def event_detail(request, event_id):
    """Vue pour afficher un événement"""
    try:
        event = Event.objects.get(id=event_id, is_active=True)
    except Event.DoesNotExist:
        return redirect('restaurant:events')
    
    context = {
        'event': event,
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/event_detail.html', context)

def gallery(request):
    """Vue pour afficher la galerie"""
    galleries = Gallery.objects.all().order_by('-created_at')
    
    context = {
        'gallery_items': galleries,
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/gallery.html', context)

def register(request):
    """Vue pour l'inscription utilisateur"""
    if request.method == 'POST':
        # Logique d'inscription
        pass
    
    context = {
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/register.html', context)

def login_view(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect('restaurant:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    context = {
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/login.html', context)

@login_required
def profile(request):
    """Vue pour le profil utilisateur"""
    context = {
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/profile.html', context)

def cart_view(request):
    """Shopping cart view"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    context = {
        'settings': SiteSettings.get_settings(),
        'cart': cart,
    }
    return render(request, 'restaurant/cart.html', context)

def delivery(request):
    """Delivery page with delivery options"""
    dishes = Dish.objects.filter(is_available=True)
    
    context = {
        'settings': SiteSettings.get_settings(),
        'dishes': dishes,
    }
    return render(request, 'restaurant/delivery.html', context)

def checkout(request):
    """Vue pour le checkout"""
    context = {
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/checkout.html', context)

def order_success(request, order_id):
    """Vue pour la confirmation de commande"""
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect('restaurant:home')
    
    context = {
        'order': order,
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/order_success.html', context)

def payment(request):
    """Vue pour la page de paiement"""
    context = {
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/payment.html', context)

def payment_success(request):
    """Vue pour la page de succès de paiement"""
    context = {
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/payment_success.html', context)

def payment_cancel(request):
    """Vue pour la page d'annulation de paiement"""
    context = {
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/payment_cancel.html', context)

@require_POST
@csrf_exempt
def newsletter_subscribe(request):
    """AJAX endpoint for newsletter subscription"""
    try:
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required'})
        
        # Validate email
        validate_email(email)
        
        # Check if already subscribed
        if Newsletter.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already subscribed'})
        
        # Create newsletter subscription
        Newsletter.objects.create(email=email)
        return JsonResponse({'success': True, 'message': 'Successfully subscribed to newsletter!'})
    
    except ValidationError:
        return JsonResponse({'success': False, 'message': 'Please enter a valid email address'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})

@require_POST
@csrf_exempt
def add_to_cart(request):
    """AJAX endpoint for add to cart functionality"""
    try:
        dish_id = request.POST.get('dish_id')
        quantity = int(request.POST.get('quantity', 1))
        dish = Dish.objects.get(id=dish_id, is_available=True)
        
        # Get or create session
        if not request.session.session_key:
            request.session.create()
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        
        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            dish=dish,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True, 
            'message': f'{dish.name} ajouté au panier !',
            'cart_total': cart.get_total_price(),
            'cart_items': cart.get_total_items(),
            'cart_count': cart.get_total_items()
        })
    
    except Dish.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Dish not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred'})

@require_POST
@csrf_exempt
def update_cart(request):
    """AJAX endpoint for updating cart quantities"""
    try:
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 0))
        
        cart_item = CartItem.objects.get(id=item_id)
        
        if quantity <= 0:
            cart_item.delete()
            message = 'Item removed from cart'
        else:
            cart_item.quantity = quantity
            cart_item.save()
            message = 'Cart updated'
        
        cart = cart_item.cart
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_total': cart.get_total_price(),
            'cart_items': cart.get_total_items(),
            'cart_count': cart.get_total_items()
        })
    
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Item not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred'})

def get_cart_count(request):
    """AJAX endpoint to get cart count"""
    try:
        if not request.session.session_key:
            return JsonResponse({'success': True, 'cart_count': 0})
        
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
        if cart:
            cart_count = cart.get_total_items()
        else:
            cart_count = 0
        
        return JsonResponse({
            'success': True,
            'cart_count': cart_count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'cart_count': 0})

def reservation_success(request):
    """Reservation success page"""
    context = {
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/reservation_success.html', context)

# ===== VUES MANQUANTES =====

def blog_detail(request, slug):
    """Blog post detail view"""
    try:
        post = get_object_or_404(BlogPost, slug=slug, is_published=True)
        context = {
            'post': post,
            'settings': SiteSettings.get_settings(),
        }
        return render(request, 'restaurant/blog_detail.html', context)
    except Exception as e:
        messages.error(request, 'Article non trouvé')
        return redirect('restaurant:blog')

def event_detail(request, event_id):
    """Event detail view"""
    try:
        event = get_object_or_404(Event, id=event_id, is_active=True)
        context = {
            'event': event,
            'settings': SiteSettings.get_settings(),
        }
        return render(request, 'restaurant/event_detail.html', context)
    except Exception as e:
        messages.error(request, 'Événement non trouvé')
        return redirect('restaurant:events')

def order_success(request, order_id):
    """Order success page"""
    try:
        order = get_object_or_404(Order, id=order_id)
        context = {
            'order': order,
            'settings': SiteSettings.get_settings(),
        }
        return render(request, 'restaurant/order_success.html', context)
    except Exception as e:
        messages.error(request, 'Commande non trouvée')
        return redirect('restaurant:home')



# ===== GESTION DES IMAGES DYNAMIQUES =====

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

@csrf_exempt
def get_dynamic_image(request, model_type, instance_id):
    """Retourne une URL d'image dynamique pour un modèle"""
    try:
        if model_type == 'dish':
            instance = get_object_or_404(Dish, id=instance_id)
        elif model_type == 'event':
            instance = get_object_or_404(Event, id=instance_id)
        elif model_type == 'chef':
            instance = get_object_or_404(Chef, id=instance_id)
        elif model_type == 'blog':
            instance = get_object_or_404(BlogPost, id=instance_id)
        else:
            return JsonResponse({'error': 'Type de modèle invalide'})
        
        if instance.image and instance.image.url:
            return JsonResponse({'image_url': instance.image.url})
        else:
            # Retourner une URL de fallback dynamique
            fallback_url = get_dynamic_image_url(model_type, instance_id)
            return JsonResponse({'image_url': fallback_url})
            
    except Exception as e:
        return JsonResponse({'error': str(e)})

# ===== VUES MANQUANTES =====

def faq(request):
    """Page FAQ"""
    context = {
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/faq.html', context)

def loyalty(request):
    """Page programme de fidélité"""
    context = {
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/loyalty.html', context)

def opening_hours(request):
    """Page horaires d'ouverture"""
    context = {
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'restaurant/opening_hours.html', context)

@csrf_exempt
@require_POST
def create_delivery_order(request):
    """Créer une commande de livraison"""
    try:
        # Logique pour créer une commande de livraison
        # Cette fonction peut être étendue selon vos besoins
        return JsonResponse({
            'success': True,
            'message': 'Commande de livraison créée avec succès'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erreur lors de la création de la commande: {str(e)}'
        })

# ===== VUES DES SERVICES =====

def private_events(request):
    """Page événements privés"""
    context = {
        'settings': SiteSettings.get_settings(),
        'page_title': 'Événements Privés',
        'page_description': 'Organisez vos événements privés dans notre restaurant. Mariages, anniversaires, séminaires et plus encore.',
    }
    return render(request, 'restaurant/services/private_events.html', context)

def cooking_classes(request):
    """Page cours de cuisine"""
    context = {
        'settings': SiteSettings.get_settings(),
        'page_title': 'Cours de Cuisine',
        'page_description': 'Apprenez l\'art culinaire avec nos chefs expérimentés. Ateliers interactifs et cours personnalisés.',
    }
    return render(request, 'restaurant/services/cooking_classes.html', context)

def gift_cards(request):
    """Page cartes cadeaux"""
    context = {
        'settings': SiteSettings.get_settings(),
        'page_title': 'Cartes Cadeaux',
        'page_description': 'Offrez une expérience culinaire unique avec nos cartes cadeaux personnalisables.',
    }
    return render(request, 'restaurant/services/gift_cards.html', context)

def catering(request):
    """Page service traiteur"""
    context = {
        'settings': SiteSettings.get_settings(),
        'page_title': 'Service Traiteur',
        'page_description': 'Service traiteur sur mesure pour vos événements. Cuisine raffinée et service professionnel.',
    }
    return render(request, 'restaurant/services/catering.html', context)

def wine_tasting(request):
    """Page dégustation de vins"""
    context = {
        'settings': SiteSettings.get_settings(),
        'page_title': 'Dégustation de Vins',
        'page_description': 'Découvrez notre sélection de vins d\'exception avec nos sommeliers experts.',
    }
    return render(request, 'restaurant/services/wine_tasting.html', context)

def reservation(request):
    """Page réservation avancée"""
    context = {
        'settings': SiteSettings.get_settings(),
        'page_title': 'Réservation',
        'page_description': 'Réservez votre table en ligne 24h/24. Service rapide et confirmation instantanée.',
    }
    return render(request, 'restaurant/services/reservation.html', context)

# ===== VUES LÉGALES MANQUANTES =====

def privacy_policy(request):
    """Page politique de confidentialité"""
    context = {
        'settings': SiteSettings.get_settings(),
        'page_title': 'Politique de Confidentialité',
        'page_description': 'Notre politique de confidentialité et de protection des données personnelles.',
    }
    return render(request, 'restaurant/legal_page.html', context)

def terms_of_service(request):
    """Page conditions d'utilisation"""
    context = {
        'settings': SiteSettings.get_settings(),
        'page_title': 'Conditions d\'Utilisation',
        'page_description': 'Conditions générales d\'utilisation de notre site et services.',
    }
    return render(request, 'restaurant/legal_page.html', context)

def legal_notices(request):
    """Page mentions légales"""
    context = {
        'settings': SiteSettings.get_settings(),
        'page_title': 'Mentions Légales',
        'page_description': 'Informations légales et mentions obligatoires.',
    }
    return render(request, 'restaurant/legal_page.html', context)



