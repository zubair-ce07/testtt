from django.views.generic import DetailView
from django.contrib.auth.models import User
from freelancers.models.profile import Profile
from freelancers.models.service import Service


class DetailView(DetailView):
    model = User
    template_name = "user/freelancer/detail.html"
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        # context.profile = context.get('object').get_profile()
        context['profile'] = Profile.objects.filter(
            user=context.get('object')).first()
        context['services'] = Service.objects.filter(
            user=context.get('object'))

        return context
