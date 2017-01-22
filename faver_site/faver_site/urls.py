"""faver_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views
import faver_app.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', faver_app.views.root_page),
    url(r'^login/$', faver_app.views.login_user),
    url(r'^logout/$', faver_app.views.logout_user),
    url(r'^register/$', faver_app.views.register_user),
    url(r'^accounts/profile/$', faver_app.views.dashboard),
    url(r'^request/$', faver_app.views.request),
]
