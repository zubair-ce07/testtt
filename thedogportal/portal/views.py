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

from .models  import Profile, Uploads, Upvotes, Downvotes, Favorites
from .forms import UploadForm

def HomepageView(request):
    if request.user.is_authenticated:
        template = loader.get_template('home.html')

        if request.method == "POST":
            upvote_id = request.POST.get('upvote', False)
            downvote_id = request.POST.get('downvote', False)
            favorite_id = request.POST.get('favorite', False)
            
            if(upvote_id):
                image = Uploads.objects.filter(image_identifier=upvote_id)[0]
                upvoter = Profile.objects.get(pk=request.user.id)
                owner = Profile.objects.get(pk=image.owner_id)

                if(not Upvotes.objects.filter(upvoter=upvoter, photo=image, owner=owner)):
                    Downvotes.objects.filter(downvoter=upvoter, photo=image, owner=owner).delete()
                    upvoted = Upvotes(upvoter=upvoter, photo=image, owner=owner)
                    upvoted.save()
                    messages.add_message(request, messages.SUCCESS, 'Post upvoted successfully!')
                else:
                    messages.add_message(request, messages.SUCCESS, 'Post already upvoted!')
            elif (downvote_id):
                image = Uploads.objects.filter(image_identifier=downvote_id)[0]
                downvoter = Profile.objects.get(pk=request.user.id)
                owner = Profile.objects.get(pk=image.owner_id)

                if(not Downvotes.objects.filter(downvoter=downvoter, photo=image, owner=owner)):
                    Upvotes.objects.filter(upvoter=downvoter, photo=image, owner=owner).delete()
                    downvoted = Downvotes(downvoter=downvoter, photo=image, owner=owner)
                    downvoted.save()
                    messages.add_message(request, messages.SUCCESS, 'Post downvoted successfully!')
                else:
                    messages.add_message(request, messages.SUCCESS, 'Post already downvoted!')
            elif(favorite_id):
                image = Uploads.objects.filter(image_identifier=favorite_id)[0]
                favoriter = Profile.objects.get(pk=request.user.id)
                owner = Profile.objects.get(pk=image.owner_id)

                if(not Favorites.objects.filter(favoriter=favoriter, photo=image, owner=owner)):
                    favorited = Favorites(favoriter=favoriter, photo=image, owner=owner)
                    favorited.save()
                    messages.add_message(request, messages.SUCCESS, 'Post added to your Favorites successfully!')
                else:
                    Favorites.objects.filter(favoriter=favoriter, photo=image, owner=owner).delete()
                    messages.add_message(request, messages.SUCCESS, 'Post removed from your Favorites!')
            else:
                messages.add_message(request, messages.DANGER, 'Unhandled request error!')


        image_count = Uploads.objects.exclude(owner=request.user.id).count()

        if image_count:
            random_image = Uploads.objects.exclude(owner=request.user.id)[randint(0, image_count - 1)]
        else:
            random_image = None
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
    success_url = reverse_lazy('my_uploads')

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

def MyFavoritesView(request):
    if request.user.is_authenticated:
        template = loader.get_template('my_favorites.html')

        if request.method == "POST":
            favorite_id = request.POST.get('favorite', False)
            Favorites.objects.filter(favoriter=request.user.id, photo=favorite_id).delete()
            messages.add_message(request, messages.SUCCESS, 'Post removed from your Favorites!')

        list_of_images = Favorites.objects.filter(favoriter=request.user.id)
        return HttpResponse(template.render({'favorites': list_of_images}, request))
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
