from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import *
from urllib.parse import unquote_plus
from datetime import datetime, timedelta, time
import json

@require_POST
@login_required
def add_project(request):
    """Add new project."""

    project_name = request.POST.get('project_name')

    if project_name is None or project_name == '':
        return HttpResponse(status=400)

    project = Project(
        name=project_name,
        owner=request.user,
        description=""
    )
    # apparently we need to save the model before we can access it's
    # many-to-many fields (members field is many-to-many)
    project.save()

    project.members.add(request.user)

    return redirect('project_details', project_name=project_name)


@require_POST
@login_required
def add_event(request, project_name):
    """Add new event."""

    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        members__id=request.user.id)

    event_name = request.POST.get('event_name', '')
    event_date = request.POST.get('date', '')
    event_time = request.POST.get('time', '')
    event_type = request.POST.get('type', 'event')
    location = request.POST.get('location', '')

    if event_name == '':
        return HttpResponse(status=400)

    event_date = datetime.strptime(event_date, '%d/%m/%Y')

    event_time = datetime.strptime(event_time, '%H:%M')
    event_time = time(hour=event_time.hour, minute=event_time.minute)

    date_time = datetime.combine(event_date, event_time)
    date_time = timezone.make_aware(date_time,
        timezone.get_current_timezone())

    event = Event(
        name=event_name,
        project=project,
        date=date_time,
        type=event_type,
        location=location
    )

    event.save()

    return redirect('project_details', project_name=project_name)


@require_POST
@login_required
def add_task(request, project_name):
    """Add new task."""

    task_name = request.POST.get('task_name', '')

    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        members__id=request.user.id)

    task_exists = Task.objects.filter(
        name=task_name, project=project).exists()

    if task_name == '' or task_exists:
        return HttpResponse(status=400)

    time_estimate = request.POST.get('time_estimate', '').split(':')
    hours = int(time_estimate[0])
    minutes = int(time_estimate[1]) if len(time_estimate) == 2 else 0
    estimated_hours = timedelta(hours=hours, minutes=minutes)

    task = Task(
        name=task_name,
        project=project,
        estimated_hours=estimated_hours
    )

    # apparently we need to save the model before we can access it's
    # many-to-many fields (members field is many-to-many)
    task.save()

    assignees = request.POST.get('assignees', '').split(',')

    for username in assignees:
        try:
            user = User.objects.get(username=username)
            task.assignees.add(user)
        except:
            pass

    return redirect('project_details', project_name=project_name)


@require_POST
@login_required
def edit_task(request, project_name):
    """Edit task."""

    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        members__id=request.user.id)

    old_name = request.POST.get('old-task-name', '')
    new_name = request.POST.get('task-name', '')
    assignees = request.POST.get('assignees', '').split(',')
    time_estimate = request.POST.get('time-estimate', '').split(':')

    if new_name == '':
        return HttpResponse(status=400)

    task = get_object_or_404(Task, name=old_name, project=project)

    task.name = new_name

    hours = int(time_estimate[0])
    minutes = int(time_estimate[1]) if len(time_estimate) == 2 else 0
    estimated_hours = timedelta(hours=hours, minutes=minutes)
    task.estimated_hours = estimated_hours

    for user in task.assignees.all():
        task.assignees.remove(user)

    for username in assignees:
        try:
            user = User.objects.get(username=username)
            task.assignees.add(user)
        except:
            continue

    task.save()

    return redirect('project_details', project_name=project_name)


@require_POST
@login_required
def toggle_task_done(request, project_name):
    """Change task done state."""

    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        members__id=request.user.id)

    task_done = int(request.POST.get('task-done', '-1'))
    task_id = int(request.POST.get('task-id', '-1'))

    task = get_object_or_404(Task, id=task_id)

    task.done = True if task_done == 1 else False

    task.save()

    return redirect('project_details', project_name=project_name)

