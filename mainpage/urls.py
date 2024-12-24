from django.urls import path
from mainpage.views import *

urlpatterns = [
    path("",index,name="index"),
    path("active",active,name="active"),
]

