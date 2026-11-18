(function () {
if (window.__restaurantHeaderEffectsLoaded) {
    return;
}
window.__restaurantHeaderEffectsLoaded = true;

// ===== EFFETS VISUELS AVANCÉS POUR LE HEADER =====

document.addEventListener('DOMContentLoaded', function () {
    initRippleEffects();
    initParallaxEffects();
    initLogoAnimations();
    initNavigationEffects();
    initCartBadgeEffects();
});

// ===== EFFETS DE RIPPLE =====
function initRippleEffects() {
    const rippleElements = document.querySelectorAll('.reserve-btn, .btn-secondary, .cart-link, .user-link');

    rippleElements.forEach(element => {
        element.addEventListener('click', function (e) {
            createRipple(e, this);
        });
    });
}

function createRipple(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
        border-radius: 50%;
        transform: scale(0);
        animation: rippleExpand 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        pointer-events: none;
        z-index: 1000;
    `;

    element.style.position = 'relative';
    element.appendChild(ripple);

    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// ===== EFFETS DE PARALLAXE =====
function initParallaxEffects() {
    const navLinks = document.querySelectorAll('.nav-menu a');

    navLinks.forEach(link => {
        link.addEventListener('mousemove', function (e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            this.style.transform = `
                translateY(-2px) 
                translateZ(10px) 
                rotateX(${rotateX}deg) 
                rotateY(${rotateY}deg)
            `;
        });

        link.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0) translateZ(0) rotateX(0) rotateY(0)';
        });
    });
}

// ===== ANIMATIONS DU LOGO =====
function initLogoAnimations() {
    const logoContainer = document.querySelector('.logo-container');
    const logoIcon = document.querySelector('.logo-icon');

    if (logoContainer && logoIcon) {
        // Animation d'entrée
        logoContainer.style.opacity = '0';
        logoContainer.style.transform = 'translateY(-20px) scale(0.9)';

        setTimeout(() => {
            logoContainer.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
            logoContainer.style.opacity = '1';
            logoContainer.style.transform = 'translateY(0) scale(1)';
        }, 200);

        // Effet de brillance au hover
        logoContainer.addEventListener('mouseenter', function () {
            createLogoShine(this);
        });

        // Animation de l'icône
        logoIcon.addEventListener('mouseenter', function () {
            this.style.animation = 'logoIconBounce 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        });

        logoIcon.addEventListener('animationend', function () {
            this.style.animation = '';
        });
    }
}

function createLogoShine(container) {
    const shine = document.createElement('div');
    shine.style.cssText = `
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.1) 40%,
            rgba(255, 255, 255, 0.3) 50%,
            rgba(255, 255, 255, 0.1) 60%,
            transparent 70%
        );
        transform: translateX(-100%) translateY(-100%) rotate(45deg);
        animation: logoShine 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        pointer-events: none;
        z-index: 1;
    `;

    container.appendChild(shine);

    setTimeout(() => {
        shine.remove();
    }, 600);
}

// ===== EFFETS DE NAVIGATION =====
function initNavigationEffects() {
    const navItems = document.querySelectorAll('.nav-menu li');

    navItems.forEach((item, index) => {
        // Animation d'entrée avec délai
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';

        setTimeout(() => {
            item.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, 300 + (index * 100));

        // Effet de hover avancé
        const link = item.querySelector('a');
        if (link) {
            link.addEventListener('mouseenter', function () {
                this.style.transform = 'translateY(-3px) translateZ(15px) rotateX(8deg)';
                this.style.textShadow = '0 4px 8px rgba(255, 107, 53, 0.3)';
            });

            link.addEventListener('mouseleave', function () {
                this.style.transform = 'translateY(0) translateZ(0) rotateX(0)';
                this.style.textShadow = 'none';
            });
        }
    });
}

// ===== EFFETS DU BADGE PANIER =====
function initCartBadgeEffects() {
    const cartBadge = document.querySelector('.cart-badge');
    const cartLink = document.querySelector('.cart-link');

    if (cartBadge && cartLink) {
        // Animation d'entrée
        cartBadge.style.transform = 'scale(0)';
        setTimeout(() => {
            cartBadge.style.transition = 'transform 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
            cartBadge.style.transform = 'scale(1)';
        }, 1000);

        // Effet au hover
        cartLink.addEventListener('mouseenter', function () {
            cartBadge.style.animation = 'cartBadgeHover 0.3s ease-in-out';
        });

        cartLink.addEventListener('mouseleave', function () {
            cartBadge.style.animation = 'cartPulse 2s ease-in-out infinite';
        });

        // Effet au clic
        cartLink.addEventListener('click', function () {
            cartBadge.style.animation = 'cartBadgeClick 0.4s ease-in-out';
            setTimeout(() => {
                cartBadge.style.animation = 'cartPulse 2s ease-in-out infinite';
            }, 400);
        });
    }
}

// ===== ANIMATIONS CSS DYNAMIQUES =====
let headerEffectsStyles = document.getElementById('header-effects-styles');
if (!headerEffectsStyles) {
    headerEffectsStyles = document.createElement('style');
    headerEffectsStyles.id = 'header-effects-styles';
    headerEffectsStyles.textContent = `
        @keyframes rippleExpand {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        @keyframes logoIconBounce {
            0%, 100% {
                transform: scale(1) rotate(0deg);
            }
            25% {
                transform: scale(1.1) rotate(2deg);
            }
            50% {
                transform: scale(0.95) rotate(-1deg);
            }
            75% {
                transform: scale(1.05) rotate(1deg);
            }
        }
        
        @keyframes logoShine {
            0% {
                transform: translateX(-100%) translateY(-100%) rotate(45deg);
            }
            100% {
                transform: translateX(100%) translateY(100%) rotate(45deg);
            }
        }
        
        @keyframes cartBadgeHover {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.3);
            }
        }
        
        @keyframes cartBadgeClick {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(0.8);
            }
        }
        
        @keyframes navItemSlideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes mobileMenuSlideIn {
            from {
                transform: translateX(-100%);
            }
            to {
                transform: translateX(0);
            }
        }
        
        @keyframes mobileMenuSlideOut {
            from {
                transform: translateX(0);
            }
            to {
                transform: translateX(-100%);
            }
        }
    `;

    if (document.head) {
        document.head.appendChild(headerEffectsStyles);
    }
}

// ===== EFFETS DE SCROLL =====
function initScrollEffects() {
    const header = document.querySelector('.header');
    if (!header) return;

    window.addEventListener('scroll', function () {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        // Effet de transparence
        if (scrollTop > 50) {
            header.classList.add('scrolled');
            header.style.backdropFilter = 'blur(25px) saturate(200%)';
        } else {
            header.classList.remove('scrolled');
            header.style.backdropFilter = 'blur(20px) saturate(180%)';
        }
    });
}

// ===== EFFETS DE PERFORMANCE =====
function optimizePerformance() {
    // Utiliser requestAnimationFrame pour les animations fluides
    const smoothScroll = (target, duration) => {
        const start = window.pageYOffset;
        const distance = target - start;
        let startTime = null;

        function animation(currentTime) {
            if (startTime === null) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const run = ease(timeElapsed, start, distance, duration);
            window.scrollTo(0, run);
            if (timeElapsed < duration) requestAnimationFrame(animation);
        }

        function ease(t, b, c, d) {
            t /= d / 2;
            if (t < 1) return c / 2 * t * t + b;
            t--;
            return -c / 2 * (t * (t - 2) - 1) + b;
        }

        requestAnimationFrame(animation);
    };

    // Optimiser les événements de scroll
    let ticking = false;

    function updateOnScroll() {
        // Mettre à jour les effets de scroll
        ticking = false;
    }

    window.addEventListener('scroll', function () {
        if (!ticking) {
            requestAnimationFrame(updateOnScroll);
            ticking = true;
        }
    });
}

// ===== INITIALISATION =====
document.addEventListener('DOMContentLoaded', function () {
    initScrollEffects();
    optimizePerformance();

    // Ajouter des classes pour les animations d'entrée
    setTimeout(() => {
        document.body.classList.add('header-loaded');
    }, 100);
});

// ===== UTILITAIRES =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function () {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ===== GESTION DES ERREURS =====
window.addEventListener('error', function (e) {
    console.error('Erreur dans les effets du header:', e.error);
});

// ===== EXPORT DES FONCTIONS =====
window.HeaderEffects = {
    initRippleEffects,
    initParallaxEffects,
    initLogoAnimations,
    initNavigationEffects,
    initCartBadgeEffects,
    createRipple,
    createLogoShine
};
})();
