from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, views as auth_views, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from urllib.parse import unquote_plus
from datetime import timedelta
from django.utils import timezone
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

    # total time logged by all members
    total_project_loggedtime = timedelta();

    for member in members:
        loggedtimes = project.loggedtime_set.filter(user=member)
        loggedtime_total = timedelta()

        for loggedtime in loggedtimes:
            loggedtime_total += loggedtime.hours

        total_project_loggedtime += loggedtime_total
        total_times_per_user.append((member.username, loggedtime_total))

    total_times_json = [time for time in total_times_per_user]

    task_list = Task.objects.filter(project=project)
    tasks = []

    for task in task_list:
        logged_times = LoggedTime.objects.filter(task=task)
        task_logged_time = timedelta()

        for time in logged_times:
            task_logged_time += time.hours

        if task.estimated_hours.total_seconds() > 0:
            task_progress = min(task_logged_time / task.estimated_hours, 1)
            task_progress = int(round(task_progress, 2) * 100)
        else:
            task_progress = 100

        tasks.append((task, task_progress))

    events = Event.objects.filter(project=project, date__gt=timezone.now())

    context = {
        'project': project,
        'total_project_loggedtime': total_project_loggedtime,
        'total_times_per_user': total_times_per_user,
        'total_times_json': json.dumps(total_times_json, default=json_serialize),
        'tasks': tasks,
        'events': events
    }

    return render(request, 'project_details.html', context)


@login_required
def dashboard(request):
    """Dashboard for viewing all current projects at the same time and
    seeing details for each project, like next event or deadline.
    """

    projects = Project.objects.filter(members__id=request.user.id)

    next_event = Event.objects\
        .filter(project__in=projects)\
        .filter(date__gt=timezone.now())\
        .order_by('date').first()

    project_list = []

    for project in projects:
        task_list = Task.objects.filter(project=project)
        logged_times = LoggedTime.objects.filter(project=project)
        estimate = timedelta()
        logged_time = timedelta()

        for task in task_list:
            estimate += task.estimated_hours

        for time in logged_times:
            logged_time += time.hours

        progress = 0

        if estimate.total_seconds() > 0:
            progress = min(logged_time / estimate, 1)
            progress = int(round(progress, 2) * 100)

        project_list.append((project, estimate, logged_time, progress))

    context = {
        'project_list': project_list,
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


def register(request):
    """Registration view."""

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')

    else:
        form = UserCreationForm()

    return render(request, 'registration.html', {'form': form})
