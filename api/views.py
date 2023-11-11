from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import check_password,make_password
from django.views.decorators.http import require_http_methods,require_safe
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from .models import FeedBack, SportRecord, Team, TeamMember, User,Sport,Article
from uuid import uuid4
import json
from django.utils import timezone
# Create your views here.


@csrf_exempt
@require_http_methods('POST')
def SignUp(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        phone = data.get('phone')
        user = User.objects.filter(username=username)
        print('[' + password + ']')
        if len(user) != 0:
            return JsonResponse({"status":-1}) 
        user = User.objects.create(username=username,password=make_password(password),email=email,phone=phone)
    except Exception as e:
        return JsonResponse({'status':-2,"msg":str(e)})
    return JsonResponse({"status":0})
    
    
@csrf_exempt
@require_http_methods('POST')
def SignIn(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    print('[' + password +  ']')
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({"status":-1})
    try:
        if check_password(password,user.password):
            request.session['session'] = str(uuid4())
            request.session['username'] = username
            return JsonResponse({'status':0})
        else:
            return JsonResponse({'status':-2})
    except Exception as e:
        return JsonResponse({'status':-3,'msg':str(e)})

@csrf_exempt
@require_http_methods('GET')
def GetAvatarAndUsername(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-2,'msg':"未登录"})
    try:
        username = request.session['username']
        user = User.objects.get(username=username)
        if user is None:
            return JsonResponse({'status':-4,'msg':"该用户并不存在"})
        return JsonResponse({'status':0,'avatar':'asd','username':username})
    except Exception as e:
        return JsonResponse({'status':-3,"msg":str(e)})    


@csrf_exempt
@require_http_methods('GET')
def GetUserInfo(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-2,'msg':"未登录"})
    try:
        user = User.objects.get(username=request.session['username'])
        teamCnt = len(TeamMember.objects.filter(userId=user))
        exerciseCnt = len(SportRecord.objects.filter(userid=user))
        
        data = {'username':user.username,'email':user.email,'phone':user.phone,'createTime':user.createTime,
                'teamCnt':teamCnt,'exerciseCnt': exerciseCnt}
        return JsonResponse({'status':0,'data':data})
    except Exception as e:
        return JsonResponse({'status':-3,"msg":str(e)})    

@csrf_exempt
@require_http_methods('GET')
def SignOut(request):
    try:
        request.session.flush()
    except:
        return JsonResponse({"status":-1})
    return JsonResponse({"status":0})

@csrf_exempt
@require_http_methods('GET')
def SportInfo(request):
    if 'session' not in request.session:
        return JsonResponse({'status':-2,'data':[]}) 
    try:
        session = Session.objects.get(session_key=request.session.session_key)
        sports = Sport.objects.all()
        data = [{'sportId': str(t.sportId),'sportName':t.sportName,'sportDescription':t.sportDescription,'sportCoverName':t.sportCoverName}  for t in sports]
        
    except Exception as e:
        print(str(e))
        return JsonResponse({'status':-1,'data':[]}) 
    return JsonResponse({'status':0,'data':data})

@csrf_exempt
@require_http_methods('POST')
def ForgetPassword(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        user = User.objects.get(username=username)
        if user is None:
            return JsonResponse({'status':-1})
        email = user.email
        send_email(
            "This is your password",
            "Nobody",
            "cc_no_reply@gmail.com",
            [email],
            fail_silently=True
        )
        return JsonResponse({'status':0})
    except Exception as e:
        return JsonResponse({'status':-2,'msg':str(e)})
 
@csrf_exempt
@require_http_methods('POST')
def GetAvatar(request):
    
    return JsonResponse({'status':0})


@csrf_exempt
@require_http_methods('POST')
def UpdateAvatar(request):
    
    return JsonResponse({'status':0})

@csrf_exempt
@require_http_methods('POST')
def ChangeUserInfo(request):
    pass


@csrf_exempt
@require_http_methods('POST')
def DeliverErrors(request):
    pass


@csrf_exempt
@require_http_methods('GET')
# use the sessionid to check if ok.
# no params
def GetArticles(request):
    try:
        username = request.session['username']
        session = request.session['session']
        if username is None or session is None:
            return JsonResponse({'status':-2,'articles':[],'msg':'permission error'})
        articles = Article.objects.all()
        data = [{'articleId': t.articleId,'userId':t.userId,'create_at':t.create_at,'update_at':t.update_at,'content':t.content} for t in articles]
        return JsonResponse({'status':0,'articles':data})
    except Exception as e:
        return JsonResponse({'status':-1,"articles":[],'msg':str(e)})

@csrf_exempt
@require_http_methods('POST')
def DeliverArticle(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})
    try:
        data = json.loads(request.body)
        title = data['title']
        content = data['content']
        user = User.objects.get(username=request.session['username'])
        if user is None:
            return JsonResponse({'status':-3,'msg':"用户不存在!"})
        article = Article.objects.create(userId=user,title=title,content=content)
        return JsonResponse({'status':0,'msg':"上传成功"})
    except Exception as e:
        return JsonResponse({'status':-2,'msg':str(e)})
    

