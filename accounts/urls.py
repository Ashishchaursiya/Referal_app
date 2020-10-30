from django.urls import path
from .views import Signup,Login,Logout,showdata,Buy,checkout,success,Register,Signin
from django.urls import path,include
urlpatterns=[
    path('', include('django.contrib.auth.urls')),
    path('register/',Register,name="register"),
    path('Sign_page/',Signin,name="signin"),
    path('signup/',Signup,name="signup"),
    path('login',Login,name="login"),
    path('logout',Logout,name="logout"),
    path('profile/',showdata,name="show"),
    path('buy/',Buy,name="buy"),
    path('checkout/',checkout,name="checkout"),
    path('success/<str:referal>',success,name="success")
]