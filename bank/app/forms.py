from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name','mobile', 'email','gender', 'aadhar', 'father_name', 'dob',  'state','address', 'photo']