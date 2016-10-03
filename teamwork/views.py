from django.shortcuts import render

def project_details(request):
    return render(request, 'project_details.html')


def dashboard(request):
    return render(request, 'dashboard.html')
