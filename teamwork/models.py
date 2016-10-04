from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    """Application users."""

    # `user` field references to User model that holds the login information
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Project(models.Model):
    """Has all information related to one project."""

    name = models.CharField(max_length=255, unique=True)
    course = models.CharField(max_length=255, blank=True)
    members = models.ManyToManyField(Student, related_name='projects')
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return "\"{0}\"".format(self.name)


class Event(models.Model):
    """Describes different events that are related to one project.
    TODO: Should deadlines be different model than events?
    """

    name = models.CharField(max_length=255, default="New Event")
    date = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.project) + ', ' + str(self.date)
