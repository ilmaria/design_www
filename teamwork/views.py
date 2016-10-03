from django.shortcuts import render

def project_details(request):
    """Project detail page for viewing all details related to one project.
    View all events, deadlines, time used for one project.
    """
    
    return render(request, 'project_details.html')


def dashboard(request):
    """Dashboard for viewing all current projects at the same time and
    seeing details for each project, like next event or deadline. 
    """

    return render(request, 'dashboard.html')
