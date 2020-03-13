import sys
from django.test import TestCase
from django.urls import reverse,resolve
sys.path.append('/home/user/Desktop/fundooappnotes/djangoproject/')
from fundooappnote.views import CreateUser
# Create your tests here.
class TestUrls(TestCase):
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class,CreateUser)