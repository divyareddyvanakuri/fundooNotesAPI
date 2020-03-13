from django.test import TestCase
from django.urls import reverse, resolve
from fundooappnote import views

# Create your tests here.
class TestUrls(TestCase):

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, views.CreateUser)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, views.LoginUser)
    
    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, views.logout)

    def test_forgotpassword_url_resolves(self):
        url = reverse('forgotpassword')
        self.assertEquals(resolve(url).func.view_class,views.ForgotPassword)

    def test_resetpassword_url_resolves(self):
        url = reverse('resetpassword')
        self.assertEquals(resolve(url).func.view_class,views.ResetPassword)

    def test_createnote_url_resolves(self):
        url = reverse('createnote')
        self.assertEquals(resolve(url).func.view_class,views.CreateNote)

    def test_editnote_url_resolves(self):
        url = reverse('editnote',kwargs={'pk':19})
        self.assertEquals(resolve(url).func.view_class,views.UpdateNote)

    def test_deletenote_url_resolves(self):
        url = reverse('deletenote',kwargs={'pk':19})
        self.assertEquals(resolve(url).func.view_class,views.DeleteNote)
    
    def test_archive_url_resolves(self):
        url = reverse('archive')
        self.assertEquals(resolve(url).func,views.archive_detail)

    def test_displaynote_url_resolves(self):
        url = reverse('displaynote')
        self.assertEquals(resolve(url).func.view_class,views.DisplayNote)
    
    def test_trash_url_resolves(self):
        url = reverse('trash')
        self.assertEquals(resolve(url).func,views.trash_detail)

    def test_pinnote_url_resolves(self):
        url = reverse('pinnote')
        self.assertEquals(resolve(url).func,views.pinnote_detail)

    def test_restore_url_resolves(self):
        url = reverse('restore',kwargs={'pk':19})
        self.assertEquals(resolve(url).func.view_class,views.RestoreNote)
    