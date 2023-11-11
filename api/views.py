from datetime import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_http_methods,require_safe
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from .models import FeedBack, Team, TeamMember, User,Sport,Article
from uuid import uuid4
import json
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
        user = User.objects.create(username=username,password=password,email=email,phone=phone)
        user.save()
    except Exception as e:
        return JsonResponse({'status':-2,"msg":str(e)})
    return JsonResponse({"status":0})
    
    
@csrf_exempt
@require_http_methods('POST')
def SignIn(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({"status":-1})
    try:
        if check_password(password,user.password):
            request.session['session'] = str(uuid4())
            request.session['username'] = username
            print(password)
            return JsonResponse({'status':0})
        else:
            return JsonResponse({'status':-2})
    except Exception as e:
        return JsonResponse({'status':-3,'msg':str(e)})

@csrf_exempt
@require_http_methods('GET')
def UserInfo(request):
    print(request.body)
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({'status':-1,"msg":"none!"})
    t = data.get('username')
    try:
        user = User.objects.filter(username=t)[0]
    except:
        return JsonResponse({'status':-1,"msg":"none!"})    
    return JsonResponse({"status":0,"msg":user.password})

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
    pass 


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
        team.save()
        teamMember = TeamMember.objects.create(teamId=team,userId=user)
        teamMember.save()
        return JsonResponse({'status':0})
    except Exception as e:
        return JsonResponse({'status':-2,'msg':str(e)})
    

@csrf_exempt
@require_http_methods('POST')
def EndTeam(request):
    pass


@csrf_exempt
@require_http_methods('POST')
def JoinTeam(request):
    pass


@csrf_exempt
@require_http_methods('POST')
def LeaveTeam(request):
    pass


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
        feedBack = FeedBack.objects.create(createUser=userid,content=content)
        feedBack.save()
        return JsonResponse({'status':0,'msg':'反馈成功!'})
    except  Exception as e:
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
        return JsonResponse({'status':0,'data':list(Team.objects.all().values())})
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
        responseData = {'teamId':teamId,'teamName':team.teamName,'createPersonName':request.session['username'],'curPersonCnt':team.curPersonCnt,
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
        userId = User.objects.get(username=request.session['username'])
        createId = data['createPerson']
        if userId != createId:
            return JsonResponse({'status':-3,'msg':'操作者不是创建用户'})
        team = Team.objects.get(teamId=teamId)
        if team.teamState != 'R':
            return JsonResponse({'status':-4,'msg':'该队伍并非正在招新中,无法开始运动'})
        team.teamState = 'O'
        team.startTime = timezone.now()
        team.save()
        return JsonResponse({'status':0})
    except Exception as e:
        return JsonResponse({'status':-2,'data':[],'msg':str(e)})
     
@csrf_exempt
@require_http_methods('POST')
def EndTeam(request):
    if 'username' not in request.session or 'session' not in request.session:
        return JsonResponse({'status':-1,'msg':"未登录"})   
    try:
        data = json.loads(request.body)
        teamId = data['teamId']
        userId = User.objects.get(username=request.session['username'])
        createId = data['createPerson']
        if userId != createId:
            return JsonResponse({'status':-3,'data':[],'msg':'操作者不是创建用户'})
        team = Team.objects.get(teamId=teamId)
        team.state = 'E'
        team.endTime = timezone.now()
        team.save()
        return JsonResponse({'status':0})
    except Exception as e:
        return JsonResponse({'status':-2,'data':[],'msg':str(e)})

