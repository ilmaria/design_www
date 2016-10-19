from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    """Application users."""

    # `user` field references to User model that holds the login information
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Student: {0}'.format(self.user.username)


class Project(models.Model):
    """Has all information related to one project."""

    name = models.CharField(max_length=255, default="My project")
    members = models.ManyToManyField(Student, related_name='projects')
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return 'Project: "{0}"'.format(self.name)


class Event(models.Model):
    """Describes different events that are related to one project."""

    name = models.CharField(max_length=255, default='My event')
    date = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return 'Event: "{0}" - {1} - {2}'.format(self.name, self.project, self.date)


class LoggedTime(models.Model):
    """This model has time information that a student has logged in
    some project."""

    date = models.DateField()
    hours = models.DurationField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return 'LoggedTime: {0} - {1} - {2}'.format(self.date, self.student, self.hours)


class Task(models.Model):
    """Tasks for check list."""

    name = models.CharField(max_length=255, default='My task')
    done = models.BooleanField()
