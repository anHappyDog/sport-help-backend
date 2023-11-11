from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.backends import ModelBackend
from django.forms import ValidationError
from django.utils import timezone


# Create your models here.
class Image(models.Model):
    imageId = models.AutoField(primary_key=True,editable=False)
    image = models.ImageField(upload_to="images/")
    createTime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Image"

class User(models.Model):
    userid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    username = models.CharField(max_length=64,null=False,unique=True)
    password = models.CharField(max_length=128,null=False,default="")
    email = models.EmailField(max_length=256,null=False,default="")
    phone = models.CharField(max_length=16,null=False,default="")
    avatar = models.ForeignKey(Image,on_delete=models.SET_NULL,null=True)
    createTime = models.DateTimeField(default=timezone.now)
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
    isTeam = models.BooleanField(default=False)
    class Meta:
        db_table = "SportRecord"
        
        






def validate_max_person_greater_than_2(value):
    if value < 2:
        raise ValidationError('max person should greater than 1')

def validate_cur_person_lte_max_person(value):
    if value > models.F('maxPerson'):
        raise ValidationError('cur person shouldn\'t greater than max person')


   
class Team(models.Model):
    STATE = [('R','RENEW'),('O','ON'),('E','END')]
    teamId = models.AutoField(primary_key=True,null=False,editable=False)
    teamName = models.CharField(unique=True,max_length=128,null=False,default='kossur')
    maxPerson = models.IntegerField(null=False,default=8,validators=[validate_max_person_greater_than_2],name='maxPerson')
    sportType = models.ForeignKey(Sport,default='其他运动',on_delete=models.CASCADE,to_field='sportName',name='sportType')
    createPerson = models.ForeignKey(User,null=True,on_delete=models.CASCADE,to_field='userid')
    createTime = models.DateTimeField(null=False,default=timezone.now)
    startTime = models.DateTimeField(default=timezone.now)
    endTime = models.DateTimeField(null=False,default=timezone.now)
    curPersonCnt = models.IntegerField(null=False,default=1,validators=[validate_cur_person_lte_max_person])
    teamState = models.CharField(null=True,max_length=1,choices=STATE)
    class Meta:
        db_table = "Team"

class TeamMember(models.Model):
    teamId = models.ForeignKey(Team,on_delete=models.CASCADE)
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = 'TeamMember'



class Article(models.Model):
    articleId = models.AutoField(primary_key=True,null=False,editable=False)
    userId = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    title = models.CharField(max_length=128,null=False,default='有趣的文章~')
    content = models.TextField(null=False)
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "Article"
        

class FeedBack(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    createUser = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    createTime = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = "FeedBack"
        
