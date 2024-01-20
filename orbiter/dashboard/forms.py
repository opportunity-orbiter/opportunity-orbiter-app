from django import forms
from .models import Company, Job


class EmailForm(forms.Form):
    pass


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'

class LocationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'