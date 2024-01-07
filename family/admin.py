from django.contrib import admin
from .models import member , family , game , score , room , message
from django.forms import Textarea , TextInput
from django.contrib.auth.admin import UserAdmin

class MemberConfig(UserAdmin):
    search_fields = ('user_name' , 'firstName' , 'lastName')
    list_display = ('user_name' , 'firstName' , 'lastName')
    ordering = ('-created',)
    fieldsets = (
        (None , {'fields':('email' , 'password', 'user_name' ,'firstName','middleName' , 'lastName' , 'FID')}),
        ('Permissions' , {'fields':('is_staff' , 'is_active')}),
        ('Personal' , {'fields':('gender' , 'maritalStatus' , 'jobOrg' , 'birthDay' ,'mobileNo' ,'mother', 'father','spouse' , 'kidsCount')}),
        ('Location' , {'fields':('address1','pinCode' , 'city' , 'country' , 'lat' , 'lng')}),
        ('Intrest' , {'fields':('sport','movie' , 'book' , 'present')}),
    )
    add_fieldsets = (
        (None , {
            'classes':('wide',),
            'fields':('email' , 'user_name' ,'firstName','middleName' , 'lastName' , 'FID' , 'password1' , 'password2')
        }),
    )

admin.site.register(member , MemberConfig)
admin.site.register(family)
admin.site.register(game)
admin.site.register(score)
admin.site.register(room)
admin.site.register(message)