@require_POST
@login_required
def delete_task(request, project_name):
    """Delete task."""

    task_name = request.POST.get('task-name', '')

    if task_name == '':
        return HttpResponse(status=400)

    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        members__id=request.user.id)

    task = Task.objects.get(name=task_name, project=project)

    task.delete()

    return redirect('project_details', project_name=project_name)


@require_POST
@login_required
def edit_project_members(request, project_name):
    """Add or remove members from the project."""

    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        owner=request.user)

    # POST['users-to-remove'] contains a list of usernames that
    # should be removed from the project
    users_to_remove = request.POST.get('users-to-remove', '').split(',')

    for member_name in users_to_remove:
        try:
            member = User.objects.exclude(id=request.user.id).get(username=member_name)
            project.members.remove(member)
        except:
            continue

    # POST['users-to-add'] contains a list of usernames that
    # should be added to the project
    users_to_add = request.POST.get('users-to-add', '').split(',')

    for member_name in users_to_add:
        try:
            member = User.objects.get(username=member_name)
            project.members.add(member)
        except:
            continue

    return redirect('project_details', project_name=project_name)


@require_POST
@login_required
def search_users(request):
    """Return all usernames matching the search query."""

    query = request.POST.get('query', '')
    blacklist = request.POST.get('blacklist', '').split(',')
    whitelist = request.POST.get('whitelist', '').split(',')

    if query != '':
        # ok request
        status_code = 200
        matching_users = User.objects.exclude(username__in=blacklist)

        if len(whitelist) > 0 and whitelist[0] != '':
            matching_users = matching_users.filter(
                username__iregex=r'(' + '|'.join(whitelist) + ')')

        matching_users.filter(username__startswith=query).values('username')
    else:
        # bad request: query isn't string
        status_code = 400
        matching_users = []

    usernames = [user.username for user in matching_users]

    response = JsonResponse(usernames, safe=False)
    response.status_code = status_code

    return response

@require_POST
@login_required
def log_time(request, project_name):
    """Log date and time for current user in the project"""

    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        members__id=request.user.id)

    # get input date and convert to yyyy-mm-dd format
    logged_date = request.POST.get('date')
    logged_date = datetime.strptime(logged_date, '%d/%m/%Y')
    logged_date = timezone.make_aware(logged_date,
        timezone.get_current_timezone())

    # convert input hours and minutes into logged hours
    time_input = request.POST.get('time')

    time = time_input.split(':')
    hours = int(time[0])
    minutes = int(time[1]) if len(time) == 2 else 0

    logged_hours = timedelta(hours=hours, minutes=minutes)

    logged_time = LoggedTime(
        date=logged_date,
        hours=logged_hours,
        user=request.user,
        project=project
    )

    task_name = request.POST.get('log-time-task', '')

    if task_name != '':
        task = Task.objects.get(name=task_name, project=project)
        logged_time.task = task

    logged_time.save()

    return redirect('project_details', project_name=project_name)


@require_POST
@login_required
def dashboard_log_time(request, project_id):
    """Log date and time for current user in the project"""

    project = get_object_or_404(Project, id=project_id)

    # get input date and convert to yyyy-mm-dd format
    logged_date = request.POST.get('date')
    logged_date = datetime.strptime(logged_date, '%d/%m/%Y')
    logged_date = timezone.make_aware(logged_date,
        timezone.get_current_timezone())

    # convert input hours and minutes into logged hours
    time_input = request.POST.get('time')

    time = time_input.split(':')
    hours = int(time[0])
    minutes = int(time[1]) if len(time) == 2 else 0

    logged_hours = timedelta(hours=hours, minutes=minutes)

    logged_time = LoggedTime(
        date=logged_date,
        hours=logged_hours,
        user=request.user,
        project=project
    )

    task_name = request.POST.get('log-time-task', '')

    if task_name != '':
        task = Task.objects.get(name=task_name, project=project)
        logged_time.task = task

    logged_time.save()

    return redirect('dashboard')
