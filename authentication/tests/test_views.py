from django.urls import reverse
from django.contrib.messages import get_messages
from utils.setup_test import TestSetup

class TestViews(TestSetup):
  #Checking Render for a register page 
  def test_should_show_register_page(self):
    response=self.client.get(reverse('register'))
    self.assertEquals(response.status_code,200)

    self.assertTemplateUsed(response,'authentication/register.html')

    
  #Checking Render for a login page 
  def test_should_show_login_page(self):
    response=self.client.get(reverse('login'))
    self.assertEquals(response.status_code,200)
    self.assertTemplateUsed(response,'authentication/login.html')
    
  #Checking user signing up and redirect to login
  def test_user_should_signup(self):
    response=self.client.post(reverse('register'),self.user)
    self.assertEquals(response.status_code,302)

  def test_should_login_successfully(self):
      user = self.create_test_user()
      response = self.client.post(reverse("login"), {
            'username': user.username,
            'password': 'password12!' 
        })
      self.assertEqual(response.status_code, 302)

      storage = get_messages(response.wsgi_request)

      self.assertIn(f'Hello again,  {user.username}',
                      list(map(lambda x: x.message, storage)))

    
  #Checking username already exist or not
  def test_user_shouldnot_signup_with_taken_username(self):
    self.client.post(reverse('register'),self.user)
    response=self.client.post(reverse('register'),self.user)
    self.assertEquals(response.status_code,409)
    storage=get_messages(response.wsgi_request)
    self.assertIn('Username has already taken.',list(map(lambda message: message.message,storage)))
    #Iterative way to do
    # errors=[]
    # for message in storage:
    #   errors.append(message.message)
    # print(errors)
    # import pdb
    # pdb.set_trace()
    
  #Checking email already exist or not
  def test_user_shouldnot_signup_with_taken_email(self):

    self.user2={
      'username':'orujfarajov',
      'email':'khayalfarajov@todo.com',
      'password':'password',
      'password2':'password'
    }
    self.client.post(reverse('register'),self.user)
    response=self.client.post(reverse('register'),self.user2)
    self.assertEquals(response.status_code,409)
    storage=get_messages(response.wsgi_request)
    # for message in storage:
    #   print(message)
    #Debugging
    # import pdb
    # pdb.set_trace()
    self.assertIn('There is a user with that email.',list(map(lambda message: message.message,storage)))

  def test_should_not_login_with_invalid_password(self):
        user = self.create_test_user()
        response = self.client.post(reverse("login"), {
            'username': user.username,
            'password': 'password12!32'
        })
        self.assertEquals(response.status_code, 401)

        storage = get_messages(response.wsgi_request)

        self.assertIn("Invalid Credentials",
                      list(map(lambda x: x.message, storage))) 
  def test_should_not_login_with_unverified_email(self):
        user = self.create_test_user_unverified_email()
        response = self.client.post(reverse("login"), {
            'username': user.username,
            'password': 'password12!',   
        })
        self.assertEquals(response.status_code, 401)

        storage = get_messages(response.wsgi_request)

        self.assertIn("Account is not verified.",
                      list(map(lambda x: x.message, storage))) 
        
  def test_should_not_signup_less6_characters_passsword(self):
        response = self.client.post(reverse("register"), {
            'username':'khayalfarajov',
            'email':'khayalfarajov@todo.com',
            'password': 'pass!', 
            'password1':'pass!'  
        })
        self.assertEquals(response.status_code, 401)

        storage = get_messages(response.wsgi_request)

        self.assertIn('Password must be at least 6 characters',
                      list(map(lambda x: x.message, storage))) 
        
  def test_should_not_signup_without_username(self):
        response = self.client.post(reverse("register"), {
            'username':'',
            'email':'khayalfarajov@todo.com',
            'password': 'password12!', 
            'password1':'password12!'  
        })
        self.assertEquals(response.status_code, 401)

        storage = get_messages(response.wsgi_request)

        self.assertIn('Username is required',
                      list(map(lambda x: x.message, storage))) 

    
  def test_should_not_signup_without_email(self):
        response = self.client.post(reverse("register"), {
            'username':'khayalfarajov',
            'email':'',
            'password': 'password12!', 
            'password1':'password12!'  
        })
        self.assertEquals(response.status_code, 401)

        storage = get_messages(response.wsgi_request)

        self.assertIn('Email is required',
                      list(map(lambda x: x.message, storage))) 
    
  def test_should_not_signup_unmatched_password(self):
        response = self.client.post(reverse("register"), {
            'username':'khayalfarajov',
            'email':'khayalfarajov@gmail.com',
            'password': 'password12!', 
            'password1':'password1!'  
        })
        self.assertEquals(response.status_code, 401)

        storage = get_messages(response.wsgi_request)

        self.assertIn('Password mismatch',
                      list(map(lambda x: x.message, storage))) 
        
  def test_should_not_signup_unvalid_email(self):
        response = self.client.post(reverse("register"), {
            'username':'khayalfarajov',
            'email':'khayaltechgmail',
            'password': '123456', 
            'password1':'123456'  
        })
        self.assertEquals(response.status_code, 401)

        storage = get_messages(response.wsgi_request)

        self.assertIn('Please enter a valid email address e.g : khayalfarajov@gmail.com',
                      list(map(lambda x: x.message, storage))) 
