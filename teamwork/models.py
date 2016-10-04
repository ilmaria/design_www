from django.db import models

class Project(models.Model):
    """Has all information related to one project."""

    name = models.CharField(max_length=255)
    course = ""

    def __str__(self):
        return "\"{0}\"".format(self.name)


class Event(models.Model):
    """Describes different events that are related to one project.
    TODO: Should deadlines be different model than events?
    """

    date = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.project) + ', ' + str(self.date)
