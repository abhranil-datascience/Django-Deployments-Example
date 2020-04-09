from django.shortcuts import render
from CustomUserApp.forms import UserRegistrationForm,UserLoginForm
from CustomUserApp.models import CustomUser
from django import forms
# Create your views here.
def index(request):
    return render(request,"CustomUserApp/Index.html")

def registration(request):
    reg_form=UserRegistrationForm()
    registration_form_dict={'registration_form':reg_form,'registration_success':False}
    if request.method == "POST":
        populated_reg_form = UserRegistrationForm(data=request.POST)
        if populated_reg_form.is_valid():
            fname=populated_reg_form.cleaned_data['FirstName']
            lname=populated_reg_form.cleaned_data['Lastname']
            email=populated_reg_form.cleaned_data['Email']
            password=populated_reg_form.cleaned_data['Password']
            sex=populated_reg_form.cleaned_data['Sex']
            portfolio=populated_reg_form.cleaned_data['Portfolio']
            if 'ProfilePicture' in request.FILES:
                pic=request.FILES['ProfilePicture']
            else:
                pic=None
            new_user=CustomUser(first_name=fname,last_name=lname,email=email,sex=sex,github_url=portfolio,profile_picture=pic)
            try:
                new_user.save()
                new_user.set_password(password)
                new_user.save()
                registration_form_dict={'registration_form':populated_reg_form,'registration_success':True}
                return render(request,"CustomUserApp/Registration.html",context=registration_form_dict)
            except:
                print("Duplicate Record!!")
                registration_form_dict={'registration_form':populated_reg_form,'registration_success':False,'error_message':"Error - Duplicate Email ID"}
                return render(request,"CustomUserApp/Registration.html",context=registration_form_dict)
        else:
            print("Invalid Form")
            registration_form_dict={'registration_form':populated_reg_form,'registration_success':False}
            return render(request,"CustomUserApp/Registration.html",context=registration_form_dict)
    return render(request,"CustomUserApp/Registration.html",context=registration_form_dict)

from django.contrib.auth import authenticate, login

def user_login(request):
    login_form=UserLoginForm()
    login_form_dict={'login_form':login_form,'login_success':False}
    if request.method=="POST":
        populated_login_form=UserLoginForm(data=request.POST)
        if populated_login_form.is_valid():
            username=populated_login_form.cleaned_data['Email']
            password=populated_login_form.cleaned_data['Password']
            curruser = authenticate(request, username=username, password=password)
            if curruser is not None:
                print("User Authenticated Successfully")
                if curruser.is_active:
                    login(request,curruser)
                    login_form_dict={'login_form':populated_login_form,'login_success':True}
                    return render(request,"CustomUserApp/Login.html",context=login_form_dict)
                else:
                    print("User Authentication Successful but not in active state")
                    login_form_dict={'login_form':populated_login_form,'login_success':False,'error_message':"User is not active."}
            else:
                print("User Authentication Unsuccessful")
                login_form_dict={'login_form':populated_login_form,'login_success':False,'error_message':"Invalid Login Details"}
        else:
            login_form_dict={'login_form':populated_login_form,'login_success':False}
            return render(request,"CustomUserApp/Login.html",context=login_form_dict)
    return render(request,"CustomUserApp/Login.html",context=login_form_dict)

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def user_logout(request):
    logout(request)
    return render(request,"CustomUserApp/Index.html")

@login_required
def display_user_list(request):
    list_of_users=CustomUser.objects.all()
    user_list_dict={'userlist':list_of_users}
    return render(request,"CustomUserApp/DisplayUserList.html",context=user_list_dict)
