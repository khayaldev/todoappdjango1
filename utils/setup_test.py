from django.test import TestCase
from authentication.models import User
from faker import Faker

class TestSetup(TestCase):
  def setUp(self):
      self.faker=Faker()
      self.password=self.faker.password()
      self.user={
        'username':self.faker.name().split(' ')[0].lower(),
        'email':'khayalfarajov@todo.com',#we can't change because of the status code 409 in testing 'test_user_shouldnot_signup_with_taken_email'
        'password':self.password,
        'password2':self.password
        }

  def create_test_user(self):
    user=User.objects.create(username='khayalfarajov',email='khayalfarajov@todo.com')
    user.set_password('password12!')
    user.is_email_verified=True
    user.save()  
    return user
  def create_test_user_unverified_email(self):
    user=User.objects.create(username='khayalfarajov',email='khayalfarajov@todo.com')
    user.set_password('password12!')
    user.save()  
    return user
    
  def tearDown(self):
      return super().tearDown()
    