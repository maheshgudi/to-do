from django.db import models
from django.contrib.auth.models import User , Group, Permission
from django.contrib.contenttypes.models import ContentType


class Task(models.Model):
    task_body = models.CharField(max_length=1000, help_text="Add your task here")
    created_by = models.ForeignKey(User)
    completed = models.BooleanField(default=False)
    group = models.ForeignKey(Group)

class UserTask(models.Model):
    assignee = models.ForeignKey(User)
    task = models.ForeignKey(Task)
