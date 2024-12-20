from django import forms
from .models import Address
from django.contrib.auth.forms import PasswordChangeForm
from user.models import CustomUser
from django.core.exceptions import ValidationError

class Addressform(forms.ModelForm):
    class Meta:
        model=Address
        fields=['name','address_title','state','city','pin','landmark','phone_number']


    def clean_pin(self):
        pin=self.cleaned_data.get('pin')
        if len(pin)!= 6 or not pin.isdigit():
            raise forms.ValidationError("Pin code must be 6 digits.")
        return pin

    def clean_phone_number(self):
        phone_number=self.cleaned_data.get('phone_number')
        if phone_number and (len(phone_number)!=10 or not phone_number.isdigit()):
            raise forms.ValidationError("Phone number must be 10 digits and contain  only numbers ")
        return phone_number

class UserpasswordchangeFrom(PasswordChangeForm):
    def clean_new_password1(self):
        new_password1=self.cleaned_data.get('new_password1')

        if len(new_password1)<8:
            raise ValidationError("password must be at least 8 characters ")
        return new_password1