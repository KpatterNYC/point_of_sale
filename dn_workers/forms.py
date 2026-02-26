import re
from django import forms
from django.core.exceptions import ValidationError

from dn_workers import models

INPUT={"class":"input input-sm w-full"}
class WorkerProfileForm(forms.ModelForm):
    class Meta:
        model=models.WorkerProfile
        fields=["first_name","last_name","phone_number"]
        widgets={
            "first_name": forms.TextInput(attrs=INPUT),
            "last_name":forms.TextInput(attrs=INPUT),
            "phone_number":forms.TextInput(attrs=INPUT|{"type":"tel","pattern":"^0(7|1)[0-9]{8}$"})
        }
        
    
    def clean_phone_number(self):
        phone_number=self.cleaned_data.get("phone_number")
        if phone_number:
            reg_ex=re.compile(r"^0(7|1)[0-9]{8}$")
            if not reg_ex.match(phone_number):
                raise ValidationError(message="Invalid phone number.")
            return phone_number
    
    def clean_first_name(self):
        first_name:str=self.cleaned_data.get("first_name")
        if first_name:
            return first_name.strip()
        
        return first_name
        
    def clean_last_name(self):
        last_name:str=self.cleaned_data.get("last_name")
        if last_name:
            return last_name.strip()
        
        return last_name
    