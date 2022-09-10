from django.db import models
from django.contrib.auth.models import AnonymousUser

#class User(AnonymousUser):
#    pass

class TractorAction(models.Model):
    name = models.CharField(max_length=128)