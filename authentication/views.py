from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from helpers.decorators import auth_user_should_not_access
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from django.urls import reverse


class EmailThread(threading.Thread):
    def __init__(self,  email):
        self.email = email
        threading.Thread.__init__(self) 
    
    def run(self):
        self.email.send()
    
def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authentication/activate.html', {
      'user':user, 
      'domain':current_site, 
      'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
      'token':generate_token.make_token(user), 
      
    })
    email = EmailMessage(subject = email_subject, body = email_body, from_email = settings.EMAIL_FROM_USER, to = [user.email])
    
    if not settings.TESTING:
        EmailThread(email).start()

def register(request):
    if request.method == 'POST':
        context = {'has_error':False, 'data':request.POST}
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if len(password)<6:
          messages.error(request,  'Password must be at least 6 characters')
          context['has_error']  =  True

        if not username:
          messages.warning(request,  'Username is required')
          context['has_error']  =  True


        if not email:
          messages.warning(request,  'Email is required')
          context['has_error']  =  True


        if password !=  password2:
          messages.error(request,  'Password mismatch')
          context['has_error']  =  True


        if not validate_email(email):
            messages.error(request,  'Please enter a valid email address e.g : khayalfarajov@gmail.com')
            context['has_error']  =  True

        if User.objects.filter(username  =  username).exists():
              messages.error(request,  'Username has already taken.')
              context['has_error']  =  True
              return render(request,  "authentication/register.html",  context,  status  =  409)


        if User.objects.filter(email  =  email).exists():
              messages.error(request,  'There is a user with that email.')
              context['has_error']  =  True
              return render(request,  "authentication/register.html",  context,  status  =  409)
            
        if context['has_error']:
          return render(request,  "authentication/register.html",  context,  status = 401)
        
        user = User.objects.create(username = username,  email = email)
        user.set_password(password)
        user.save()
        
        if not context['has_error']:
          send_activation_email(user,  request)
          messages.success(request,  'We have sent email for verification. Check your mailbox.')
          return redirect('login')      
        
        messages.success(request,  'Your account is ready')
    return render(request,  "authentication/register.html")

 
@auth_user_should_not_access
def login_user(request):
  
    if request.method == 'POST':
      context = {'data':request.POST}
      username = request.POST.get('username')
      password = request.POST.get('password')
      
      
      user = authenticate(username = username, password = password)
      
      if not user:
        messages.error(request,  'Invalid Credentials')
        return render(request,  "authentication/login.html",  context,  status = 401)
      
      if user and not user.is_email_verified:
          messages.error(request,  'Account is not verified.')
          return render(request,  "authentication/login.html",  context,  status = 401)
      
      login(request,  user)
      messages.success(request,  f'Hello again,  {request.user.username}')
      return redirect(reverse('home'))
    return render(request,  'authentication/login.html')




def logout_user(request):
    if request.method == 'POST':
      logout(request)
      messages.success(request,  'Your signed out succesfully')

      
      return redirect('login')



def activate_user(request,  uidb64,  token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
      
    except Exception as e:
        user = None
    if user and generate_token.check_token(user,  token):
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Email is verified,  now you can log in !')
        return redirect('login')
      
    return render(request,  'authentication/activation-failed.html',  {"user":user})


