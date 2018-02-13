from django import forms
from freelancers.models.service import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['id', 'icon', 'objective', 'description']

    def save(self, commit=True):
        service = super(ServiceForm, self).save(commit=False)
        if commit:
            service.save()
        return service
