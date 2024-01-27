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
            # Save the list as a JSON array without escaped double quotes
            print(values)


            # TODO vielleicht ist der DUMP ja nichts das richtige
            return values
        return None

    def init(self, args, **kwargs):
        super().init(args, **kwargs)

        # If instance has business_fields, populate business_fields_input with a string
        if self.instance.business_fields:
            self.fields['business_fields_input'].initial = ', '.join(json.loads(self.instance.business_fields))
            # You can customize the separator based on your preferences

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
