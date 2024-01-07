from django.forms import ModelForm , forms
from django.db import models
from django.forms import CheckboxInput, ModelChoiceField,ModelMultipleChoiceField
from django.contrib.auth.forms import UserCreationForm  , UserChangeForm
from .models import member
# from django.contrib.auth.models import User



class MemberForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['required'] = 'required'

    class Meta:
        model = member
        fields = ['FID' , 'email' ,  'user_name','firstName','lastName' , 'gender' , 'city', 'pinCode' , 'country' ,'password1' , 'password2']


class MemberForm1(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = member
        fields = ['middleName' ,'email' ,'mobileNo' ,'jobOrg','maritalStatus','mother','father','spouse', 'address1' , 'country' , 'city','sport','movie' ,'book','present' , 'pinCode']
    

    


