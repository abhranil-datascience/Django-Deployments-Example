app_name='CustomUserApp'
from django.urls import path,re_path,include
from CustomUserApp import views
urlpatterns = [
    re_path(r'register/$',views.registration,name="RegistrationPage"),
    re_path(r'login/$',views.user_login,name="LoginPage"),
    re_path(r'userlist/$',views.display_user_list,name="DisplayUsersPage"),
    re_path(r'logout/$',views.user_logout,name="Logout")
]
