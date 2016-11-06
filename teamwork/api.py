from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import *
from urllib.parse import unquote_plus
import json

@require_POST
def edit_project_members(request, username, project_name):
    """Add or remove members from the project.
    """

    user = get_object_or_404(User, username=username)

    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        owner__user__username=username)
    
    # ok
    status_code = 200

    # POST['remove[]'] contains a list of usernames that
    # should be removed from the project
    for member_name in request.POST.getlist('remove[]'):
        try:
            member = User.objects.exclude(pk=user.id).get(username=member_name)
            project.members.remove(member.student)
        except:
            # bad request, user tried to remove a non-existing project member
            status_code = 400
            continue
    
    # POST['add[]'] contains a list of usernames that
    # should be added to the project
    for member_name in request.POST.getlist('add[]'):
        try:
            member = User.objects.get(username=member_name)
            project.members.add(member.student)
        except:
            # bad request, user tried to add a non-existing project member
            status_code = 400
            continue
    
    # get usernames in a list and send them as a response
    project_members = project.members.values('user')
    members_list = []
    for member in project_members:
        user = User.objects.get(pk=member['user'])
        members_list.append(user.username)

    response = JsonResponse(members_list, safe=False)
    response.status_code = status_code

    return response
