from django import forms
from .models import Company, Job
import json


class EmailForm(forms.Form):
    pass


class CompanyForm(forms.ModelForm):
    business_fields_input = forms.CharField(
        label='Business Fields',
        help_text='Enter different strings separated by commas',
        required=False,
    )

    class Meta:
        model = Company
        fields = '__all__'

    def clean_business_fields_input(self):
        data = self.cleaned_data['business_fields_input']
        if data:
            # Convert comma-separated values to a Python list
            values = [s.strip() for s in data.split(',')]
            return values
        return None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print("hello")

        # If instance has business_fields, populate business_fields_input with a string
        if self.instance.business_fields:
            print("hello")
            print(self.instance.business_fields)
            try:
                print(self.instance.business_fields)
                business_fields_str = ', '.join(self.instance.business_fields)
                print(business_fields_str)
                self.fields['business_fields_input'].initial = business_fields_str

            except json.JSONDecodeError as e:
                # Handle the case where business_fields is not a valid JSON string
                print(f"Error decoding business_fields: {e}")
        else:
            print("no business_fields")

    def save(self, commit=True):
        # Set the value of business_fields before saving
        self.instance.business_fields = self.cleaned_data['business_fields_input']
        return super().save(commit)



class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'


class LocationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
