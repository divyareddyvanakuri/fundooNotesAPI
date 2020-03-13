from django.test import TestCase,Client
from django.urls import reverse
from fundooappnote import views
import json
# Create your tests here.
class TestUrls(TestCase):
    
    def test_register_POST(self):
        client = Client()
        respone = client.post(path=reverse('register'),data={'username':'bambam',
        'email':'bamabam@gmail.com','password':'123','confirmpassword':'123'},format='json')
        self.assertEquals(respone.status_code,200)
    