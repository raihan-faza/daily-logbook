from datetime import datetime as dt

from django.db import models


class Log(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(default=dt.today())
    details = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
