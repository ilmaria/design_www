from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import *
from urllib.parse import unquote_plus
import json

@require_POST
def edit_project_members(request, username, project_name):
    """Add or remove members from the project."""

    user = get_object_or_404(User, username=username)

    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        owner__user__username=username)

    # POST['remove[]'] contains a list of usernames that
    # should be removed from the project
    for member_name in request.POST.getlist('remove[]'):
        try:
            member = User.objects.exclude(id=user.id).get(username=member_name)
            project.members.remove(member.student)
        except:
            # bad request: user tried to remove a non-existing project member
            return HttpResponse(status=400)
    
    # POST['add[]'] contains a list of usernames that
    # should be added to the project
    for member_name in request.POST.getlist('add[]'):
        try:
            member = User.objects.get(username=member_name)
            project.members.add(member.student)
        except:
            # bad request: user tried to add a non-existing project member
            return HttpResponse(status=400)

    return HttpResponseRedirect(reverse('project_details', args=(username, project_name)))


@require_POST
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
