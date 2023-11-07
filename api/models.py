from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone

# Create your models here.
class User(models.Model):
    userid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    username = models.CharField(max_length=64,null=False,unique=True)
    password = models.CharField(max_length=128,null=False,default="")
    email = models.EmailField(max_length=256,null=False,default="")
    phone = models.CharField(max_length=16,null=False,default="")
    def save(self,*args,**kwargs):
        self.password = make_password(self.password)
        super(User,self).save(*args,**kwargs)    
    def __str__(self) -> str:
        return self.username
    class Meta:
        db_table = 'User'
        
class Sport(models.Model):
    sportId = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    sportName = models.CharField(max_length=32,unique=True,null=False)
    sportDescription = models.CharField(max_length=256,null=False) 
    sportCoverName = models.CharField(max_length=64,null=False,default='defaultSportCover.jpg')   
    class Meta:
        db_table = "Sport"


class SportRecord(models.Model):
    sportRecordId = models.AutoField(primary_key=True,null=False,editable=False)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    sportId = models.ForeignKey(Sport,on_delete=models.CASCADE)
    startTime = models.DateTimeField(null=False)
    endTime = models.DateTimeField(null=False)
    class Meta:
        db_table = "SportRecord"


class Team(models.Model):
    teamId = models.AutoField(primary_key=True,null=False,editable=False)
    
    class Meta:
        db_table = "Team"



class Article(models.Model):
    articleId = models.AutoField(primary_key=True,null=False,editable=False)
    userId = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    content = models.TextField(null=False)
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "Article"