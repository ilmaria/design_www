from django.shortcuts import render, get_object_or_404
from .models import *
from urllib.parse import unquote_plus
from datetime import timedelta
from .utils import json_serialize
import json

def project_details(request, username, project_name):
    """Project detail page for viewing all details related to one project.
    View all events, deadlines, time used for one project.
    """

    user = get_object_or_404(User, username=username)

    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        members__user__username=username)

    loggedtimes = project.loggedtime_set.filter(student__user=user)
    loggedtime_total = timedelta()

    for loggedtime in loggedtimes:
        loggedtime_total += loggedtime.hours

    context = {
        'user': user,
        'project': project,
        'loggedtime_total': loggedtime_total
    }

    return render(request, 'project_details.html', context)


def dashboard(request, username):
    """Dashboard for viewing all current projects at the same time and
    seeing details for each project, like next event or deadline.
    """

    user = get_object_or_404(User, username=username)
    projects = Project.objects.filter(members__user__username=username)

    context = {
        'user': user,
        'projects': projects
    }

    return render(request, 'dashboard.html', context)


def calendar(request, username):
    """Calendar that shows all events."""

    user = get_object_or_404(User, username=username)
    projects = Project.objects.filter(members__user__username=username)

    event_set = Event.objects.filter(project__in=projects)\
        .values('date', 'name', 'location')

    # turn QuerySet into a native python list of dictionaries
    events = [event for event in event_set]

    context = {
        'user': user,
        'projects': projects,
        'events': json.dumps(events, default=json_serialize)
    }

    return render(request, 'calendar.html', context)
