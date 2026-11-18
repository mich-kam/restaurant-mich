// ===== FONCTIONS PRINCIPALES POUR LE SITE MODERNE =====

if (!window.__restaurantMainInit) {
    window.__restaurantMainInit = true;

    document.addEventListener('DOMContentLoaded', function () {
    // Gestion du thème (maintenant géré par theme-manager.js)
    // initThemeToggle();

    // Gestion du menu mobile
    initMobileMenu();

    // Gestion des animations
    initAnimations();

    // Gestion des notifications
    initNotifications();

    // Gestion du header au scroll
    initHeaderScroll();

    // Gestion de la newsletter
    initNewsletter();

    // Gestion des effets de hover
    initHoverEffects();

    // Gestion de l'accessibilité
    initAccessibility();

    // Écouter les changements de thème
    initThemeChangeListener();
    });
}

// ===== ÉCOUTEUR DE CHANGEMENT DE THÈME =====
function initThemeChangeListener() {
    document.addEventListener('themeChanged', function (event) {
        const theme = event.detail.theme;
        console.log('Thème changé vers:', theme);

        // Mettre à jour les composants qui dépendent du thème
        updateThemeDependentComponents(theme);
    });
}

function updateThemeDependentComponents(theme) {
    // Mettre à jour les notifications si nécessaire
    if (window.notificationManager) {
        window.notificationManager.updateTheme(theme);
    }

    // Mettre à jour les animations si nécessaire
    if (window.animationManager) {
        window.animationManager.updateTheme(theme);
    }

    // Déclencher un événement personnalisé pour les autres composants
    document.dispatchEvent(new CustomEvent('themeUpdated', {
        detail: { theme: theme }
    }));
}

// ===== GESTION DU THÈME (DÉPLACÉ VERS theme-manager.js) =====
/*
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const html = document.documentElement;

    // Récupérer le thème sauvegardé
    const savedTheme = localStorage.getItem('theme') || 'dark';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);

            // Animation de transition
            themeToggle.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                themeToggle.style.transform = 'rotate(0deg)';
            }, 300);
        });
    }
}

function updateThemeIcon(theme) {
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        if (theme === 'dark') {
            themeIcon.className = 'fas fa-sun';
            themeIcon.title = 'Passer au mode clair';
        } else {
            themeIcon.className = 'fas fa-moon';
            themeIcon.title = 'Passer au mode sombre';
        }
    }
}
*/

// ===== GESTION DU MENU MOBILE =====
function initMobileMenu() {
    const mobileToggle = document.getElementById('mobile-menu-toggle');
    const navMenu = document.getElementById('nav-menu');
    const body = document.body;

    if (mobileToggle && navMenu) {
        const setMenuOpen = isOpen => {
            navMenu.classList.toggle('active', isOpen);
            mobileToggle.classList.toggle('active', isOpen);
            mobileToggle.setAttribute('aria-expanded', String(isOpen));
            mobileToggle.setAttribute('aria-label', isOpen ? 'Fermer le menu' : 'Ouvrir le menu');
            body.classList.toggle('mobile-nav-open', isOpen);
            body.style.overflow = isOpen ? 'hidden' : '';
        };

        const closeOnDesktop = () => {
            if (window.matchMedia('(min-width: 1200px)').matches) {
                setMenuOpen(false);
            }
        };

        mobileToggle.addEventListener('click', function () {
            setMenuOpen(!navMenu.classList.contains('active'));
        });
        window.addEventListener('resize', closeOnDesktop);

        // Fermer le menu quand on clique sur un lien
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function () {
                setMenuOpen(false);
            });
        });

        // Fermer le menu quand on clique en dehors
        document.addEventListener('click', function (e) {
            if (!navMenu.contains(e.target) && !mobileToggle.contains(e.target)) {
                setMenuOpen(false);
            }
        });

        // Fermer le menu avec la touche Escape
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && navMenu.classList.contains('active')) {
                setMenuOpen(false);
            }
        });
    }
}

// ===== ANIMATIONS AU SCROLL =====
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');

                // Animation spéciale pour les éléments avec délai
                const delay = entry.target.dataset.delay;
                if (delay) {
                    setTimeout(() => {
                        entry.target.classList.add('animate-in');
                    }, parseInt(delay));
                }
            }
        });
    }, observerOptions);

    // Observer les éléments avec la classe 'animate-on-scroll'
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));

    // Animation des compteurs
    initCounters();
}

