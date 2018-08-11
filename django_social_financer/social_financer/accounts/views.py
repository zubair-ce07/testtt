from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import F
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import requests
from math import sin, cos, sqrt, atan2, radians

from .forms import SignUpForm
from .models import UserProfile
# Create your views here.
#
class SignUpView(generic.FormView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    context_object_name = 'form'
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        self.save_user(form)
        # form.save()
        return super().form_valid(form)

    def save_user(self, form):
        new_user = User.objects.create_user(username=form.cleaned_data['email_address'],
                                            first_name = form.cleaned_data['first_name'],
                                            last_name = form.cleaned_data['last_name'],
                                            password= form.cleaned_data['password'],
                                            email=form.cleaned_data['email_address'])
        new_user.save()
        self.save_user_profile(new_user, form)

    def save_user_profile(self, user, form):
        user.userprofile.cnic_no = form.cleaned_data['cnic_no']
        user.userprofile.phone_no = form.cleaned_data['phone_no']
        user.userprofile.address = form.cleaned_data['address']
        user.userprofile.city = form.cleaned_data['city'].lower()
        user.userprofile.country = form.cleaned_data['country'].lower()
        user.userprofile.role = form.cleaned_data['role']
        user.userprofile.categories.set(form.cleaned_data['categories'])
        user.userprofile.postal_code = form.cleaned_data['postal_code']
        long,lat = self.get_long_lat_from_address(form.cleaned_data['address'])
        if long:
            user.userprofile.longitude = long
            user.userprofile.latitude = lat
        user.userprofile.save()
        pass

    def get_long_lat_from_address(self, address):
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + '+'.join(address.split())
        try:
            response = requests(url)
            location = response['results'][0]['geometry']['location']
        except:
            return (None, None)
        else:
            lat = location['lat']
            long = location['long']
            return (long, lat)
# class LoginView(generic.View):

# class LoginView(generic.FormView):
#     template_name = 'registration/login.html'
#     success_url = reverse_lazy('users:home')
#
#     def form_valid(self, form):
#         email = form.cleaned_data['email']
#         password = form.cleaned_data['password']
#         user = authenticate(self.request, email, password)
#         if user is not None:
#             login(self.request, user)
#             return HttpResponseRedirect(reverse_lazy(self.success_url))
#         else:
#             pass

@login_required
def home_view(request):
    role = request.user.userprofile.role
    if role == 'DN':
        return home_donor(request, request.user)
    elif role == 'CN':
        return home_consumer(request, request.user)
    return HttpResponse("Home l{}l".format(role))

def home_donor(request, user):
    # https://www.google.com/maps/search/?api=1&query=
    consumers = UserProfile.objects.filter(city=user.userprofile.city, country=user.userprofile.country)
    if consumers.exist():
        for consumer in consumers:

            pass
    return render(request,'accounts/donor/map.html')
    # return HttpResponse('Donor Home')
    pass

def get_distance_btw_coordinates(src_long, src_lat, dest_long, dest_lat):
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(52.2296756)
    lon1 = radians(21.0122287)
    lat2 = radians(52.406374)
    lon2 = radians(16.9251681)

    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1

    a = sin(delta_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def home_consumer(request, user):
    return HttpResponse('Consumer Home')
    pass
