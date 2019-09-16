from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView

from portal.utils import profile_info_incomplete
from .models import (Profile,
                     Uploads,
                     Upvotes,
                     Downvotes,
                     Favorites)

from .forms import UploadForm

from portal.constants import (RESPONSES,
                              LOGIN_URL,
                              MY_UPLOADS_URL,
                              FAVORITE_ID_NAME)


class HomepageView(LoginRequiredMixin, View):
    login_url = reverse_lazy(LOGIN_URL)
    template_name = "home.html"

    def post(self, request, *args, **kwargs):
        userid = request.user.id
        upvote_id = request.POST.get("upvote", False)
        downvote_id = request.POST.get("downvote", False)
        favorite_id = request.POST.get(FAVORITE_ID_NAME, False)

        if(upvote_id):
            image = Uploads.get_single_upload_by_id(upvote_id)
            upvoter = Profile.get_user_by_id(userid)
            owner = Profile.get_user_by_id(image.owner_id)

            if(not Upvotes.get_upvotes_object(upvoter, image, owner)):
                Downvotes.delete_downvotes_object(upvoter, image, owner)
                upvoted = Upvotes.new_upvotes_instance(upvoter, image, owner)
                upvoted.save()

                messages.add_message(request,
                                     messages.SUCCESS,
                                     RESPONSES["upvotes"]["success"])
            else:
                messages.add_message(request,
                                     messages.SUCCESS,
                                     RESPONSES["upvotes"]["already"])
        elif (downvote_id):
            image = Uploads.get_single_upload_by_id(downvote_id)
            downvoter = Profile.get_user_by_id(userid)
            owner = Profile.get_user_by_id(image.owner_id)

            if(not Downvotes.get_downvotes_object(downvoter, image, owner)):
                Upvotes.delete_upvotes_object(downvoter, image, owner)
                downvoted = Downvotes.new_downvotes_instance(downvoter, image, owner)
                downvoted.save()

                messages.add_message(request,
                                     messages.SUCCESS,
                                     RESPONSES["downvotes"]["success"])
            else:
                messages.add_message(request,
                                     messages.SUCCESS,
                                     RESPONSES["downvotes"]["already"])
        elif(favorite_id):
            image = Uploads.get_single_upload_by_id(favorite_id)
            favoriter = Profile.get_user_by_id(userid)
            owner = Profile.get_user_by_id(image.owner_id)

            if(not Favorites.get_favorites_object(favoriter, image, owner)):
                favorited = Favorites.new_favorites_instance(favoriter, image, owner)
                favorited.save()

                messages.add_message(request,
                                     messages.SUCCESS,
                                     RESPONSES["favorites"]["add"])
            else:
                Favorites.delete_favorites_object(favoriter, image, owner)
                messages.add_message(request,
                                     messages.SUCCESS,
                                     RESPONSES["favorites"]["remove"])
        else:
            messages.add_message(request,
                                 messages.DANGER,
                                 RESPONSES["unhandled"])

        return HttpResponseRedirect(self.request.path_info)

    def get(self, request, *args, **kwargs):
        userid = request.user.id
        upload_count = Uploads.get_id_excluded_upload_count(userid)
        user_profile = Profile.objects.filter(pk=userid)[0]

        if (profile_info_incomplete(user_profile)):
            messages.add_message(request,
                                 messages.WARNING,
                                 RESPONSES["settings"]["warning"])

        if upload_count:
            random_image = Uploads.get_id_excluded_random_upload(userid, upload_count)
        else:
            random_image = None

        upvoted = random_image.upvotes_set.filter(upvoter=userid)
        downvoted = random_image.downvotes_set.filter(downvoter=userid)
        favorited = random_image.favorites_set.filter(favoriter=userid)

        homepage_context_dict = {"random_image": random_image,
                                 "upvoted": upvoted,
                                 "downvoted": downvoted,
                                 "favorited": favorited}

        return render(request, self.template_name, homepage_context_dict)


class UploadsView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy(LOGIN_URL)
    model = Uploads
    form = UploadForm()
    fields = ["title", "image"]
    template_name = "upload.html"
    success_url = reverse_lazy(MY_UPLOADS_URL)

    def form_valid(self, form):
        messages.add_message(self.request,
                             messages.SUCCESS,
                             RESPONSES["posts"]["uploaded"])
        owner = self.request.user
        form.instance.owner = owner

        return super(UploadsView, self).form_valid(form)


class MyUploadsView(LoginRequiredMixin, View, SuccessMessageMixin):
    login_url = reverse_lazy(LOGIN_URL)
    template_name = "my_uploads.html"
    success_message = RESPONSES["posts"]["deleted"]

    def post(self, request, *args, **kwargs):
        id_to_delete = request.POST.getlist("delete_image")[0]
        Uploads.delete_single_upload_by_id(id_to_delete)

        return HttpResponseRedirect(self.request.path_info)

    def get(self, request, *args, **kwargs):
        list_of_images = Uploads.objects.filter(owner=request.user.id)
        my_uploads_context_dict = {"uploads": list_of_images}

        return render(request, self.template_name, my_uploads_context_dict)


class MyFavoritesView(LoginRequiredMixin, View, SuccessMessageMixin):
    login_url = reverse_lazy(LOGIN_URL)
    template_name = "my_favorites.html"
    success_message = RESPONSES["favorites"]["remove"]

    def post(self, request, *args, **kwargs):
        favorite_id = request.POST.get(FAVORITE_ID_NAME, False)
        image = Uploads.get_single_upload_by_id(favorite_id)
        owner = Profile.get_user_by_id(image.owner_id)
        Favorites.delete_favorites_object(request.user.id, favorite_id, owner)

        return HttpResponseRedirect(self.request.path_info)

    def get(self, request, *args, **kwargs):
        list_of_images = Favorites.objects.filter(favoriter=request.user.id)
        my_favs_context_dict = {"favorites": list_of_images}

        return render(request, self.template_name, my_favs_context_dict)


class MySettings(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    login_url = reverse_lazy(LOGIN_URL)
    model = Profile
    fields = ["bio", "location", "birth_date"]
    template_name = "settings.html"
    success_url = reverse_lazy("index")
    success_message = RESPONSES["settings"]["saved"]

    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.id)
