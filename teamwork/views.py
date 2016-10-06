from django.shortcuts import render, get_object_or_404
from .models import *
from urllib.parse import unquote_plus

def project_details(request, username, project_name):
    """Project detail page for viewing all details related to one project.
    View all events, deadlines, time used for one project.
    """
    
    user = get_object_or_404(User, username=username)
    project_name = unquote_plus(project_name)
    project = get_object_or_404(Project,
        name=project_name,
        members__user__username=username)

    context = {
        'user': user,
        'project': project
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
