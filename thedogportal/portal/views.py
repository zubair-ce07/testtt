from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from django.db.models.aggregates import Count
from random import randint

from .models  import Profile, Uploads, Upvotes
from .forms import UploadForm

def HomepageView(request):
    if request.user.is_authenticated:
        template = loader.get_template('home.html')

        if request.method == "POST":
            image_id = request.POST.getlist('upvote')[0]
            image = Uploads.objects.filter(image_identifier=image_id)[0]
            upvoter = Profile.objects.get(pk=request.user.id)
            owner = Profile.objects.get(pk=image.owner_id)
            if(not Upvotes.objects.filter(upvoter=upvoter, photo=image, owner=owner)):
                upvoted = Upvotes(upvoter=upvoter, photo=image, owner=owner)
                upvoted.save()
                messages.add_message(request, messages.SUCCESS, 'Post upvoted successfully!')
            else:
                messages.add_message(request, messages.SUCCESS, 'Post already upvoted!')

        random_image = Uploads.objects.exclude(owner=request.user.id)[randint(0, Uploads.objects.exclude(owner=request.user.id).count() - 1)]
        user_profile = Profile.objects.filter(pk=request.user.id)[0]

        if (not user_profile.location or not user_profile.bio or not user_profile.birth_date):
            messages.add_message(request, messages.WARNING, 'Please complete you profile by going to settings!')

        return HttpResponse(template.render({"random_image": random_image}, request))
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
        messages.add_message(self.request, messages.SUCCESS, 'Post uploaded successfully!')
        owner = self.request.user
        form.instance.owner = owner
        return super(UploadsView, self).form_valid(form)

def MyUploadsView(request):
    if request.user.is_authenticated:
        template = loader.get_template('my_uploads.html')

        if request.method == "POST":
            items_to_delete = request.POST.getlist('delete_image')
            Uploads.objects.filter(pk__in=items_to_delete).delete()
            messages.add_message(request, messages.SUCCESS, 'Post deleted successfully!')

        list_of_images = Uploads.objects.filter(owner=request.user.id)
        return HttpResponse(template.render({'uploads': list_of_images}, request))
    else:
        return redirect('login')

class MySettings(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Profile
    fields = ['bio', 'location', 'birth_date']
    template_name = 'settings.html'
    success_url = reverse_lazy('index')
    success_message = "Settings successfully saved!"

    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.id)
