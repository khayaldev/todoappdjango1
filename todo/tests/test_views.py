from utils.setup_test import TestSetup
from django.urls import reverse
from todo.models import Todo

class TestViews(TestSetup):
  def test_should_create_todo(self):
    user=self.create_test_user()
    self.client.post(reverse('login'),{
      'username':user.username,
      'password':'password12!'
    })
    
    
    todos=Todo.objects.all()
    self.assertEqual(todos.count(),0)
    response=self.client.post(reverse('create'),{
      'owner':user,
      'title':'My todo',
      'description':'Let us  get it'
    })
    utodos=Todo.objects.all()
    
    self.assertEqual(utodos.count(),1)
    