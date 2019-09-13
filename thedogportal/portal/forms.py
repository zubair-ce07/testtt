from django import forms


class UploadForm(forms.Form):
    title = forms.CharField(label='Title for the post', max_length=255)
    image = forms.ImageField(label='Upload Image')
