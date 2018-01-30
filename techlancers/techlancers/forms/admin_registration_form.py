from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


class AdminRegistrationForm(UserCreationForm):

    def save(self, commit=True):
        user = super(AdminRegistrationForm, self).save(commit=False)
        if commit:
            user.save()
            new_group, created = Group.objects.get_or_create(name='Admin')
            user.groups.set([new_group])
        return user
