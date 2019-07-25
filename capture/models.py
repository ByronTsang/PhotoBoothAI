from django.db import models

# Create your models here.
from django.urls import reverse
from django.db import models

import misaka

from albums.models import Album

from django.contrib.auth import get_user_model
User = get_user_model()
'''
class Capture(models.Model):
    user = models.ForeignKey(User, related_name="photos",on_delete=models.PROTECT)
    album = models.ForeignKey(Album, related_name="photos",null=True, blank=True,on_delete=models.PROTECT)
    
    def __str__(self):
        return self.message
        '''