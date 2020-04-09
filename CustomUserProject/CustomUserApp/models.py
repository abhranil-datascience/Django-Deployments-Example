from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
# Create your models here.
########################################## Custom User Manager ########################################################
class CustomUserManager(BaseUserManager):

    def create_user(self,first_name,last_name,email,sex=None,github_url=None,profile_picture=None,password=None,is_active=True,is_staff=False,
                    is_superuser=False):
        if not first_name:
            raise ValueError("FirstName is a mandatory Field.")
        if not last_name:
            raise ValueError("LastName is a mandatory Field.")
        if not email:
            raise ValueError("Email is a mandatory Field.")
        custom_user=self.model(first_name=first_name,last_name=last_name,email=email,sex=sex,github_url=github_url,profile_picture=profile_picture)
        custom_user.set_password(password)
        custom_user.is_staff=is_staff
        custom_user.is_active=is_active
        custom_user.is_superuser=is_superuser
        custom_user.save(using=self._db)
        return custom_user

    def create_superuser(self,first_name,last_name,email,sex=None,github_url=None,profile_picture=None,password=None):
        admin_user=self.create_user(first_name=first_name,last_name=last_name,email=email,sex=sex,github_url=github_url,
                                    profile_picture=profile_picture,password=password,is_active=True,is_staff=True,is_superuser=True)
        return admin_user
####################################### Custom User Definition ##########################################################
from django.utils import timezone
class CustomUser(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(verbose_name=('first name'),max_length=50,blank=False)
    last_name = models.CharField(verbose_name=('last name'),max_length=50,blank=False)
    email = models.EmailField(verbose_name=('email address'),max_length=255,unique=True,blank=False)
    sex = models.CharField(verbose_name=('sex'),max_length=1,blank=True,null=True)
    # password field supplied by AbstractBaseUser
    github_url = models.URLField(max_length=200,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='profile_pic',blank=True,null=True) # this folder will be inside /media/
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    # last_login field supplied by AbstractBaseUser

    objects=CustomUserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name',]

    def __str__(self):
        return self.email
