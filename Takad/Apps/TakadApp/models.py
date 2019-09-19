from django.db import models
from datetime import date, datetime


class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255, null=True)
    password = models.TextField()
    is_admin = models.BooleanField()


class Reports(models.Model):
    verbose_msg = models.TextField()
    md5 = models.CharField(max_length=255)
    sha1 = models.CharField(max_length=255)
    sha256 = models.CharField(max_length=256)
    scan_date = models.DateTimeField()
    permalink = models.TextField()
    positives = models.IntegerField()
    total = models.IntegerField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

class Scan(models.Model):
    name = models.CharField(max_length=50)
    detected = models.BooleanField()
    version = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    update = models.IntegerField()
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
