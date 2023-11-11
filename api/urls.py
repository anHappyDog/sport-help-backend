from django.urls import path 
from .views import SignUp,SignIn,GetUserInfo,SportInfo,ForgetPassword,SignOut,GetSportList,CreateTeam,SubmitFeedBack,GetMyTeam,GetTeams
from .views import GetTeamDetails,StartTeam,EndTeam,TestPassword,DestroyTeam,JoinTeam,LeaveTeam,GetSportRecord,UploadAvatar,GetAvatarAndUsername
urlpatterns = [
    path('SignUp',SignUp,name='SignUp'),
    path('SignIn',SignIn,name='SignIn'),
    path('GetUserInfo',GetUserInfo,name='GetUserInfo'),
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
    path('TestPassword',TestPassword,name='TestPassword'),
    path('DestroyTeam',DestroyTeam,name='DestroyTeam'),
    path('JoinTeam',JoinTeam,name='JoinTeam'),
    path('LeaveTeam',LeaveTeam,name='LeaveTeam'),
    path('GetSportRecord',GetSportRecord,name='GetSportRecord'), 
    path('UploadAvatar',UploadAvatar,name='UploadAvatar'), 
    path('GetAvatarAndUsername',GetAvatarAndUsername,name='GetAvatarAndUsername'),     
]
