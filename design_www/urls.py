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
from django.views.generic import RedirectView

from teamwork import views
from teamwork import api

urlpatterns = [
    url(r'^login/$', views.login, name='login'),

    url(r'^logout/', views.logout, name='logout'),

    url(r'^admin/', admin.site.urls),

    url(r'^$', RedirectView.as_view(pattern_name='login'), name='home'),

    url(r'^dashboard/$', views.dashboard, name='dashboard'),

    url(r'^calendar/$', views.calendar, name='calendar'),

    url(r'^(?P<project_name>.+?)/$',
        views.project_details, name='project_details'),

    url(r'^(?P<project_name>.+?)/edit_project_members/?$',
        api.edit_project_members, name='edit_project_members'),

    url(r'^(?P<project_name>.+?)/log_time/?$', api.log_time, name='log_time'),

    url(r'^(?P<project_name>.+?)/add_task/?$', api.add_task, name='add_task'),

    url(r'^(?P<project_name>.+?)/delete_task/?$', api.delete_task, name='delete_task'),

    url(r'^search_users/?$', api.search_users, name='search_users'),

    url(r'^add_project/?$', api.add_project, name='add_project'),
]