// ===== ANIMATION DES COMPTEURS =====
function initCounters() {
    const counters = document.querySelectorAll('.counter');

    const counterObserver = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.dataset.target);
                const duration = 2000; // 2 secondes
                const increment = target / (duration / 16); // 60 FPS
                let current = 0;

                const updateCounter = () => {
                    current += increment;
                    if (current < target) {
                        counter.textContent = Math.floor(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target;
                    }
                };

                updateCounter();
                counterObserver.unobserve(counter);
            }
        });
    });

    counters.forEach(counter => counterObserver.observe(counter));
}

// ===== GESTION DU HEADER AU SCROLL =====
function initHeaderScroll() {
    const header = document.querySelector('.header');
    if (!header) return;

    window.addEventListener('scroll', function () {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

// ===== GESTION DE LA NEWSLETTER =====
function initNewsletter() {
    const newsletterForm = document.querySelector('.newsletter-form-modern');

    if (newsletterForm) {
        newsletterForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const submitButton = this.querySelector('button[type="submit"]');
            const buttonMarkup = submitButton.innerHTML;
            submitButton.disabled = true;
            submitButton.classList.add('loading');
            submitButton.setAttribute('aria-busy', 'true');

            try {
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: new FormData(this),
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const data = await response.json();

                if (!response.ok || !data.success) {
                    showNotification(data.message || 'Inscription impossible. Veuillez réessayer.', 'error');
                    return;
                }

                showNotification('Merci pour votre inscription à notre newsletter !', 'success');
                this.reset();
            } catch (error) {
                showNotification('Impossible de contacter le serveur. Vérifiez votre connexion puis réessayez.', 'error');
            } finally {
                submitButton.innerHTML = buttonMarkup;
                submitButton.disabled = false;
                submitButton.classList.remove('loading');
                submitButton.removeAttribute('aria-busy');
            }
        });
    }
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// ===== EFFETS DE HOVER =====
function initHoverEffects() {
    // Effet de parallaxe sur les cartes
    const cards = document.querySelectorAll('.modern-card, .dish-card-modern');

    cards.forEach(card => {
        card.addEventListener('mousemove', function (e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', function () {
            this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
        });
    });

    // Effet de ripple sur les boutons
    const buttons = document.querySelectorAll('.reserve-btn, .btn-secondary, .newsletter-form-modern button');

    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// ===== GESTION DES NOTIFICATIONS =====
function initNotifications() {
    // Créer le conteneur de notifications s'il n'existe pas
    if (!document.querySelector('.notification-container')) {
        const notificationContainer = document.createElement('div');
        notificationContainer.className = 'notification-container';
        document.body.appendChild(notificationContainer);
    }
}

function showNotification(message, type = 'info', duration = 5000) {
    const notificationContainer = document.querySelector('.notification-container');
    const notification = document.createElement('div');

    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;

    notificationContainer.appendChild(notification);

    // Animation d'entrée
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    // Fermer la notification
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        hideNotification(notification);
    });

    // Auto-fermeture
    setTimeout(() => {
        hideNotification(notification);
    }, duration);
}

function hideNotification(notification) {
    notification.classList.remove('show');
    setTimeout(() => {
        notification.remove();
    }, 300);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// ===== ACCESSIBILITÉ =====
function initAccessibility() {
    // Gestion du focus visible
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });

    document.addEventListener('mousedown', function () {
        document.body.classList.remove('keyboard-navigation');
    });

    // Skip to main content
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Passer au contenu principal';
    skipLink.className = 'skip-link';
    document.body.insertBefore(skipLink, document.body.firstChild);

    // Ajouter l'ID au main content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.id = 'main-content';
    }
}

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

// ===== GESTION DU PANIER =====
function updateCartCount(count) {
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        cartBadge.textContent = count;

        // Animation du badge
        cartBadge.style.transform = 'scale(1.2)';
        setTimeout(() => {
            cartBadge.style.transform = 'scale(1)';
        }, 200);
    }
}

// ===== GESTION DES IMAGES LAZY LOADING =====
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// ===== GESTION DU SCROLL SMOOTH =====
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===== INITIALISATION DES FONCTIONS ADDITIONNELLES =====
document.addEventListener('DOMContentLoaded', function () {
    initLazyLoading();
    initSmoothScroll();
});

// ===== GESTION DES ERREURS =====
window.addEventListener('error', function (e) {
    console.error('Erreur JavaScript:', e.error);
    showNotification('Une erreur est survenue. Veuillez rafraîchir la page.', 'error');
});

// ===== GESTION DE LA PERFORMANCE =====
window.addEventListener('load', function () {
    // Masquer le loader si présent
    const loader = document.querySelector('.loader');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(() => {
            loader.style.display = 'none';
        }, 300);
    }

    // Optimiser les images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        if (img.complete) {
            img.classList.add('loaded');
        } else {
            img.addEventListener('load', function () {
                this.classList.add('loaded');
            });
        }
    });
});
