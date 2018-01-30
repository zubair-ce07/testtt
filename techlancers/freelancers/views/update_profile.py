from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import UpdateView
from freelancers.models.profile import Profile
from freelancers.forms.profile_form import ProfileForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm

    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return HttpResponse("success")
        return HttpResponse("done")
