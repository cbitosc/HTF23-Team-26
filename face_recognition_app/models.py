from django.db import models


class Attendance(models.Model):
    name = models.CharField(max_length=255)
    time = models.TimeField()
    date = models.DateField()