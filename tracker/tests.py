from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()

# I have some unexpected errors occurring during tests
# about test db already exists and db is being accessed by other users
# so can't do much before fixing it

class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("register")

    def test_registration_view_post_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_view_post_invalid_data(self):
        data = {
            'username': 'testuser',
            'password1': 'pass',
            'password2': 'different'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())
