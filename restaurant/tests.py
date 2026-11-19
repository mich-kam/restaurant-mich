from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse


@override_settings(
    STORAGES={
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
)
class RestaurantAdminBrandingTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin_user = user_model.objects.create_superuser(
            username='admin-test',
            email='admin-test@example.com',
            password='test-only-password',
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

    def test_admin_home_uses_restaurant_branding_and_theme(self):
        response = self.client.get(reverse('admin:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bites')
        self.assertContains(response, 'Bites Restaurant')
        self.assertContains(response, 'css/admin-theme.css')
        self.assertContains(response, 'Voir le site')

    def test_admin_login_uses_restaurant_theme(self):
        self.client.logout()

        response = self.client.get(reverse('admin:login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'css/admin-theme.css')
