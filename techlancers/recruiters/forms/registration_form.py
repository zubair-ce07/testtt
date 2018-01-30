from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


class RegistrationForm(UserCreationForm):

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.save()
            new_group, created = Group.objects.get_or_create(name='Recruiter')
            user.groups.set([new_group])
        return user
