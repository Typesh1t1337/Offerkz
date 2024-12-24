from django.urls import path
from account.views import *

urlpatterns = [
    path('login/',user_login,name='login'),
    path('register/',user_register, name='register'),
    path('forget/',forget,name='forget'),
    path('cashin/<str:user_name_path>/',cash_in,name='cash_in'),
    path('cashout/<str:user_name_path>/',cash_out,name='cash_out'),
    path('logout',user_logout,name='logout'),
    path('profile/<str:user_name_path>/',profile,name='profile'),
    path('edit/profile/<str:user_name_path>/',edit_profile,name='edit'),
    path('edit/photo/<str:user_name_path>/',edit_avatar,name='avatar'),
    path('edit/password/<str:user_name_path>/' ,edit_password, name='password'),
    path('confirmation/' ,user_not_active,name='confirmation'),
    path('confirm/<uidb64>/<token>/',confirm_email,name='confirm_email')
]