from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
       return HttpResponseRedirect('active')
    return render(request,"main/index.html")

@login_required
def active(request):
    username = request.user.username
    size_of_name_text = 16
    if len(username) >6:
        size_of_name_text =14
    customs = {
        "username": username,
        'linkFind':'link-grey',
        'linkUpload':'link-grey',
        'sizeOfName':size_of_name_text,
    }
    return render(request,"main/mainActive.html",customs)

