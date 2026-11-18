(function () {
    if (window.__restaurantServiceLinksLoaded) {
        return;
    }
    window.__restaurantServiceLinksLoaded = true;

    /**
     * Service Links Manager - Effets modernes pour les liens de services
     * Gère les animations, interactions et analytics des liens de services
     */

    class ServiceLinksManager {
    constructor() {
        this.serviceLinks = document.querySelectorAll('.service-link');
        this.analytics = {};
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupIntersectionObserver();
        this.setupAnalytics();
        this.addRippleEffect();
    }

    setupEventListeners() {
        this.serviceLinks.forEach(link => {
            // Effet de hover avec délai
            link.addEventListener('mouseenter', (e) => this.handleHover(e));
            link.addEventListener('mouseleave', (e) => this.handleLeave(e));

            // Effet de clic avec ripple
            link.addEventListener('click', (e) => this.handleClick(e));

            // Effet de focus pour l'accessibilité
            link.addEventListener('focus', (e) => this.handleFocus(e));
            link.addEventListener('blur', (e) => this.handleBlur(e));

            // Effet de toucher pour mobile
            link.addEventListener('touchstart', (e) => this.handleTouch(e));
        });
    }

    setupIntersectionObserver() {
        const options = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('service-visible');
                    this.trackServiceView(entry.target.dataset.service);
                }
            });
        }, options);

        this.serviceLinks.forEach(link => {
            observer.observe(link);
        });
    }

    handleHover(e) {
        const link = e.currentTarget;
        const icon = link.querySelector('i');
        const text = link.querySelector('.service-text');

        // Animation de l'icône
        icon.style.transform = 'scale(1.2) rotate(8deg)';
        icon.style.filter = 'drop-shadow(0 4px 8px rgba(255, 107, 53, 0.6))';

        // Animation du texte
        text.style.transform = 'translateX(5px)';

        // Effet de brillance
        this.addShineEffect(link);

        // Son subtil (optionnel)
        this.playHoverSound();
    }

    handleLeave(e) {
        const link = e.currentTarget;
        const icon = link.querySelector('i');
        const text = link.querySelector('.service-text');

        // Reset des animations
        icon.style.transform = '';
        icon.style.filter = '';
        text.style.transform = '';

        // Suppression de l'effet de brillance
        this.removeShineEffect(link);
    }

    handleClick(e) {
        const link = e.currentTarget;
        const service = link.dataset.service;

        // Effet de ripple
        this.createRippleEffect(e);

        // Animation de clic
        link.style.transform = 'scale(0.95)';
        setTimeout(() => {
            link.style.transform = '';
        }, 150);

        // Tracking analytics
        this.trackServiceClick(service);

        // Son de clic (optionnel)
        this.playClickSound();

        // Transition fluide vers la page
        this.smoothTransition(link.href);
    }

    handleFocus(e) {
        const link = e.currentTarget;
        link.classList.add('service-focused');

        // Animation d'accessibilité
        link.style.outline = '3px solid #ff6b35';
        link.style.outlineOffset = '2px';
    }

    handleBlur(e) {
        const link = e.currentTarget;
        link.classList.remove('service-focused');
        link.style.outline = '';
        link.style.outlineOffset = '';
    }

    handleTouch(e) {
        const link = e.currentTarget;
        link.classList.add('service-touched');

        setTimeout(() => {
            link.classList.remove('service-touched');
        }, 300);
    }

    addShineEffect(link) {
        const shine = document.createElement('div');
        shine.className = 'service-shine';
        shine.style.cssText = `
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            transition: left 0.6s ease;
            pointer-events: none;
            z-index: 1;
        `;

        link.appendChild(shine);

        // Animation de la brillance
        requestAnimationFrame(() => {
            shine.style.left = '100%';
        });

        // Suppression après animation
        setTimeout(() => {
            if (shine.parentNode) {
                shine.parentNode.removeChild(shine);
            }
        }, 600);
    }

    removeShineEffect(link) {
        const shine = link.querySelector('.service-shine');
        if (shine) {
            shine.remove();
        }
    }

    createRippleEffect(e) {
        const link = e.currentTarget;
        const ripple = document.createElement('span');
        const rect = link.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: radial-gradient(circle, rgba(255, 107, 53, 0.3) 0%, transparent 70%);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
            z-index: 2;
        `;

        link.appendChild(ripple);

        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }

    addRippleEffect() {
        // Ajout de la CSS pour l'animation ripple
        let rippleStyles = document.getElementById('ripple-styles');
        if (!rippleStyles) {
            rippleStyles = document.createElement('style');
            rippleStyles.id = 'ripple-styles';
            rippleStyles.textContent = `
                @keyframes ripple-animation {
                    to {
                        transform: scale(2);
                        opacity: 0;
                    }
                }
                
                .service-link {
                    position: relative;
                    overflow: hidden;
                }
                
                .service-visible {
                    animation: serviceFadeIn 0.8s ease-out forwards;
                }
                
                @keyframes serviceFadeIn {
                    from {
                        opacity: 0;
                        transform: translateY(20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                .service-focused {
                    box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.3);
                }
                
                .service-touched {
                    transform: scale(0.98);
                }
            `;
            if (document.head) {
                document.head.appendChild(rippleStyles);
            }
        }
    }

    smoothTransition(url) {
        // Effet de transition fluide
        document.body.style.opacity = '0.8';
        document.body.style.transition = 'opacity 0.3s ease';

        setTimeout(() => {
            window.location.href = url;
        }, 300);
    }

    // Analytics et tracking
    setupAnalytics() {
        this.analytics = {
            views: {},
            clicks: {},
            hoverTime: {}
        };
    }

    trackServiceView(service) {
        if (!this.analytics.views[service]) {
            this.analytics.views[service] = 0;
        }
        this.analytics.views[service]++;

        // Envoi des données analytics (optionnel)
        this.sendAnalytics('view', service);
    }

    trackServiceClick(service) {
        if (!this.analytics.clicks[service]) {
            this.analytics.clicks[service] = 0;
        }
        this.analytics.clicks[service]++;

        // Envoi des données analytics (optionnel)
        this.sendAnalytics('click', service);
    }

    sendAnalytics(action, service) {
        // Envoi des données vers votre système d'analytics
        // Exemple avec Google Analytics ou un système personnalisé
        if (typeof gtag !== 'undefined') {
            gtag('event', action, {
                'event_category': 'service_interaction',
                'event_label': service,
                'value': 1
            });
        }

        // Ou envoi vers votre API
        fetch('/api/analytics/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({
                action: action,
                service: service,
                timestamp: new Date().toISOString()
            })
        }).catch(error => {
            console.log('Analytics error:', error);
        });
    }

    getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }

    // Effets sonores (optionnels)
    playHoverSound() {
        // Son subtil au hover (peut être désactivé)
        if (this.shouldPlaySounds()) {
            // Implémentation du son
        }
    }

    playClickSound() {
        // Son de clic (peut être désactivé)
        if (this.shouldPlaySounds()) {
            // Implémentation du son
        }
    }

    shouldPlaySounds() {
        // Vérifier les préférences utilisateur
        return !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    // Méthodes utilitaires
    getAnalytics() {
        return this.analytics;
    }

    resetAnalytics() {
        this.analytics = {
            views: {},
            clicks: {},
            hoverTime: {}
        };
    }
    }

    // Initialisation quand le DOM est prêt
    document.addEventListener('DOMContentLoaded', () => {
        new ServiceLinksManager();
    });

    // Export pour utilisation dans d'autres modules
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = ServiceLinksManager;
    }
})();
