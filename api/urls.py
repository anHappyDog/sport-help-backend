from django.urls import path 
from .views import SignUp,SignIn,UserInfo,SportInfo,ForgetPassword,SignOut,GetSportList,CreateTeam,SubmitFeedBack,GetMyTeam,GetTeams
from .views import GetTeamDetails,StartTeam,EndTeam
urlpatterns = [
    path('SignUp',SignUp,name='SignUp'),
    path('SignIn',SignIn,name='SignIn'),
    path('UserInfo',UserInfo,name='UserInfo'),
    path('SportInfo',SportInfo,name='SportInfo'),
    path('ForgetPassword',ForgetPassword,name='ForgetPassword'),
    path('SignOut',SignOut,name='SignOut'),
    path('GetSportList',GetSportList,name='GetSportList'),
    path('CreateTeam',CreateTeam,name='CreateTeam'),
    path('SubmitFeedBack',SubmitFeedBack,name='SubmitFeedBack'),
    path('GetMyTeam',GetMyTeam,name='GetMyTeam'),
    path('GetTeams',GetTeams,name='GetTeams'),
    path('GetTeamDetails',GetTeamDetails,name='GetTeamDetails'),
    path('StartTeam',StartTeam,name='StartTeam'),
    path('EndTeam',EndTeam,name='EndTeam'),
    
    
]
