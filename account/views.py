import array

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model,update_session_auth_hash
from django.utils.encoding import force_str

from django.contrib.auth.tokens import default_token_generator
from .forms import UpdatePhotoForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .utils import send_html_message
def user_login(request):
    if request.method == "POST":
        login = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=login, password=password)
        user_to_check = get_user_model().objects.filter(username=login).first()
        if user is not None:
            if user_to_check.is_verified:
                auth_login(request, user)
                return HttpResponseRedirect('/active')
            else:
               logout(request)
               return redirect('confirmation')
        else:
            return render(request, 'registration/login.html',{'error':'Неверный логин либо пароль'})

    return render(request, "registration/login.html")



def user_not_active(request):
    return render(request, 'account/activate_account.html')

def user_register(request):
    CustomUser = get_user_model()
    if request.method == "POST":
        login = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]


        if password != password2:
            messages.error( request, "Пароли не совпадают")
            return redirect('register')
        if CustomUser.objects.filter(email=email).exists():
           messages.error(request,"Пользователь с такой почтой уже существует")
           return redirect('register')
        if CustomUser.objects.filter(username=login).exists():
           messages.error(request,"Это имя пользователя уже занято")
           return redirect('register')

        user =CustomUser.objects.create_user(username=login, email=email, password=password)

        auth_login(request, user)

        send_html_message(email,login)

        logout(request)

        return redirect('login')



    return render(request, "registration/register.html")



def confirm_email(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise Http404("Ссылка для подтверждения уже недействительна")


    if default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        auth_login(request, user)

        return redirect('active')

    else:
        raise Http404("Ссылка для подтверждения уже недействительна")


    return render(request,'registration/confirmEmail.html')

def forget(request):
    return render(request, "registration/forget.html")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def profile(request,user_name_path):
    user = request.user
    user_name = request.user.username
    user_name_size = 28

    if user.first_name and user.last_name:
        user_name_size = 20

    size_of_name_text = 16
    if len(user_name) > 6:
        size_of_name_text = 14

    nav_status = ['nav-active', 'nav-not-active', 'nav-not-active', 'nav-not-active', 'nav-not-active']
    a_status = ['a-active', 'a-not-active', 'a-not-active', 'a-not-active', 'a-not-active']

    options = {
        'user': user,
        'linkFind':'link-grey',
        'linkUpload':'link-grey',
        'linkProfile':'link-green',
        'linkLogout':'link-grey',
        'user_path': user_name_path,
        'user_name_size': user_name_size,
        'sizeOfName': size_of_name_text,
        'nav_status': nav_status,
        'a_status': a_status,
    }




    return render(request, "account/profile.html",options)

@login_required
def edit_profile(request, user_name_path):
    User = get_user_model()
    user = request.user
    user_name = request.user.username
    user_name_size = 28
    size_of_name_text = 16
    if len(user_name) > 6:
        size_of_name_text = 14

    if user.first_name and user.last_name:
        user_name_size = 20

    verify_code = 000000

    is_new_email = False
    is_new_email_verified = False
    error_mail = ""
    error_login = ""
    nav_status = ['nav-not-active', 'nav-not-active', 'nav-active', 'nav-not-active', 'nav-not-active']
    a_status = ['a-not-active', 'a-not-active', 'a-active', 'a-not-active', 'a-not-active']

    options = {
        'user': user,
        'linkFind': 'link-grey',
        'linkUpload': 'link-grey',
        'linkProfile': 'link-green',
        'linkLogout': 'link-grey',
        'user_name_size': user_name_size,
        'user_name_path': user_name_path,
        'error_login': error_login,
        'sizeOfName': size_of_name_text,
        'a_status': a_status,
        'nav_status': nav_status,
    }

    if request.method == 'POST':
        login = request.POST["login"]
        email = request.POST["email"]
        first_name = request.POST.get("first_name","").strip()
        last_name = request.POST.get("last_name","").strip()

        if login != user.username:
            if User.objects.filter(username=login).exclude(pk = user.pk).exists():
                error_login ="Логин уже занят"
                options['error_login'] = error_login
                return render(request, 'account/changeData.html',options)
        if email != user.email:
            is_new_email = True
            verify_code_from_post = request.POST["verify_code"]
            if verify_code_from_post == verify_code:
                is_new_email_verified = True
                user.full_clean()
                user.save()
            else:
                error_mail = "Неверный код подтверждения!"


        user.username = login
        user.first_name = first_name
        user.last_name = last_name
        user.full_clean()
        user.save()
        return HttpResponseRedirect('/accounts/profile/' + user_name_path)




    return render(request,'account/changeData.html',options)

@login_required
def edit_avatar(request, user_name_path):
    user = request.user


    user_name_size = 20  if user.first_name and user.last_name else 28
    size_of_name_text = 14 if len(user.username) > 6 else 16

    if request.method == "POST":
        form = UpdatePhotoForm(request.POST, request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/accounts/profile/{user_name_path}')
    else:
        form = UpdatePhotoForm()

    nav_status = ['nav-not-active', 'nav-not-active', 'nav-active', 'nav-not-active', 'nav-not-active']
    a_status = ['a-not-active', 'a-not-active', 'a-active', 'a-not-active', 'a-not-active']

    options = {
        'user': user,
        'linkFind': 'link-grey',
        'linkUpload': 'link-grey',
        'linkProfile': 'link-green',
        'linkLogout': 'link-grey',
        'user_name_size': user_name_size,
        'sizeOfName': size_of_name_text,
        'nav_status': nav_status,
        'a_status': a_status,
        'form': form,
        }

    return render(request, "account/changeAvatar.html",options)

@login_required
def edit_password(request, user_name_path):
    user = request.user

    user_name_size = 20 if user.first_name and user.last_name else 28
    size_of_name_text = 14 if len(user.username) > 6 else 16

    if request.method == "POST":
        form_update_password = PasswordChangeForm(request.user,request.POST)
        if form_update_password.is_valid():
            user.set_password(form_update_password.cleaned_data["new_password1"])
            user.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(f'/accounts/profile/{user_name_path}')
    else:
        form_update_password = PasswordChangeForm(request.user)

    nav_status = ['nav-not-active','nav-not-active','nav-active','nav-not-active','nav-not-active']
    a_status = ['a-not-active','a-not-active','a-active','a-not-active','a-not-active']

    options ={
        'user': user,
        'linkFind': 'link-grey',
        'linkUpload': 'link-grey',
        'linkProfile': 'link-green',
        'linkLogout': 'link-grey',
        'user_name_size': user_name_size,
        'sizeOfName': size_of_name_text,
        'form': form_update_password,
        'nav_status': nav_status,
        'a_status': a_status,
        }

    return render(request, 'account/changePassword.html', options)

@login_required
def cash_in(request,user_name_path):
    user = request.user
    return HttpResponse(f'{user.username} - cash in')

@login_required
def cash_out(request,user_name_path):
    user = request.user
    return HttpResponse(f'{user.username} - cash out')



