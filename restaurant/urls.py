from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    
    # User authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    
    # Shopping cart and orders
    path('cart/', views.cart_view, name='cart'),
    path('delivery/', views.delivery, name='delivery'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('reservation-success/', views.reservation_success, name='reservation_success'),
    
    # AJAX endpoints
    path('newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('dynamic-image/<str:model_type>/<int:instance_id>/', views.get_dynamic_image, name='get_dynamic_image'),
    
    # Additional pages
    path('faq/', views.faq, name='faq'),
    path('loyalty/', views.loyalty, name='loyalty'),
    path('opening-hours/', views.opening_hours, name='opening_hours'),
    path('create-delivery-order/', views.create_delivery_order, name='create_delivery_order'),
    
    # Legal pages
    path('politique-confidentialite/', views.privacy_policy, name='privacy_policy'),
    path('conditions-utilisation/', views.terms_of_service, name='terms_of_service'),
    path('mentions-legales/', views.legal_notices, name='legal_notices'),
    
    # Services pages
    path('services/private-events/', views.private_events, name='private_events'),
    path('services/cooking-classes/', views.cooking_classes, name='cooking_classes'),
    path('services/gift-cards/', views.gift_cards, name='gift_cards'),
    path('services/catering/', views.catering, name='catering'),
    path('services/wine-tasting/', views.wine_tasting, name='wine_tasting'),
    path('services/reservation/', views.reservation, name='reservation'),
    
    # ===== DASHBOARD MODERNE =====
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/api/', views.dashboard_api, name='dashboard_api'),
    path('dashboard/orders/', views.order_management_view, name='order_management'),
    path('dashboard/orders/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('dashboard/analytics/', views.analytics_view, name='analytics'),
    path('admin/', views.admin_view, name='admin'),
] 