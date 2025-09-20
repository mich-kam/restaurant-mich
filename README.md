# Portfolio Michel - Django

Un portfolio professionnel moderne développé avec Django, présentant les compétences, projets et expériences de manière élégante et responsive.

## 🚀 Fonctionnalités

### 📱 Design et Interface
- **Design moderne** avec dégradés et animations fluides
- **Entièrement responsive** pour tous les appareils (mobile, tablette, desktop)
- **Animations AOS** pour des transitions visuelles attrayantes
- **Navigation fixe** avec effets de survol
- **Interface utilisateur intuitive** avec breadcrumbs et navigation claire

### 📊 Gestion de Contenu
- **Interface d'administration Django** complète et personnalisée
- **Gestion des projets** avec galerie d'images, technologies et liens
- **Système de compétences** organisé par catégories avec niveaux
- **Timeline des expériences** professionnelles et formations
- **Formulaire de contact** avec validation et messages

### 🔍 Fonctionnalités Avancées
- **Système de recherche** pour les projets
- **Filtres dynamiques** par technologie et statut
- **Pagination** pour une navigation optimale
- **Téléchargement de CV** 
- **Galerie d'images** avec modal et zoom
- **Système de messages** pour les contacts

## 🛠️ Technologies Utilisées

### Backend
- **Django 4.2.7** - Framework web Python
- **SQLite** - Base de données (prête pour PostgreSQL)
- **Pillow** - Gestion des images
- **Python 3.12** - Langage de programmation

### Frontend
- **Bootstrap 5** - Framework CSS responsive
- **HTML5/CSS3** - Structure et style
- **JavaScript ES6** - Interactivité
- **Font Awesome 6** - Icônes
- **Google Fonts (Poppins)** - Typographie
- **AOS Library** - Animations au scroll

## 📦 Installation et Configuration

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner le projet**
```bash
git clone <url-du-repo>
cd mich-pro
```

2. **Installer les dépendances**
```bash
pip install django pillow
```

3. **Effectuer les migrations**
```bash
python manage.py migrate
```

4. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

5. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

6. **Accéder au portfolio**
- Portfolio : http://127.0.0.1:8000/
- Administration : http://127.0.0.1:8000/admin/

## 📋 Structure du Projet

```
mich-pro/
├── portfolio/                  # Application principale
│   ├── models.py              # Modèles de données
│   ├── views.py               # Vues et logique
│   ├── urls.py                # Configuration des URLs
│   ├── admin.py               # Interface d'administration
│   ├── forms.py               # Formulaires
│   └── migrations/            # Migrations de base de données
├── portfolio_michel/          # Configuration du projet
│   ├── settings.py            # Paramètres Django
│   ├── urls.py                # URLs principales
│   └── wsgi.py                # Configuration WSGI
├── templates/portfolio/       # Templates HTML
│   ├── base.html              # Template de base
│   ├── accueil.html           # Page d'accueil
│   ├── apropos.html           # Page à propos
│   ├── projets.html           # Liste des projets
│   ├── projet_detail.html     # Détail d'un projet
│   ├── competences.html       # Page des compétences
│   ├── experiences.html       # Page des expériences
│   └── contact.html           # Page de contact
├── static/                    # Fichiers statiques
│   ├── css/style.css          # Styles CSS personnalisés
│   └── js/script.js           # JavaScript personnalisé
└── media/                     # Fichiers uploadés (images, CV)
```

## 🎯 Modèles de Données

### ProfilPersonnel
Informations personnelles, CV, réseaux sociaux, disponibilité

### Categorie
Catégories de compétences (Frontend, Backend, DevOps, etc.)

### Competence
Compétences techniques avec niveaux et pourcentages

### Projet
Projets avec descriptions, technologies, images et liens

### Experience
Expériences professionnelles, formations et projets personnels

### Contact
Messages de contact avec système de notification

### ImageProjet
Galerie d'images pour chaque projet

## 🔧 Configuration

### Administration Django
Le projet inclut une interface d'administration personnalisée avec :
- Gestion complète de tous les modèles
- Interface intuitive pour l'ajout de contenu
- Filtres et recherche avancés
- Organisation logique des données

### Fichiers Media
Les images et fichiers sont stockés dans le dossier `media/` :
- Photos de profil : `media/profil/`
- Images de projets : `media/projets/`
- CV : `media/cv/`

## 🚀 Déploiement en Production

### Variables d'Environnement
Créer un fichier `.env` avec :
```env
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=your-database-url
STATIC_ROOT=/path/to/static/
MEDIA_ROOT=/path/to/media/
```

### Base de Données
Le projet est configuré pour SQLite en développement mais peut facilement être migré vers PostgreSQL :

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'portfolio_db',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Serveur Web
Configuration recommandée avec Nginx + Gunicorn pour la production.

## 📱 Pages Disponibles

### 🏠 Accueil (`/`)
- Section hero avec présentation
- Projets récents (3 derniers)
- Compétences principales (8 principales)
- Expériences récentes (2 dernières)
- Call-to-action pour contact

### 👤 À propos (`/apropos/`)
- Biographie détaillée avec photo
- Compétences organisées par catégorie
- Timeline complète des expériences
- Informations de contact
- Réseaux sociaux

### 💼 Projets (`/projets/`)
- Liste paginée des projets
- Système de recherche
- Filtres par technologie et statut
- Cartes avec preview et métadonnées
- Statistiques des projets

### 🔍 Détail Projet (`/projet/<id>/`)
- Description complète du projet
- Galerie d'images avec modal
- Technologies utilisées avec niveaux
- Liens vers démo et code source
- Projets similaires

### 🛠️ Compétences (`/competences/`)
- Compétences organisées par catégorie
- Barres de progression animées
- Projets utilisant chaque compétence
- Statistiques des compétences
- Section d'apprentissage continu

### 🎓 Expériences (`/experiences/`)
- Timeline interactive par type
- Onglets : Travail, Formation, Freelance, Personnel
- Détails complets de chaque expérience
- Compétences utilisées pour chaque poste
- Résumé du parcours

### 📧 Contact (`/contact/`)
- Formulaire de contact avec validation
- Informations de contact détaillées
- FAQ interactive
- Réseaux sociaux
- Temps de réponse estimé

## 🎨 Personnalisation

### Couleurs et Thème
Modifier les variables CSS dans `static/css/style.css` :
```css
:root {
    --primary-color: #6c63ff;
    --accent-color: #ff6b6b;
    --dark-color: #2c3e50;
    /* ... */
}
```

### Contenu
Tout le contenu est gérable via l'interface d'administration Django à l'adresse `/admin/`

## 🐛 Dépannage

### Problèmes Courants

1. **Images non affichées**
   - Vérifier la configuration MEDIA_URL et MEDIA_ROOT
   - S'assurer que les permissions du dossier media sont correctes

2. **Erreurs de migration**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Problèmes de CSS/JS**
   - Vérifier la configuration STATIC_URL
   - Exécuter `python manage.py collectstatic` en production

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👤 Auteur

**Michel Dupont** - Développeur Full Stack
- 📧 Email : michel.dupont@email.com
- 🔗 LinkedIn : [linkedin.com/in/michel-dupont](https://linkedin.com/in/michel-dupont)
- 🐱 GitHub : [github.com/micheldupont](https://github.com/micheldupont)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📞 Support

Pour toute question ou problème :
- 📧 Email : support@portfolio-michel.com
- 🐛 Issues : [GitHub Issues](https://github.com/micheldupont/portfolio/issues)

---

**⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !**
