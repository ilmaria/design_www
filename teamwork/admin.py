from django.contrib import admin

from teamwork.models import *

for model in [Project, Event, Student, LoggedTime]:
    admin.site.register(model)
