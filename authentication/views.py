from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from loginsysahy import settings
from django.core.mail import send_mail

def home(request):
    return render(request, 'authentication/index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exists. Be original dawg')
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, 'Email already registered :/')
            return redirect('home')
        
        if len(username)>18:
            messages.error(request, 'Username cannot be longer than 18 characters')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")

        if not username.isalnum():
            messages.error(request, 'Username must be alpha-numeric')
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname

        myuser.save()

        messages.success(request, "Da tao acc. check mail, moi gui mail xac nhan (tinh nang nay chua duoc ap dung)")

        # the email
        # ill rewrite it soon
        subject = 'Chao mung den voi web capcap tuyen sinh 10'
        message = 'chao' + myuser.first_name + '\n' + 'confirm email de kich hoat tai khoan bbla bla bla' 
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')
    
    return render(request, 'authentication/signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'authentication/index.html', {'firstname': firstname})
        
        else:
            messages.error(request, 'Bad credentials :<')
            return redirect('home')
    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')