@csrf_exempt
@require_http_methods('POST')
def SearchFoodCalory(request):
    pass



@csrf_exempt
@require_http_methods('POST')
def GetExercisePlan(request):
    pass



@csrf_exempt
@require_http_methods('POST')
def GetCityWalk(request):
    pass


@csrf_exempt
@require_http_methods('POST')
def CreateTeam(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})
    try:
        user= User.objects.get(username=request.session['username'])
        data = json.loads(request.body)
        sport = Sport.objects.get(sportName=data['sportType'])
        team = Team.objects.create(teamName=data['teamName'],maxPerson=data['maxPerson'],sportType=sport,createPerson=user,curPersonCnt=1,teamState='R')
        TeamMember.objects.create(teamId=team,userId=user)
        return JsonResponse({'status':0})
    except Exception as e:
        return JsonResponse({'status':-2,'msg':str(e)})
    

@csrf_exempt
@require_http_methods('POST')
def EndTeam(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})
    try:
        data = json.loads(request.body)
        teamId = data['teamId']
        team = Team.objects.get(teamId=teamId)
        if team is None:
            return JsonResponse({'stauts':-5,'msg':"该队伍并不存在"})
        if team.teamState != 'O':
            return JsonResponse({'stauts':-4,'msg':"该队伍目前不支持结束"})
        user = User.objects.get(username=request.session['username'])
        createId = team.createPerson.userid
        if user.userid != createId:
            return JsonResponse({'status':-3,'msg':'操作者不是创建用户'})    
        team.teamState = 'E'
        team.endTime = timezone.now()
        team.save()
        for t in TeamMember.objects.filter(teamId=teamId):
            SportRecord.objects.create(userid=t.userId,sportId=Sport.objects.get(sportName=team.sportType),startTime=team.startTime,endTime=team.endTime)
        return JsonResponse({'status':0,'msg':"结束成功"})
    except Exception as e:
        print(e)
        return JsonResponse({'status':-2,'msg':str(e)})

@csrf_exempt
@require_http_methods('POST')
def DestroyTeam(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})
    try:
        data = json.loads(request.body)
        teamId = data['teamId']
        team = Team.objects.get(teamId=teamId)
        if team is None:
            return JsonResponse({'stauts':-2,'msg':"该队伍并不存在"})
        if team.teamState != 'R':
            return JsonResponse({'stauts':-4,'msg':"该队伍目前不支持解散"})    
        team.delete()
        
        return JsonResponse({'status':0,'msg':"解散成功"})
    except Exception as e:
        return JsonResponse({'status':-2,'msg':str(e)})

@csrf_exempt
@require_http_methods('POST')
def JoinTeam(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})
    try:
        data = json.loads(request.body)
        teamId = data['teamId']
        team = Team.objects.get(teamId=teamId)
        if team is None:
            return JsonResponse({'stauts':-2,'msg':"该队伍并不存在"})
        if team.teamState != 'R':
            return JsonResponse({'stauts':-4,'msg':"该队伍目前不支持加入"})    
        user = User.objects.get(username=request.session['username'])
        if user is None:
            return JsonResponse({'status':-3,'msg':'该用户并不存在'})
        TeamMember.objects.create(teamId=team,userId=user)
        return JsonResponse({'status':0,'msg':"加入成功"})
    except Exception as e:
        return JsonResponse({'status':-2,'msg':str(e)})

@csrf_exempt
@require_http_methods('POST')
def LeaveTeam(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})
    try:
        data = json.loads(request.body)
        teamId = data['teamId']
        team = Team.objects.get(teamId=teamId)
        if team is None:
            return JsonResponse({'stauts':-2,'msg':"该队伍并不存在"})
        user = User.objects.get(username=request.session['username'])
        if user is None:
            return JsonResponse({'status':-3,'msg':'该用户并不存在'})
        if team.teamState != 'R':
            return JsonResponse({'stauts':-4,'msg':"该队伍目前不支持离开"})    
        teamMember =  TeamMember.objects.get(teamId=team,userId=user)
        if teamMember is None:
            return JsonResponse({'status':-4,'msg':'该用户并不在该队伍中'})
        teamMember.delete()
        return JsonResponse({'status':0,'msg':"离队成功"})
    except Exception as e:
        return JsonResponse({'status':-2,'msg':str(e)})


