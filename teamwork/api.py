from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import *
from urllib.parse import unquote_plus
import json

@require_POST
def add_project(request, new_project_name, username):
    """Add new project."""
    user = get_object_or_404(User, username=username)
    student=Student(user)
    # POST['new_project_name'] contains name for the new project to be created
    project_name = request.POST.get('new_project_name')
    project=Project(project_name, [], student, "")
    project.members.add(student)
    project.save()

    return HttpResponseRedirect(reverse('project_details', args=(username, project_name)))