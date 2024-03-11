from .abstract import Abstract
from django.db import models
from .project import Project


class Task(Abstract):
    status = models.BooleanField(default=False)
    priority = models.IntegerField(default=1)
    deadline = models.DateTimeField(null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
