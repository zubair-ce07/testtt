from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.conf import settings

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .models  import Profile, Uploads

def homepage(request):
    if request.user.is_authenticated:
        template = loader.get_template('home.html')
        print("User ID: ", request.user.id)
        return HttpResponse(template.render({}, request))
    else:
        return redirect('login')

class UploadsView(CreateView):
    model = Uploads
    fields = ['title', 'image']
    template_name = 'upload.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        owner = self.request.user
        form.instance.owner = owner
        return super(UploadsView, self).form_valid(form)

class MyUploadsView(ListView):
    model = Uploads
    template_name = 'my_uploads.html'
