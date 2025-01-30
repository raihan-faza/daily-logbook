from datetime import datetime as dt

from django.contrib.auth.models import User
from django.db import models


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateField(default=dt.today().strftime("%d-%m-%Y"))
    details = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
