from django.contrib import admin
############### Custom imports ########################
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from CustomUserApp.models import CustomUser
########## Register your models here. ###################
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='Password Confirmation',widget=forms.PasswordInput)

    class Meta:
        model=CustomUser
        fields=('first_name','last_name','email','sex','github_url','profile_picture','is_active','is_staff','is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit==True:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model=CustomUser
        fields=('first_name','last_name','email','sex','github_url','profile_picture','is_active','is_staff','is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form  = UserChangeForm
    add_form = UserCreationForm

    #Fields To Display When Displaying List Of User
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff','is_superuser','last_login')
    #Fields To Display When Displaying List Of User
    list_filter = ('is_superuser',)
    #Fields To Display When Editing Users
    fieldsets=(
        (None,{'fields':('email','password')}),
        ('Personal Info',{'fields':('first_name','last_name','sex')}),
        ('Social',{'fields':('github_url','profile_picture')}),
        ('Premissions',{'fields':('is_active','is_staff','is_superuser','groups','user_permissions',)}),
        ('Activity',{'fields':('last_login','date_joined')}),
    )
    #Fields To Display When Creating New Users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name','sex','password1','password2','github_url','profile_picture','is_active','is_staff','is_superuser',),
        }),
    )
    search_fields = ('email',)
    ordering = ('last_login',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)
