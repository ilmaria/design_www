from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from urllib.parse import unquote_plus
from datetime import timedelta, datetime
from .utils import json_serialize
import json


@login_required
def project_details(request, project_name):
    """Project detail page for viewing all details related to one project.
    View all tasks, events, deadlines, time used for one project.
    """

    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        members__id=request.user.id)

    total_times_per_user = []
    members = project.members.all()

    for member in members:
        loggedtimes = project.loggedtime_set.filter(user=member)
        loggedtime_total = timedelta()

        for loggedtime in loggedtimes:
            loggedtime_total += loggedtime.hours

        total_times_per_user.append((member.username, loggedtime_total))

    total_times_json = [time for time in total_times_per_user]

    events = Event.objects.filter(project=project, date__gt=datetime.now())

    context = {
        'project': project,
        'total_times_per_user': total_times_per_user,
        'total_times_json': json.dumps(total_times_json, default=json_serialize),
        'events': events,
    }

    return render(request, 'project_details.html', context)


@login_required
def dashboard(request):
    """Dashboard for viewing all current projects at the same time and
    seeing details for each project, like next event or deadline.
    """

    projects = Project.objects.filter(members__id=request.user.id)
    next_event = Event.objects.all()[:1]

    context = {
        'projects': projects,
        'next_event': next_event
    }

    return render(request, 'dashboard.html', context)

@login_required
def calendar(request):
    """Calendar that shows all events."""

    projects = Project.objects.filter(members__id=request.user.id)
    event_set = Event.objects.filter(project__in=projects)\
        .values('date', 'name', 'location', 'project__name')

    # turn QuerySet into a native python list of dictionaries
    events = [event for event in event_set]

    context = {
        'projects': projects,
        'events': json.dumps(events, default=json_serialize)
    }

    return render(request, 'calendar.html', context)


def login(request):
    """Login view."""

    return auth_views.login(request, template_name='login.html')


def logout(request):
    """Logout view."""

    return auth_views.logout(request, template_name='logout.html')
