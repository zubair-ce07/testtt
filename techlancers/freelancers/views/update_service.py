from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import UpdateView
from freelancers.forms.service_form import ServiceForm
from freelancers.models.service import Service
from django.forms import modelformset_factory


class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm

    def get_object(self):
        return Service.objects.get(pk=self.request.POST.get('serviceID'))

    def get_context_data(self, **kwargs):
        context = super(ServiceUpdateView, self).get_context_data(**kwargs)
        ServiceFormSet = modelformset_factory(Service, form=ServiceForm)
        context['services_formset'] = ServiceFormSet(self.request.POST)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['services_formset']
        valid_forms = [form.save()
                       for form in formset.forms if form.is_valid()]
        for service_form in valid_forms:
            instances = service_form.save()
            formset.instance = instances
            return HttpResponse("success")
