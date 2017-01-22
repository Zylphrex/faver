from django.shortcuts import render
from django.contrib.auth import views, authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import json

from faver_app.models import FaverUser, FaverRequest, FaverContract


# Create your views here.
@csrf_exempt
def root_page(request):
    if request.user.is_authenticated():
        return dashboard(request)
    return render(request, 'faver_app/login.html')

@csrf_exempt
def register_user(request):
    if request.user.is_authenticated():
        return dashboard(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = User.objects.create_user(username, password=password)
            faver_user = FaverUser(username=username, password=password)
            faver_user.save()
            login(request, user)
            return dashboard(request)

        return render(request, 'faver_app/failed.html', context={'reason': 'Missing username or password'})

    return render(request, 'faver_app/failed.html', context={'reason': 'Not a POST request'})

@csrf_exempt
def login_user(request):
    if request.user.is_authenticated():
        return dashboard(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                if request.user.is_authenticated():
                    return dashboard(request)

            return render(request, 'faver_app/failed.html', context={'reason': 'Incorrect username or password'})

        return render(request, 'faver_app/failed.html', context={'reason': 'Missing username or password'})

    return render(request, 'faver_app/failed.html', context={'reason': 'Not a POST request'})

@csrf_exempt
def logout_user(request):
    logout(request)
    return render(request, 'faver_app/login.html')

@csrf_exempt
def dashboard(request):
    username = request.user.username
    faver_user = FaverUser.objects.get(username=username)
    return render(request, 'faver_app/dashboard.html', context={'username': username, 'reputation': faver_user.reputation, 'coins': faver_user.coins})

@csrf_exempt
def post_request(request):
    title = request.POST['title']
    description = request.POST['description']
    reward = int(request.POST['reward'])
    latitude = float(request.POST['latitude'])
    longitude = float(request.POST['longitude'])
    issuer = FaverUser.objects.get(username=request.user.username)
    issuer.coins -= reward
    issuer.save()
    faver_request = FaverRequest(title=title, description=description, reward=reward, latitude=latitude, longitude=longitude, issuer=issuer)
    faver_request.save()

    return get_requests(request)

@csrf_exempt
def get_requests(request):
    all_requests = []
    for faver_request in FaverRequest.objects.all():
        if not FaverContract.objects.filter(request=faver_request):
            single_request = {
                'title': faver_request.title,
                'description': faver_request.description,
                'issuer': faver_request.issuer.username,
                'reward': faver_request.reward,
                'latitude': str(faver_request.latitude),
                'longitude': str(faver_request.longitude),
            }
            all_requests.append(single_request)
    return HttpResponse(json.dumps(all_requests), content_type="application/json")

@csrf_exempt
def accept_request(request):
    issuer = FaverUser.objects.get(username=request.POST['issuer'])
    acceptor = FaverUser.objects.get(username=request.user.username)
    faver_request = FaverRequest.objects.get(title=request.POST['title'],  issuer=issuer)
    faver_contract = FaverContract(request=faver_request, issuer=issuer, acceptor=acceptor)
    faver_contract.save()
    return HttpResponse(json.dumps([]), content_type="application/json")

@csrf_exempt
def my_requests(request):
    username = request.user.username
    faver_user = FaverUser.objects.get(username=username)

    untaken_requests = []
    taken_requests = []

    for request_issued in FaverRequest.objects.filter(issuer=faver_user):
        if not FaverContract.objects.filter(request=request_issued):
            untaken_requests.append(request_issued)
        else:
            taken_requests.append(request_issued)

    return render(request, 'faver_app/my_requests.html', context={'username': username, 'reputation': faver_user.reputation, 'coins': faver_user.coins, 'untaken_requests': untaken_requests, 'taken_requests': taken_requests})

@csrf_exempt
def complete_request(request):
    username = request.user.username
    faver_user = FaverUser.objects.get(username=username)
    faver_request = FaverRequest.objects.get(title=request.POST['title'], issuer=faver_user)
    faver_contract = FaverContract.objects.get(request=faver_request, issuer=faver_user)
    acceptor = faver_contract.acceptor
    acceptor.coins += faver_request.reward
    acceptor.reputation += faver_request.reward * 2
    acceptor.save()
    faver_contract.delete()
    faver_request.delete()
    return my_requests(request)
