// ===== GESTIONNAIRE DE THÈME MODERNE =====

class ThemeManager {
    constructor() {
        this.themeToggle = document.getElementById('theme-toggle');
        this.themeIcon = document.getElementById('theme-icon');
        this.html = document.documentElement;
        this.currentTheme = 'dark';
        this.isTransitioning = false;

        this.init();
    }

    init() {
        this.loadSavedTheme();
        this.detectSystemPreference();

        this.initEvents();

        this.applyTheme(this.currentTheme);

        this.observeSystemPreference();
    }

    detectSystemPreference() {
        if (!this.getStoredTheme()) {
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            this.currentTheme = prefersDark ? 'dark' : 'light';
        }
    }

    getStoredTheme() {
        try {
            const savedTheme = localStorage.getItem('theme');
            return savedTheme === 'dark' || savedTheme === 'light' ? savedTheme : null;
        } catch (error) {
            return null;
        }
    }

    loadSavedTheme() {
        const savedTheme = this.getStoredTheme();
        if (savedTheme) {
            this.currentTheme = savedTheme;
        }
    }

    initEvents() {
        if (this.themeToggle) {
            // Gestionnaire de clic principal
            this.themeToggle.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleTheme();
            });

            // Gestionnaire de clavier pour l'accessibilité
            this.themeToggle.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggleTheme();
                }
            });

            // Gestionnaire de focus pour l'accessibilité
            this.themeToggle.addEventListener('focus', () => {
                this.themeToggle.setAttribute('aria-pressed', this.currentTheme === 'dark');
            });
        }
    }

    toggleTheme() {
        if (this.isTransitioning) return;

        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.switchTheme(newTheme);
    }

    switchTheme(newTheme) {
        this.isTransitioning = true;

        // Animation de transition
        this.animateThemeTransition(() => {
            this.applyTheme(newTheme);
            this.currentTheme = newTheme;
            this.saveTheme(newTheme);
            this.isTransitioning = false;
        });
    }

    applyTheme(theme) {
        // Appliquer le thème au HTML
        this.html.setAttribute('data-theme', theme);

        // Mettre à jour les métadonnées de navigateur et l'icône
        this.updateColorScheme(theme);
        this.updateIcon(theme);

        // Mettre à jour les attributs d'accessibilité
        this.updateAccessibility(theme);

        // Déclencher un événement personnalisé
        this.dispatchThemeEvent(theme);
    }

    updateColorScheme(theme) {
        let metaThemeColor = document.querySelector('meta[name="theme-color"]');
        let metaColorScheme = document.querySelector('meta[name="color-scheme"]');

        if (!metaThemeColor) {
            metaThemeColor = document.createElement('meta');
            metaThemeColor.name = 'theme-color';
            document.head.appendChild(metaThemeColor);
        }
        metaThemeColor.content = theme === 'dark' ? '#0f1419' : '#ff6b35';

        if (!metaColorScheme) {
            metaColorScheme = document.createElement('meta');
            metaColorScheme.name = 'color-scheme';
            document.head.appendChild(metaColorScheme);
        }
        metaColorScheme.content = theme === 'dark' ? 'dark' : 'light';
    }

    updateIcon(theme) {
        const toggleLabel = theme === 'dark' ? 'Passer au mode clair' : 'Passer au mode sombre';

        if (this.themeIcon) {
            const iconClass = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';

            // Animation de l'icône
            this.themeIcon.style.transform = 'scale(0) rotate(180deg)';

            setTimeout(() => {
                this.themeIcon.className = iconClass;
                this.themeIcon.title = toggleLabel;
                this.themeIcon.setAttribute('aria-label', toggleLabel);
                this.themeIcon.style.transform = 'scale(1) rotate(0deg)';
            }, 150);
        }

        if (this.themeToggle) {
            this.themeToggle.title = toggleLabel;
            this.themeToggle.setAttribute('title', toggleLabel);
        }
    }

    updateAccessibility(theme) {
        if (this.themeToggle) {
            const isDark = theme === 'dark';
            const label = isDark ? 'Passer au mode clair' : 'Passer au mode sombre';

            this.themeToggle.setAttribute('aria-pressed', String(isDark));
            this.themeToggle.setAttribute('aria-checked', String(isDark));
            this.themeToggle.setAttribute('aria-label', label);
            this.themeToggle.setAttribute('title', label);
            this.themeToggle.title = label;
        }
    }

    animateThemeTransition(callback) {
        // Ajouter une classe de transition
        this.html.classList.add('theme-transitioning');

        // Animation du bouton
        if (this.themeToggle) {
            this.themeToggle.style.transform = 'scale(0.9) rotate(180deg)';
        }

        // Attendre la fin de l'animation
        setTimeout(() => {
            if (this.themeToggle) {
                this.themeToggle.style.transform = 'scale(1) rotate(0deg)';
            }
            this.html.classList.remove('theme-transitioning');
            callback();
        }, 300);
    }

    saveTheme(theme) {
        try {
            localStorage.setItem('theme', theme);
            localStorage.setItem('themeTimestamp', Date.now().toString());
        } catch (error) {
            // Ignore storage errors in restricted browsers.
        }
    }

    observeSystemPreference() {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

        mediaQuery.addEventListener('change', (e) => {
            // Seulement si l'utilisateur n'a pas explicitement choisi un thème
            if (!localStorage.getItem('theme')) {
                const newTheme = e.matches ? 'dark' : 'light';
                this.switchTheme(newTheme);
            }
        });
    }

    dispatchThemeEvent(theme) {
        const event = new CustomEvent('themeChanged', {
            detail: {
                theme: theme,
                timestamp: Date.now()
            }
        });
        document.dispatchEvent(event);
    }

    // Méthodes utilitaires
    getCurrentTheme() {
        return this.currentTheme;
    }

    isDarkMode() {
        return this.currentTheme === 'dark';
    }

    isLightMode() {
        return this.currentTheme === 'light';
    }

    // Méthode pour forcer un thème (utile pour les tests)
    forceTheme(theme) {
        if (theme === 'dark' || theme === 'light') {
            this.switchTheme(theme);
        }
    }
}

// ===== INITIALISATION =====

let themeManager;

document.addEventListener('DOMContentLoaded', () => {
    // Initialiser le gestionnaire de thème
    themeManager = new ThemeManager();

    // Exposer globalement pour les tests
    window.themeManager = themeManager;

    // Fonctions utilitaires globales
    window.toggleTheme = () => themeManager.toggleTheme();
    window.setDarkMode = () => themeManager.forceTheme('dark');
    window.setLightMode = () => themeManager.forceTheme('light');
    window.getCurrentTheme = () => themeManager.getCurrentTheme();
});

// ===== GESTION DES ERREURS =====

window.addEventListener('error', (e) => {
    if (e.message.includes('theme')) {
        console.warn('Erreur de thème détectée, réinitialisation...');
        if (themeManager) {
            themeManager.forceTheme('dark');
        }
    }
});

// ===== UTILITAIRES POUR LES TESTS =====

// Fonction pour simuler un changement de préférence système
function simulateSystemPreferenceChange(isDark) {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const event = new MediaQueryListEvent('change', {
        matches: isDark
    });
    mediaQuery.dispatchEvent(event);
}

// Fonction pour réinitialiser le thème
function resetTheme() {
    localStorage.removeItem('theme');
    localStorage.removeItem('themeTimestamp');
    if (themeManager) {
        themeManager.forceTheme('dark');
    }
}

// Exposer les fonctions de test
window.simulateSystemPreferenceChange = simulateSystemPreferenceChange;
window.resetTheme = resetTheme;
