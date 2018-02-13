from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from freelancers.forms.profile_form import ProfileForm
from freelancers.forms.service_form import ServiceForm
from freelancers.models.profile import Profile
from freelancers.models.service import Service
from django.forms import modelformset_factory


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    model = User
    template_name = "user/freelancer/profile.html"

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user).first()
        profile_form = ProfileForm(instance=profile)
        ServiceFormSet = modelformset_factory(
            Service, form=ServiceForm, extra=0)
        service_forms = ServiceFormSet(
            queryset=Service.objects.filter(user=request.user))
        context = self.get_context_data(**kwargs)
        context['profile'] = vars(profile)
        context['profile_form'] = profile_form
        context['service_forms'] = service_forms
        return self.render_to_response(context)
