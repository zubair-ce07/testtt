import requests
from math import sin, cos, sqrt, atan2, radians

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from .forms import SignUpForm
from .models import UserProfile
from . import constants, helpers
# Create your views here.
#
class SignUpView(generic.FormView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    context_object_name = 'form'
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        """ The Sign up form was validated
        """
        self.save_user(form)
        return super().form_valid(form)

    def save_user(self, form):
        """ The  user object is created and saved
        """
        new_user = User.objects.create_user(username=form.cleaned_data['email_address'],
                                            first_name = form.cleaned_data['first_name'],
                                            last_name = form.cleaned_data['last_name'],
                                            password= form.cleaned_data['password'],
                                            email=form.cleaned_data['email_address'])
        new_user.save()
        self.save_user_profile(new_user, form)

    def save_user_profile(self, user, form):
        """ The userprofile object that has one-one link with user us created and saved
        """
        user.userprofile.cnic_no = form.cleaned_data['cnic_no']
        user.userprofile.phone_no = form.cleaned_data['phone_no']
        user.userprofile.address = form.cleaned_data['address']
        user.userprofile.city = form.cleaned_data['city'].lower()
        user.userprofile.country = form.cleaned_data['country'].lower()
        user.userprofile.role = form.cleaned_data['role']
        user.userprofile.categories.set(form.cleaned_data['categories'])
        user.userprofile.postal_code = form.cleaned_data['postal_code']
        # Code commented intentionally. Represents Co-ordinates feature
        # long,lat = self.get_long_lat_from_address(form.cleaned_data['address'])
        # if long:
        #     user.userprofile.longitude = long
        #     user.userprofile.latitude = lat
        user.userprofile.save()
        pass

    # Code commented intentionally. Represents Co-ordinates feature
    # def get_long_lat_from_address(self, address):
    #    """ long/lat are fetched from Google API using address
    #    """
    #     url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + '+'.join(address.split())
    #     try:
    #         response = requests(url)
    #         location = response['results'][0]['geometry']['location']
    #     except:
    #         return (None, None)
    #     else:
    #         lat = location['lat']
    #         long = location['long']
    #         return (long, lat)

@login_required
def home_view(request):
    role = request.user.userprofile.role
    if role == 'DN':
        return home_donor(request, request.user)
    elif role == 'CN':
        return home_consumer(request, request.user)
    elif request.user.is_staff:
        return redirect(request.build_absolute_uri() + 'admin/')
    return HttpResponse("Home l{}l".format(role))

def home_donor(request, user):
    """ Select consumers View
    """
    if request.method == 'POST': # Post indicates pair has been selected
        pair_id = int(request.POST.get("pair_id",-1))
        pair_user = get_object_or_404(UserProfile, pk=pair_id)
        pair_user.pair = request.user.userprofile
        pair_user.save()
        return HttpResponseRedirect(reverse('accounts:my_consumers'))
    elif request.method == 'GET': # Get indicates view must be populated
        consumers = UserProfile.objects.filter(
            city=user.userprofile.city.lower(),
            country=user.userprofile.country.lower(),
            role='CN')
        consumers = consumers.exclude(id=request.user.userprofile.id)
        consumers = consumers.exclude(id__in=request.user.userprofile.pairs.values('id'))
        return render(request,'accounts/donor/select_consumers.html',
                      context={'consumers': consumers, 'map_url' : constants.map_url})

def donors_pairs(request):
    if request.method == 'GET':
        return render(request,'accounts/donor/my_consumers.html',
                      context={'pair' : request.user.userprofile.pairs.all(),
                               'map_url' : constants.map_url})

def home_consumer(request, user):
    if request.method == 'GET':
        return render(request,
                      'accounts/consumer/my_donor.html',
                      context={'donor': request.user.userprofile.pair,
                               'my_category': request.user.userprofile.categories,
                               'map_url' : 'https://www.google.com/maps/search/?api=1&query='})
