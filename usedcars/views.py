from .models import UsedCars
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'usedcars/index.html'
    context_object_name = 'wheels'

    def get_queryset(self):
        return UsedCars.objects.all()


class DetailView(generic.ListView):
    model = UsedCars
    template_name = 'usedcars/temp.html'