from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import *
from urllib.parse import unquote_plus
from datetime import timedelta
import datetime
import json

@require_POST
@login_required
def add_project(request):
    """Add new project."""

    project_name = request.POST.get('project_name')

    if project_name is None:
        return HttpResponse(status=400)

    project = Project(
        name=project_name,
        owner=request.user,
        description=""
    )
    # apparently we need to save the project before we can access it's
    # many-to-many fields (members field is many-to-many)
    project.save()

    project.members.add(request.user)
    project.save()

    return redirect('dashboard')


@require_POST
@login_required
def edit_project_members(request, project_name):
    """Add or remove members from the project."""

    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        owner=request.user)

    # POST['remove[]'] contains a list of usernames that
    # should be removed from the project
    for member_name in request.POST.getlist('remove[]'):
        try:
            member = User.objects.exclude(id=request.user.id).get(username=member_name)
            project.members.remove(member)
        except:
            # bad request: user tried to remove a non-existing project member
            return HttpResponse(status=400)

    # POST['add[]'] contains a list of usernames that
    # should be added to the project
    for member_name in request.POST.getlist('add[]'):
        try:
            member = User.objects.get(username=member_name)
            project.members.add(member)
        except:
            # bad request: user tried to add a non-existing project member
            return HttpResponse(status=400)

    return redirect('project_details', project_name=project_name)


@require_POST
@login_required
def search_users(request):
    """Return all usernames matching the search query."""

    query = request.POST.get('query')

    # check if the query is a string
    if isinstance(query, str):
        # ok request
        status_code = 200
        matching_users = User.objects\
            .exclude(id=request.user.id)\
            .filter(username__startswith=query)\
            .values('username')
    else:
        # bad request: query isn't string
        status_code = 400
        matching_users = []

    usernames = [user['username'] for user in matching_users]

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
        owner=request.user)

    logged_date = request.POST.get('date')

    # convert input hours and minutes into logged hours
    input_hours = request.POST.get('hours')
    input_minutes = request.POST.get('minutes')
    logged_hours = timedelta(
        hours=int(input_hours),
        minutes=int(input_minutes)
    )

    loggedTime = LoggedTime(
        date=logged_date,
        hours=logged_hours,
        user=request.user,
        project=project
    )

    loggedTime.save()

    return redirect('project_details', project_name=project_name)
