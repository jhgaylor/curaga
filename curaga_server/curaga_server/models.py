from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Package(models.Model):
    name = models.CharField(max_length=200, unique=True)
    package = models.FileField(upload_to='packages')
    user = models.ForeignKey(User)

class PackageDownload(models.Model):
    package = models.ForeignKey(Package)
    ip = models.IPAddressField()
