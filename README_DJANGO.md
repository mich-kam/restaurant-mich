# Bites Restaurant - Django Web Application

A modern, responsive restaurant website built with Django, featuring a complete content management system, reservation system, and interactive features.

## 🍽️ Features

### Frontend Features
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Modern UI**: Clean, modern design with smooth animations
- **Interactive Elements**: Add to cart, newsletter subscription, reservation form
- **Dynamic Content**: All content managed through Django admin

### Backend Features
- **Django Admin Panel**: Complete content management system
- **Database Models**: Categories, Dishes, Chefs, Testimonials, Services, Reservations
- **Form Handling**: Reservation and newsletter subscription forms
- **AJAX Integration**: Real-time interactions without page reload
- **Media Management**: Image uploads for dishes, chefs, and site content

### Sections
1. **Header**: Navigation with logo and reserve button
2. **Hero Section**: Main banner with call-to-action
3. **Categories**: Food categories with icons
4. **Popular Dishes**: Featured dishes with add to cart
5. **Services**: Restaurant services showcase
6. **Menu**: Complete menu with category filtering
7. **Reservation**: Table booking system
8. **Testimonials**: Customer reviews
9. **Chefs**: Team showcase
10. **Mobile App**: App download section
11. **Footer**: Contact info and social links

## 🛠️ Technologies Used

- **Backend**: Django 5.2.1, Python 3.12
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Icons**: Font Awesome 6.0
- **Fonts**: Google Fonts (Poppins)
- **Images**: Unsplash (placeholder images)

## 📁 Project Structure

```
bites_restaurant/
├── bites_restaurant/          # Django project settings
│   ├── settings.py           # Project configuration
│   ├── urls.py              # Main URL patterns
│   └── wsgi.py              # WSGI configuration
├── restaurant/               # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms
│   ├── admin.py             # Admin interface
│   ├── urls.py              # App URL patterns
│   └── management/          # Custom management commands
│       └── commands/
│           └── populate_data.py
├── templates/               # HTML templates
│   └── restaurant/
│       ├── base.html        # Base template
│       ├── home.html        # Home page
│       ├── menu.html        # Menu page
│       ├── about.html       # About page
│       ├── contact.html     # Contact/Reservation page
│       └── reservation_success.html
├── static/                  # Static files
│   ├── css/
│   │   └── styles.css       # Custom styles
│   └── js/
│       └── script.js        # JavaScript functionality
├── media/                   # User uploaded files
├── manage.py               # Django management script
└── db.sqlite3              # SQLite database
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/project
   ```

2. **Install Django** (if not already installed)
   ```bash
   pip install django
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Populate with sample data**
   ```bash
   python manage.py populate_data
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the website**
   - Main site: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/
   - Create a local administrator with `python manage.py createsuperuser`

## 🎨 Customization

### Adding New Dishes
1. Go to http://localhost:8000/admin/
2. Login with admin credentials
3. Navigate to "Dishes" section
4. Click "Add Dish"
5. Fill in the details and upload an image
6. Save the dish

### Managing Categories
1. In admin panel, go to "Categories"
2. Add new categories with appropriate icons
3. Assign dishes to categories

### Updating Site Settings
1. In admin panel, go to "Site Settings"
2. Update hero text, contact information, social media links
3. Upload hero image if desired

### Adding Chefs
1. In admin panel, go to "Chefs"
2. Add chef information including name, position, experience
3. Upload chef photos

## 🔧 Configuration

### Database
The project uses SQLite by default. For production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files
For production, run:
```bash
python manage.py collectstatic
```

### Environment Variables
Create a `.env` file for sensitive settings:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

## 📱 Responsive Design

The website is fully responsive and works on:
- **Mobile**: 320px - 768px
- **Tablet**: 768px - 1024px
- **Desktop**: 1024px+

## 🎯 Key Features Explained

### Reservation System
- Form validation with Django forms
- Email notifications (can be extended)
- Admin panel for managing reservations
- Success page after booking

### Newsletter Subscription
- AJAX-based subscription
- Email validation
- Admin panel management
- Duplicate prevention

### Add to Cart
- AJAX functionality
- Real-time notifications
- Session-based cart (can be extended to database)

### Category Filtering
- Dynamic menu filtering
- URL-based category selection
- Responsive filter buttons

## 🔒 Security Features

- CSRF protection on all forms
- SQL injection prevention (Django ORM)
- XSS protection
- Secure file uploads
- Admin authentication

## 🚀 Deployment

### For Production
1. Set `DEBUG = False` in settings.py
2. Configure production database
3. Set up static file serving
4. Configure media file serving
5. Set up web server (Nginx + Gunicorn recommended)

### Environment Variables
```bash
export SECRET_KEY="your-secret-key"
export DEBUG="False"
export ALLOWED_HOSTS="yourdomain.com"
```

## 🤝 Contributing

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For support or questions:
- Check the Django documentation
- Review the code comments
- Create an issue in the repository

## 🎉 Credits

- **Design**: Modern restaurant website design
- **Icons**: Font Awesome
- **Images**: Unsplash (placeholder images)
- **Framework**: Django
- **Frontend**: Bootstrap 5

---

**Enjoy your delicious Django restaurant website! 🍕🍔🍜** 