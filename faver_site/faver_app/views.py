from django.shortcuts import render
from django.contrib.auth import views, authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from faver_app.models import FaverUser, FaverRequest

# Create your views here.
@csrf_exempt
def root_page(request):
    if request.user.is_authenticated():
        return dashboard(request, request.user.username)
    return render(request, 'faver_app/login.html')

@csrf_exempt
def register_user(request):
    if request.user.is_authenticated():
        return dashboard(request, request.user.username)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = User.objects.create_user(username, password=password)
            faver_user = FaverUser(username=username, password=password)
            faver_user.save()
            login(request, user)
            return render(request, 'faver_app/dashboard.html', context={'username': username})

        return render(request, 'faver_app/failed.html', context={'reason': 'Missing username or password'})

    return render(request, 'faver_app/failed.html', context={'reason': 'Not a POST request'})

@csrf_exempt
def login_user(request):
    if request.user.is_authenticated():
        return dashboard(request, request.user.username)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                if request.user.is_authenticated():
                    username = request.user.username
                    return render(request, 'faver_app/dashboard.html', context={'username': username})

            return render(request, 'faver_app/failed.html', context={'reason': 'Incorrect username or password'})

        return render(request, 'faver_app/failed.html', context={'reason': 'Missing username or password'})

    return render(request, 'faver_app/failed.html', context={'reason': 'Not a POST request'})

@csrf_exempt
def logout_user(request):
    logout(request)
    return render(request, 'faver_app/login.html')

def dashboard(request, username):
    faver_user = FaverUser.objects.get(username=username)
    return render(request, 'faver_app/dashboard.html', context={'username': username, 'reputation': faver_user.reputation, 'coins': faver_user.coins})

def request(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        reward = int(request.POST['reward'])
        issuer = FaverUser.objects.get(username=request.user.username)
        faver_request = FaverRequest(title=title, description=description, reward=reward, issuer=issuer)
        faver_request.save()

    return dashboard(request, request.user.username)
