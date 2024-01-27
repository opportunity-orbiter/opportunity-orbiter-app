from django import forms
from .models import Company, Job, Location
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
        exclude = ['business_fields']

    def clean_business_fields_input(self):
        return self._clean_and_format_input('business_fields')
    
    def _clean_and_format_input(self, field_name):
        data = self.cleaned_data[f'{field_name}_input']
        if data:
            values = [s.strip() for s in data.split(',')]
            return values
        return None            
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields_to_handle = ['business_fields']

        for field_name in fields_to_handle:
            initial_value = self.instance.__dict__[field_name]
            print(initial_value)
            if initial_value:
                try:
                    formatted_value = ', '.join(initial_value)
                    self.fields[f'{field_name}_input'].initial = formatted_value
                    print(formatted_value)
                except json.JSONDecodeError as e:
                    print(f"Error decoding {field_name}: {e}")
            else:
                print(f"No {field_name}")

    def save(self, commit=True):
        fields_to_handle = ['business_fields']

        for field_name in fields_to_handle:
            self.instance.__dict__[field_name] = self.cleaned_data[f'{field_name}_input']

        return super().save(commit)



# old form without opening for addons
# class CompanyForm(forms.ModelForm):
#     business_fields_input = forms.CharField(
#         label='Business Fields',
#         help_text='Enter different strings separated by commas',
#         required=False,
#     )

#     class Meta:
#         model = Company
#         fields = '__all__'

#     def clean_business_fields_input(self):
#         data = self.cleaned_data['business_fields_input']
#         if data:
#             # Convert comma-separated values to a Python list  --> not JSON!
#             values = [s.strip() for s in data.split(',')]
#             return values
#         return None

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         print("testing initialization")

#         # If instance has business_fields, populate business_fields_input with a string
#         if self.instance.business_fields:
#             print(self.instance.business_fields)
#             try:
#                 print(self.instance.business_fields)
#                 business_fields_str = ', '.join(self.instance.business_fields)
#                 print(business_fields_str)
#                 self.fields['business_fields_input'].initial = business_fields_str

#             except json.JSONDecodeError as e:
#                 # Handle the case where business_fields is not a valid JSON string
#                 print(f"Error decoding business_fields: {e}")
#         else:
#             print("no business_fields")

#     def save(self, commit=True):
#         # Set the value of business_fields form input
#         self.instance.business_fields = self.cleaned_data['business_fields_input']
#         return super().save(commit)



#TODO, change company form to be modular like following: 
class JobForm(forms.ModelForm):
    tasks_and_responsibilities_input = forms.CharField(
        label='Tasks and Responsibilities',
        help_text='Enter different tasks and responsibilities separated by commas',
        required=False,
    )
    tech_skill_requirements_input = forms.CharField(
        label='Tech Skill Requirements',
        help_text='Enter different tech skill requirements separated by commas',
        required=False,
    )
    non_tech_skill_requirements_input = forms.CharField(
        label='Non-Tech Skill Requirements',
        help_text='Enter different non-tech skill requirements separated by commas',
        required=False,
    )
    benefits_input = forms.CharField(
        label='Benefits',
        help_text='Enter different benefits separated by commas',
        required=False,
    )

    class Meta:
        model = Job
        exclude = ['tasks_and_responsibilities', 'tech_skill_requirements', 'non_tech_skill_requirements', 'benefits']

    def clean_tasks_and_responsibilities_input(self):
        return self._clean_and_format_input('tasks_and_responsibilities')

    def clean_tech_skill_requirements_input(self):
        return self._clean_and_format_input('tech_skill_requirements')

    def clean_non_tech_skill_requirements_input(self):
        return self._clean_and_format_input('non_tech_skill_requirements')

    def clean_benefits_input(self):
        return self._clean_and_format_input('benefits')

    def _clean_and_format_input(self, field_name):
        data = self.cleaned_data[f'{field_name}_input']
        if data:
            values = [s.strip() for s in data.split(',')]
            return values
        return None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields_to_handle = ['tasks_and_responsibilities', 'tech_skill_requirements', 'non_tech_skill_requirements', 'benefits']

        for field_name in fields_to_handle:
            initial_value = self.instance.__dict__[field_name]
            print(initial_value)
            if initial_value:
                try:
                    formatted_value = ', '.join(initial_value)
                    self.fields[f'{field_name}_input'].initial = formatted_value
                    print(formatted_value)
                except json.JSONDecodeError as e:
                    print(f"Error decoding {field_name}: {e}")
            else:
                print(f"No {field_name}")

    def save(self, commit=True):
        fields_to_handle = ['tasks_and_responsibilities', 'tech_skill_requirements', 'non_tech_skill_requirements', 'benefits']

        for field_name in fields_to_handle:
            self.instance.__dict__[field_name] = self.cleaned_data[f'{field_name}_input']

        return super().save(commit)


class LocationForm(forms.ModelForm):
    business_fields_input = forms.CharField(
        label='Business Fields',
        help_text='Enter different strings separated by commas',
        required=False,
    )
    
    class Meta:
        model = Location
        exclude = ['business_fields']

    def clean_business_fields_input(self):
        return self._clean_and_format_input('business_fields')
    
    def _clean_and_format_input(self, field_name):
        data = self.cleaned_data[f'{field_name}_input']
        if data:
            values = [s.strip() for s in data.split(',')]
            return values
        return None            
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields_to_handle = ['business_fields']

        for field_name in fields_to_handle:
            initial_value = self.instance.__dict__[field_name]
            print(initial_value)
            if initial_value:
                try:
                    formatted_value = ', '.join(initial_value)
                    self.fields[f'{field_name}_input'].initial = formatted_value
                    print(formatted_value)
                except json.JSONDecodeError as e:
                    print(f"Error decoding {field_name}: {e}")
            else:
                print(f"No {field_name}")

    def save(self, commit=True):
        fields_to_handle = ['business_fields']

        for field_name in fields_to_handle:
            self.instance.__dict__[field_name] = self.cleaned_data[f'{field_name}_input']

        return super().save(commit)


    
