from authentication.models import User
from utils.setup_test import TestSetup
from todo.models import Todo

class TestModels(TestSetup):
  def test_should_create_todo(self):
    user=self.create_test_user()
    todo=Todo(owner=user,title='mytodo',description="let's get it")
    todo.save()
    self.assertEqual(str(todo),'mytodo')
