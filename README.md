# Bites Restaurant

Site de restaurant responsive développé avec Django 5.2. Il comprend un menu, les réservations, les commandes, les événements, un blog et une administration Django.

## Développement local

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Le site est disponible sur <http://127.0.0.1:8000/> et l'administration sur <http://127.0.0.1:8000/admin/>.

En local, SQLite est utilisé par défaut. Pour créer un compte d'administration, exécutez `python manage.py createsuperuser`.

## Déploiement gratuit

Le dépôt contient un Blueprint Render (`render.yaml`) pour le serveur web gratuit. Render met les services gratuits en veille après une période d'inactivité; le premier chargement peut donc être lent. Le système de fichiers du serveur est temporaire.

1. Créez une base PostgreSQL gratuite sur [Neon](https://neon.com/).
2. Dans Render, choisissez **New > Blueprint**, puis le dépôt `mich-kam/restaurant-mich`.
3. Fournissez l'URL de connexion PostgreSQL Neon comme variable `DATABASE_URL`.
4. Déployez le Blueprint. Render génère la clé Django et configure les hôtes HTTPS.
5. Créez votre compte administrateur avec `python manage.py createsuperuser` après connexion à la base de production, ou via une console Render.

Ne publiez jamais `.env`, `db.sqlite3`, les mots de passe ni les clés privées. Les fichiers téléversés via l'administration ne sont pas persistants sur l'offre gratuite Render.
