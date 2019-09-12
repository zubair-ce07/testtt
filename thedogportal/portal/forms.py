from django import forms

class UploadForm(forms.Form):
    title = forms.CharField(label='Title for the post', max_length=255)
    image = forms.ImageField(label='Upload Image')

# class SettingsForm(forms.Form):
#     bio = forms.CharField(max_length=255, label='Bio')
#     location = forms.CharField(max_length=30, label='Country')
#     birth_date = forms.DateField(label='Birthday')
#     widget = forms.DateInput(attrs={'class':'datepicker form-control', 'placeholder':'Select a date'}, format='%d/%m/%Y')
