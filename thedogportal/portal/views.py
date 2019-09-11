from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .models  import Profile, Uploads
from .forms import UploadForm

def HomepageView(request):
    if request.user.is_authenticated:
        template = loader.get_template('home.html')
        return HttpResponse(template.render({}, request))
    else:
        return redirect('login')

class UploadsView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Uploads
    form = UploadForm()
    fields = ['title', 'image']
    template_name = 'upload.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        owner = self.request.user
        form.instance.owner = owner
        return super(UploadsView, self).form_valid(form)

def MyUploadsView(request):
    if request.user.is_authenticated:
        template = loader.get_template('my_uploads.html')

        if request.method == "POST":
            items_to_delete = request.POST.getlist('delete_image')
            Uploads.objects.filter(pk__in=items_to_delete).delete()

        list_of_images = Uploads.objects.filter(owner=request.user.id)
        return HttpResponse(template.render({'uploads': list_of_images}, request))
    else:
        return redirect('login')

def DeleteImageView(request):
#     if request.user.is_authenticated:
#         template = loader.get_template('my_uploads.html')
#         list_of_images = Uploads.objects.filter(owner=request.user.id)
#         return HttpResponse(template.render({'uploads': list_of_images}, request))
#     else:
        return redirect('login')
