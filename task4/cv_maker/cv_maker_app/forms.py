from django import forms
from .models import BasicInformation, Education, Experience


class BasicInformationForm(forms.ModelForm):
    user_id = forms.IntegerField()
    name = forms.CharField(max_length=30)
    date_of_birth = forms.DateTimeField()
    contact_number = forms.IntegerField()
    address = forms.CharField(max_length=255)
    email = forms.EmailField()
    CHOICES = [('1', 'Beginner'),
               ('2', 'Little Knowledge'),
               ('3', 'Intermediate'),
               ('4', 'Advance'),
               ('5', 'Expert')
               ]
    skill1 = forms.CharField(max_length=30, required=False)
    skill2 = forms.CharField(max_length=30, required=False)
    skill3 = forms.CharField(max_length=30, required=False)
    skill4 = forms.CharField(max_length=30, required=False)
    skill5 = forms.CharField(max_length=30, required=False)
    skill1_level = forms.ChoiceField(widget=forms.RadioSelect, required=False, choices=CHOICES)
    skill2_level = forms.ChoiceField(widget=forms.RadioSelect, required=False, choices=CHOICES)
    skill3_level = forms.ChoiceField(widget=forms.RadioSelect, required=False, choices=CHOICES)
    skill4_level = forms.ChoiceField(widget=forms.RadioSelect, required=False, choices=CHOICES)
    skill5_level = forms.ChoiceField(widget=forms.RadioSelect, required=False, choices=CHOICES)
    hobby1 = forms.CharField(max_length=30, required=False)
    hobby2 = forms.CharField(max_length=30, required=False)
    hobby3 = forms.CharField(max_length=30, required=False)
    reference1 = forms.CharField(max_length=30, required=False)
    reference2 = forms.CharField(max_length=30, required=False)

    class Meta:
        model = BasicInformation
        fields = ['user_id',
                  'name',
                  'date_of_birth',
                  'contact_number',
                  'address',
                  'email',
                  'skill1',
                  'skill2',
                  'skill3',
                  'skill4',
                  'skill5',
                  'skill1_level',
                  'skill2_level',
                  'skill3_level',
                  'skill4_level',
                  'skill5_level',
                  'hobby1',
                  'hobby2',
                  'hobby3',
                  'reference1',
                  'reference2',
                  ]


class EducationForm(forms.ModelForm):
    user_id = forms.IntegerField()
    degree = forms.CharField(max_length=30)
    institute = forms.CharField(max_length=100)
    starting_date = forms.DateTimeField()
    ending_date = forms.DateTimeField(required=False)
    city = forms.CharField(max_length=30)
    description = forms.CharField(max_length=255)

    class Meta:
        model = Education
        fields = [
            'user_id',
            'degree',
            'institute',
            'starting_date',
            'ending_date',
            'city',
            'description',
        ]


class ExperienceForm(forms.ModelForm):
    user_id = forms.IntegerField()
    organization = forms.CharField(max_length=30)
    position = forms.CharField(max_length=30)
    starting_date = forms.DateTimeField()
    ending_date = forms.DateTimeField(required=False)
    job_description = forms.CharField(max_length=255)
    city = forms.CharField(max_length=30)

    class Meta:
        model = Experience
        fields = [
            'user_id',
            'organization',
            'position',
            'starting_date',
            'ending_date',
            'job_description',
            'city',
        ]
