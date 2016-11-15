from django.contrib import admin

from teamwork.models import *

for model in [Project, Event, LoggedTime, Task]:
    admin.site.register(model)
