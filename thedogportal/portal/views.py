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

from portal.messages import responses
import portal.utils as dbUtils

from .models import Profile, Uploads, Upvotes, Downvotes, Favorites

from .forms import UploadForm


def HomepageView(request):
    if request.user.is_authenticated:
        template = loader.get_template('home.html')
        userid = request.user.id

        if request.method == "POST":
            upvote_id = request.POST.get('upvote', False)
            downvote_id = request.POST.get('downvote', False)
            favorite_id = request.POST.get('favorite', False)

            if(upvote_id):
                image = dbUtils.get_single_upload_by_id(upvote_id)
                upvoter = dbUtils.get_user_by_id(userid)
                owner = dbUtils.get_user_by_id(image.owner_id)

                if(not dbUtils.get_upvotes_object(upvoter, image, owner)):
                    dbUtils.delete_downvotes_object(upvoter, image, owner)
                    upvoted = dbUtils.new_upvotes_instance(upvoter, image, owner)
                    upvoted.save()

                    messages.add_message(request,
                                         messages.SUCCESS,
                                         responses["upvotes"]["success"])
                else:
                    messages.add_message(request,
                                         messages.SUCCESS,
                                         responses["upvotes"]["already"])
            elif (downvote_id):
                image = dbUtils.get_single_upload_by_id(downvote_id)
                downvoter = dbUtils.get_user_by_id(userid)
                owner = dbUtils.get_user_by_id(image.owner_id)

                if(not dbUtils.get_downvotes_object(downvoter, image, owner)):
                    dbUtils.delete_upvotes_object(downvoter, image, owner)
                    downvoted = new_downvotes_instance(downvoter, image, owner)
                    downvoted.save()

                    messages.add_message(request,
                                         messages.SUCCESS,
                                         responses["downvotes"]["success"])
                else:
                    messages.add_message(request,
                                         messages.SUCCESS,
                                         responses["downvotes"]["already"])
            elif(favorite_id):
                image = dbUtils.get_single_upload_by_id(favorite_id)
                favoriter = dbUtils.get_user_by_id(userid)
                owner = dbUtils.get_user_by_id(image.owner_id)

                if(not get_favorites_object(favoriter, image, owner)):
                    favorited = dbUtils.new_favorites_instance(favoriter, image, owner)
                    favorited.save()

                    messages.add_message(request,
                                         messages.SUCCESS,
                                         responses["favorites"]["add"])
                else:
                    dbUtils.delete_favorites_object(favoriter, image, owner)
                    messages.add_message(request,
                                         messages.SUCCESS,
                                         responses["favorites"]["remove"])
            else:
                messages.add_message(request,
                                     messages.DANGER,
                                     responses["unhandled"])

        upload_count = dbUtils.get_id_excluded_upload_count(userid)

        if upload_count:
            random_image = dbUtils.get_id_excluded_random_upload(userid, upload_count)
        else:
            random_image = None
        user_profile = Profile.objects.filter(pk=userid)[0]

        if (not user_profile.location or not
                user_profile.bio or not
                user_profile.birth_date):
            messages.add_message(request,
                                 messages.WARNING,
                                 responses["settings"]["warning"])

        upvoted = random_image.upvotes_set.filter(upvoter=userid)
        downvoted = random_image.downvotes_set.filter(downvoter=userid)
        favorited = random_image.favorites_set.filter(favoriter=userid)

        return HttpResponse(template.render({"random_image": random_image,
                                             'upvoted': upvoted,
                                             'downvoted': downvoted,
                                             'favorited': favorited}, request))
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
        messages.add_message(self.request,
                             messages.SUCCESS,
                             responses["posts"]["uploaded"])
        owner = self.request.user
        form.instance.owner = owner
        return super(UploadsView, self).form_valid(form)


def MyUploadsView(request):
    if request.user.is_authenticated:
        template = loader.get_template('my_uploads.html')

        if request.method == "POST":
            items_to_delete = request.POST.getlist('delete_image')
            dbUtils.delete_single_upload_by_id(items_to_delete)
            messages.add_message(request,
                                 messages.SUCCESS,
                                 responses["posts"]["deleted"])

        list_of_images = Uploads.objects.filter(owner=request.user.id)
        my_uploads_context_dict = {'uploads': list_of_images}

        return HttpResponse(template.render(my_uploads_context_dict, request))
    else:
        return redirect('login')


def MyFavoritesView(request):
    if request.user.is_authenticated:
        template = loader.get_template('my_favorites.html')

        if request.method == "POST":
            favorite_id = request.POST.get('favorite', False)
            dbUtils.delete_favorites_object(request.user.id, favorite_id)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 responses["favorites"]["remove"])

        list_of_images = Favorites.objects.filter(favoriter=request.user.id)
        my_favs_context_dict = {'favorites': list_of_images}
        return HttpResponse(template.render(my_favs_context_dict, request))
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
