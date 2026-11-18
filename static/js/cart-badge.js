// ===== GESTION DU BADGE CART =====

class CartBadgeManager {
    constructor() {
        this.badge = document.querySelector('.cart-badge');
        this.init();
    }

    init() {
        if (!this.badge) return;

        // Initialiser l'état du badge
        this.updateBadgeState();

        // Observer les changements du contenu du badge
        this.observeBadgeChanges();

        // Écouter les événements de mise à jour du panier
        this.listenToCartUpdates();
    }

    updateBadgeState() {
        const content = this.badge.textContent.trim();
        const count = parseInt(content) || 0;

        // Retirer toutes les classes
        this.badge.classList.remove('has-items', 'empty');

        if (count > 0) {
            this.badge.classList.add('has-items');
            this.badge.style.opacity = '1';
        } else {
            this.badge.classList.add('empty');
            this.badge.style.opacity = '0.8';
        }
    }

    observeBadgeChanges() {
        // Observer les changements du contenu
        const observer = new MutationObserver(() => {
            this.updateBadgeState();
        });

        observer.observe(this.badge, {
            childList: true,
            characterData: true,
            subtree: true
        });
    }

    listenToCartUpdates() {
        // Écouter les événements personnalisés de mise à jour du panier
        document.addEventListener('cartUpdated', (event) => {
            const { count } = event.detail;
            this.updateBadgeCount(count);
        });

        // Écouter les clics sur les boutons d'ajout au panier
        document.addEventListener('click', (event) => {
            if (event.target.matches('.add-to-cart, .add-to-cart-btn')) {
                this.animateBadge();
            }
        });
    }

    updateBadgeCount(count) {
        if (!this.badge) return;

        this.badge.textContent = count.toString();
        this.updateBadgeState();

        // Animation spéciale pour l'ajout d'articles
        if (count > 0) {
            this.animateBadge();
        }
    }

    animateBadge() {
        if (!this.badge) return;

        // Animation de bounce
        this.badge.style.transform = 'scale(1.3)';
        this.badge.style.transition = 'transform 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55)';

        setTimeout(() => {
            this.badge.style.transform = 'scale(1)';
        }, 300);

        // Retirer la transition après l'animation
        setTimeout(() => {
            this.badge.style.transition = '';
        }, 600);
    }

    // Méthode pour forcer la mise à jour
    forceUpdate() {
        this.updateBadgeState();
    }
}

// ===== INITIALISATION =====

document.addEventListener('DOMContentLoaded', () => {
    // Initialiser le gestionnaire de badge
    window.cartBadgeManager = new CartBadgeManager();

    // Fonction globale pour mettre à jour le badge
    window.updateCartBadge = (count) => {
        if (window.cartBadgeManager) {
            window.cartBadgeManager.updateBadgeCount(count);
        }
    };

    // Fonction pour déclencher l'animation
    window.animateCartBadge = () => {
        if (window.cartBadgeManager) {
            window.cartBadgeManager.animateBadge();
        }
    };
});

// ===== UTILITAIRES =====

// Fonction pour simuler l'ajout d'articles (pour les tests)
function simulateAddToCart() {
    const badge = document.querySelector('.cart-badge');
    if (badge) {
        const currentCount = parseInt(badge.textContent) || 0;
        const newCount = currentCount + 1;

        // Déclencher l'événement personnalisé
        document.dispatchEvent(new CustomEvent('cartUpdated', {
            detail: { count: newCount }
        }));
    }
}

// Fonction pour réinitialiser le panier (pour les tests)
function resetCart() {
    document.dispatchEvent(new CustomEvent('cartUpdated', {
        detail: { count: 0 }
    }));
}

// Exposer les fonctions de test globalement
window.simulateAddToCart = simulateAddToCart;
window.resetCart = resetCart;
