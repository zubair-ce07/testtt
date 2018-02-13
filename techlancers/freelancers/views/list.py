from django.contrib.auth.models import User
from django.views.generic import ListView


class ListView(ListView):
    model = User
    template_name = "user/freelancer/list.html"
    queryset = User.objects.filter(groups__name='Freelancer')

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        new_context = User.objects.filter(
            username__contains=filter_val,
            groups__name='Freelancer'
        )
        return new_context
