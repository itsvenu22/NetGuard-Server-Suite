from django.db import models

# Create your models here.
class userdata(models.Model):
    username = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=255,null=True)
    usertype = models.CharField(max_length=255,null=True)

class usermapping(models.Model):
    user = models.ForeignKey(userdata, on_delete=models.SET_NULL, null=True, blank=True)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)