@csrf_exempt
@require_http_methods('GET')
def GetSportRecord(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})   
    try:
        user = User.objects.get(username=request.session['username'])
        data = [{"sportName":t.sportId.sportName,"startTime":t.startTime,"endTime":t.endTime,"isTeam":t.isTeam} for t in SportRecord.objects.filter(userid=user)]
        return JsonResponse({'status':0,'data':data})
    except Exception as e:
        return JsonResponse({'status':-2,'msg':str(e)})

@csrf_exempt
@require_http_methods('GET')
def GetSportTaste(request):
    pass


@csrf_exempt
@require_http_methods('GET')
def GetSportList(request):
    
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录",'data':[]})
    try:
        data =[ t.sportName for t in Sport.objects.all()]
        return JsonResponse({'status':0,'data':data})
    except Exception as e:
        return JsonResponse({'status':-2,'msg':str(e),'data':[]})


@csrf_exempt
@require_http_methods('POST')
def SubmitFeedBack(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})
    try:
        userid = User.objects.get(username=request.session['username'])
        data = json.loads(request.body)
        content = data["content"] 
        FeedBack.objects.create(createUser=userid,content=content)
        return JsonResponse({'status':0,'msg':'反馈成功!'})
    except  Exception as e:
        return JsonResponse({'status':-2,'msg':str(e)})

@csrf_exempt
@require_http_methods('POST')
def GetMyArticles(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})   
    try:
        user = User.objects.get(username=request.session['username'])
        articles = [{"articleId":t.articleId,"username":user.username,"title":t.title,"content":t.content,"createTime":t.create_at,"updateTime":t.update_at} for t in Article.objects.filter(userId=user)]
        return JsonResponse({'status':0,'data':articles})
    except Exception as e:
        return JsonResponse({'status':-2,'msg':str(e)})

@csrf_exempt
@require_http_methods('GET')
def GetMyTeam(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})   
    
    try:
        user = User.objects.get(username=request.session['username'])
        return JsonResponse({'data':list(Team.objects.filter(createPerson=user).values()),'status':0})
    except Exception as e:
        return JsonResponse({'status':-2,'msg':str(e)})

@csrf_exempt
@require_http_methods('GET')
def GetTeams(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})   
    try:
        return JsonResponse({'status':0,'data':list(Team.objects.filter(teamState__regex=r'R|O').values())})
    except Exception as e:
        return JsonResponse({'status':-2,'data':[],'msg':str(e)})
    
@csrf_exempt
@require_http_methods('POST')
def GetTeamDetails(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})   
    try:
        data = json.loads(request.body)
        teamId = data['teamId']
        team = Team.objects.get(teamId=teamId)
        user = User.objects.get(username=request.session['username'])
        createId = team.createPerson.userid
        isMember = False
        members = [{'userId':t.userId.userid,'username':t.userId.username,'avatarAddress': t.userId.avatar} for t in TeamMember.objects.filter(teamId=team) ]
        for t in members:
            if user.userid in t.values():
                isMember = True
                break
        responseData = {'teamId':teamId,'teamName':team.teamName,'createPersonName':team.createPerson.username,'curPersonCnt':team.curPersonCnt,
                        'maxPersonCnt':team.maxPerson,'createTime':team.createTime,'startTime':team.startTime,'endTime':team.endTime,
                        'teamState':team.teamState,'members': members}
        return JsonResponse({'status':0,'data': responseData,'self':createId ==user.userid,'isMember':isMember})
    except Exception as e:
        return JsonResponse({'status':-2,'data':[],'msg':str(e)})

@csrf_exempt
@require_http_methods('POST')
def StartTeam(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})   
    try:
        data = json.loads(request.body)
        teamId = data['teamId']
        user = User.objects.get(username=request.session['username'])
        team = Team.objects.get(teamId=teamId)
        if team is None:
            return JsonResponse({'status':-5,'msg':'该队伍不存在!'})
        createId = team.createPerson.userid
        if user.userid != createId:
            return JsonResponse({'status':-3,'msg':'操作者不是创建用户'})
        if team.teamState != 'R':
            return JsonResponse({'status':-4,'msg':'该队伍并非正在招新中,无法开始运动'})
        team.teamState = 'O'
        team.startTime = timezone.now()
        team.save()
        return JsonResponse({'status':0})
    except Exception as e:
        return JsonResponse({'status':-2,'data':[],'msg':str(e)})
     


@csrf_exempt
@require_http_methods('GET')
def TestPassword(request):
    password = '12345678'
    password_hash = make_password(password)
    return JsonResponse({'status':check_password(password=password,encoded=password_hash)})

@csrf_exempt
@require_http_methods('POST')
def UploadAvatar(request):
    pass