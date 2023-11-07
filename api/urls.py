from django.urls import path 
from .views import SignUp,SignIn,UserInfo,SportInfo,ForgetPassword,SignOut
urlpatterns = [
    path('SignUp',SignUp,name='SignUp'),
    path('SignIn',SignIn,name='SignIn'),
    path('UserInfo',UserInfo,name='UserInfo'),
    path('SportInfo',SportInfo,name='SportInfo'),
    path('ForgetPassword',ForgetPassword,name='ForgetPassword'),
    path('SignOut',SignOut,name='SignOut'),
]
