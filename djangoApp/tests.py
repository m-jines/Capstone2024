from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
class easyTest(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        
class viewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_your_view(self):
        url = reverse('home')  
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)  