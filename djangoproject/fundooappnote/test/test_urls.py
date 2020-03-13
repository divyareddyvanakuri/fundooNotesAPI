from django.test import TestCase
from django.urls import reverse, resolve
from fundooappnote.views import CreateUser, LoginUser,logout,ForgotPassword,ResetPassword


# Create your tests here.
class TestUrls(TestCase):
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, CreateUser)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginUser)
    
    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)

    def test_forgotpassword_url_resolves(self):
        url = reverse('forgotpassword')
        self.assertEquals(resolve(url).func.view_class,ForgotPassword)

    def test_resetpassword_url_resolves(self):
        url = reverse('resetpassword')
        self.assertEquals(resolve(url).func.view_class,ResetPassword)