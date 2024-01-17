from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from emailverify import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import smart_str

from django.core.mail import EmailMessage,send_mail


def home(request):
    return render(request,'authentication/index.html')

def signup(request):
    if request.method == 'POST':

        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username = username):
            messages.error(request,'This Username Is Already Taken! Please Try Another')
            return redirect('signup')
        
        if User.objects.filter(email = email):
            messages.error(request,'This Email Is Already Registered! Please Try Another Email or Try Signin')
            return redirect('signup')
        
        if len(username)>10:
            messages.error(request,'This Username Should Be Under 10 Characters')
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request,'The Passwords Are not Matching!')
            return redirect('signup')
        

        user = User.objects.create_user(username=username, first_name=first_name ,last_name=last_name, email=email, password=pass1)
        user.save()
        messages.success(request,'Account Created Successfully')

        # Welcome Mail

        subject = "Finally First Login Mail Verify Project!"
        message = " Hello!" + user.first_name + "Welcome To My Verification Test \n Thank You For Your Patience! \n Hope This Works \n\n Thanks,"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently = False)

        return redirect('signin')


        


    else:
        return render(request,'authentication/signup.html')

def signin(request): 
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user =authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request, 'authentication/index.html',{'fname' : fname})
        else:
            messages.error(request,'Add Credentials')
            return redirect('home')
        
    return render(request,'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request,'Sucessfully Logged Out!')
    return redirect('home')