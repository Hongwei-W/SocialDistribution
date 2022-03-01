from rest_framework.test import APITestCase
from myapp.models import Author
from django.contrib.auth.models import Author

class TestUserModel(APITestCase):

    def test_creates_user(self):
        user = User.objects.create_user('testtest', 'test@123.com', 'werfwxqw12')
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'test@123.com')

# class TestAuthorModel(APITestCase):
#
#     def test_create_author(self):
#         author = Author.objects.create_author
