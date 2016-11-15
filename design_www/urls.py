"""design_www URL Configuration

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

from teamwork import views
from teamwork import api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^$', views.login, name='login'),

    url(r'^(?P<username>\w+)/dashboard/$',
        views.dashboard, name='dashboard'),
    
    url(r'^(?P<username>\w+)/calendar/$',
        views.calendar, name='calendar'),

    url(r'^(?P<username>\w+)/(?P<project_name>.+?)/$',
        views.project_details, name='project_details'),

    url(r'^add_project/?$',
        api.add_project, name='add_project'),
]
