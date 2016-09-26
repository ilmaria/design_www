from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "\"{0}\"".format(self.name)


class Event(models.Model):
    date = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.project) + ', ' + str(self.date)
