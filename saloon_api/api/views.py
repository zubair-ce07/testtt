"""
Contains the views related to saloon api responsible for creating, updating, deleting
users (customer, owner, employee), appointments, saloons
"""
import arrow
import os
import pathlib
import requests
import uuid

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import APIException
import django_filters.rest_framework

from .constants import APPOINTMENT_CHOICES
from .filters import SaloonFilter
from .models import Saloon, Area, Feedback, Appointment
from .permissions import (IsUserASaloonOwner, IsUserACustomer, CanMarkFeedback, CanUpdateUserProfile,
                          CanAddEmployee, CanProcessAppointment, CanCancelAppointmet)
from .serializers import (UserSerializer, SaloonSerializer, EmployeeSerializer, FeedbackSerializer,
                          RequestAppointmentSerializer, AppointmentSerializer, ProcessAppointmentSerializer,
                          UserProfileSerializer, SaloonSearchSerializer, )
from .utils import get_random_string
from accounts.models import UserProfile
from saloon_api.settings import GEO_LOCATION_API_ACCESS_KEY, GEO_LOCATION_API_URL


class OwnerCreateView(generics.ListCreateAPIView):
    """
    Gives the list of existing owners and
    creates a new owner(user) and its profile and sets the user_type = 'o'
    in profile table
    """
    queryset = User.objects.filter(userprofile__user_type='o').values('id', 'username', 'password',
                                                                      'userprofile__user_type')
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new user."""
        user = serializer.save()
        user.set_password(user.password)
        user.save()
        user = User.objects.get(username=serializer.validated_data['username'])
        profile = UserProfile.objects.get(user=user)
        profile.user_type = 'o'
        profile.save()


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Updates the user's password on update request.
    Deletes the user on delete request.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        """
        Updates the password
        """
        user = serializer.save()
        # to save hashed password
        user.set_password(user.password)
        user.save()


class CustomerCreateView(generics.ListCreateAPIView):
    """
    Returns the list of existing customers.
    Creates a new customer (user) and sets user_type = 'c' in its profile.
    """
    queryset = User.objects.filter(userprofile__user_type='c').values('id', 'username', 'password',
                                                                      'userprofile__user_type')
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()
        user = User.objects.get(username=serializer.validated_data['username'])
        profile = UserProfile.objects.get(user=user)
        profile.user_type = 'c'
        profile.save()


class SaloonCreateView(generics.ListCreateAPIView):
    """
    Returns the list of existing saloons owned by the user.
    Creates the new saloon.
    """
    serializer_class = SaloonSerializer
    # only a saloon owner can add a saloon
    permission_classes = (permissions.IsAuthenticated, IsUserASaloonOwner,)

    def get_queryset(self):
        # getting the existing saloons of the owner
        return Saloon.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        # if an area already exists don't create that entity again
        # just assign the already created one to new area
        # otherwise create a new entity
        try:
            area = Area.objects.get(name__iexact=serializer.validated_data['area'],
                                    city=serializer.validated_data['city'])
            serializer.validated_data['area'] = area
        except Area.DoesNotExist:
            area = Area.objects.create(name=serializer.validated_data['area'], city=serializer.validated_data['city'])
            serializer.validated_data['area'] = area
        serializer.validated_data['country'] = area.city.country
        # if user provides the saloon logo
        # then give that image a unique name using uuid
        # and save that image.
        if serializer.validated_data['logo'] is not None:
            random_name = uuid.uuid4().hex
            # getting extension of image
            saloon_logo_tokens = serializer.validated_data['logo'].name.split('.')
            new_logo_name = '{}.{}'.format(random_name, saloon_logo_tokens[-1])
            serializer.validated_data['logo'].name = new_logo_name
        serializer.save()


class SaloonDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves the specific saloon object using lookup field pk available in the URL.
    Deletes the requested saloon on delete request.
    Updates the saloon on update request.
    """
    serializer_class = SaloonSerializer
    permission_classes = (permissions.IsAuthenticated, IsUserASaloonOwner,)

    def get_queryset(self):
        # getting the existing saloons of user
        return Saloon.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        location = self.get_latitude_and_longitude()
        # if an area already exists don't create that entity again
        # just assign the already created one to new area
        # otherwise create a new entity
        try:
            area = Area.objects.get(name__iexact=serializer.validated_data['area'],
                                    city=serializer.validated_data['city'])
            area.latitude = location['latitude']
            area.longitude = location['longitude']
            serializer.validated_data['area'] = area
        except Area.DoesNotExist:
            area = Area.objects.create(
                name=serializer.validated_data['area'], city=serializer.validated_data['city'],
                latitude=location['latitude'], longitude=location['longitude'],
            )
            serializer.validated_data['area'] = area
        serializer.validated_data['country'] = area.city.country
        saloon = get_object_or_404(Saloon, pk=self.kwargs['pk'])
        # if the the user sends the new saloon logo then update it
        # otherwise leave it as it was before
        if serializer.validated_data['logo'] is not None:
            self.delete_saloon_logo(saloon.logo)
            random_name = uuid.uuid4().hex
            saloon_logo_tokens = serializer.validated_data['logo'].name.split('.')
            new_logo_name = '{}.{}'.format(random_name, saloon_logo_tokens[-1])
            serializer.validated_data['logo'].name = new_logo_name
        else:
            serializer.validated_data['logo'] = saloon.logo
        serializer.save()

    def delete_saloon_logo(self, logo_name):
        """
        Deletes the previous logo of saloon if exists
        """
        current_path = os.getcwd()
        # to make the paths compatible with Windows and linux
        new_path = pathlib.Path('{}/{}'.format(current_path, 'media/saloon_logos'))
        os.chdir(str(new_path))
        picture_names = os.listdir()
        for picture_name in picture_names:
            if logo_name.name.find(picture_name) != -1:
                os.remove(picture_name)
                break
        os.chdir(current_path)

    def get_latitude_and_longitude(self):
        """
        Uses an external api ( ip stack ) to find the latitude and longitude of
        the user using its IP.
        """
        client_ip = self.request.META.get('REMOTE_ADDR')
        url = '{}/{}'.format(GEO_LOCATION_API_URL, client_ip)
        params = {
            'access_key': GEO_LOCATION_API_ACCESS_KEY
        }
        # sending request to external API
        response = requests.get(url, params)
        json_data = response.json()
        # set location values None in case of any error
        if 'error' in json_data:
            location = {
                'latitude': None,
                'longitude': None,
            }
        else:
            location = {
                'latitude': json_data['latitude'],
                'longitude': json_data['longitude'],
            }
        return location


class SaloonListView(generics.ListAPIView):
    """
    Returns the list of all the available saloons.
    Also supports filtering on the basis of fields declared
    in SaloonFilter defined in filter module
    """
    queryset = Saloon.objects.all()
    serializer_class = SaloonSearchSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = SaloonFilter


class EmployeeCreateView(generics.ListCreateAPIView):
    """
    Returns the list of available employees of respective saloon.
    Creates an employee using given credentials.
    """
    serializer_class = EmployeeSerializer
    # only an owner of the respected saloon can add employees to his saloon(s)
    permission_classes = (permissions.IsAuthenticated, IsUserASaloonOwner, CanAddEmployee)

    def get_queryset(self):
        """
        Returns some specific attributes of user and its profile
        """
        return UserProfile.objects.filter(user_type='e', saloon__owner=self.request.user).values(
            'pk', 'user__username', 'user__email', 'user__first_name', 'user__last_name', 'birth_date', 'saloon',
            'contact_number', 'address'
        )

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = User.objects.create(
                username=serializer.validated_data.get('user__username'),
                # for now we are dealing an employee  a
                # user who doesn't need any signup and login
                # so just set it's password a random string
                password=get_random_string(),
                email=serializer.validated_data.get('user__email'),
                first_name=serializer.validated_data.get('user__first_name'),
                last_name=serializer.validated_data.get('user__last_name'),
            )
            profile = UserProfile.objects.get(user=user)
            profile.user_type = 'e'
            profile.address = serializer.validated_data.get('address')
            profile.birth_date = serializer.validated_data.get('birth_date')
            profile.contact_number = serializer.validated_data.get('contact_number')
            # an employee must work in a saloon
            # so set its profile's saloon attribute to it's
            # respective saloon
            profile.saloon = Saloon.objects.get(pk=self.kwargs['pk'])
            profile.save()


class EmployeeListView(generics.ListAPIView):
    """
    Returns the list of available employees of the saloon if
    the user is the owner of that saloon.
    """
    serializer_class = EmployeeSerializer
    # only an owner of the saloon can view his/her  employees
    permission_classes = (permissions.IsAuthenticated, IsUserASaloonOwner, CanAddEmployee)

    def get_queryset(self):
        return UserProfile.objects.filter(user_type='e', saloon__owner=self.request.user).values(
            'pk', 'user__username', 'user__email', 'user__first_name', 'user__last_name', 'birth_date', 'saloon',
            'contact_number', 'address'
        )


class EmployeeDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves the specific employee using lookup field 'pk' available in URL.
    Updates an employee on update request.
    Deletes an employee on delete request.
    """
    serializer_class = EmployeeSerializer
    # only the owner of the respective saloon can perform this action
    permission_classes = (permissions.IsAuthenticated, IsUserASaloonOwner, CanAddEmployee)

    def get_queryset(self):
        """
        Returns specific attributes of employee and its profile.
        """
        return UserProfile.objects.filter(user_type='e', saloon__owner=self.request.user).values(
            'pk', 'user__username', 'user__email', 'user__first_name', 'user__last_name', 'birth_date', 'saloon',
            'contact_number', 'address'
        )

    def perform_update(self, serializer):
        user = get_object_or_404(User, id=self.kwargs['pk'], userprofile__saloon__owner=self.request.user)
        user.username = serializer.validated_data.get('user__username')
        user.email = serializer.validated_data.get('user__email')
        user.first_name = serializer.validated_data.get('user__first_name')
        user.last_name = serializer.validated_data.get('user__last_name')
        user.save()
        profile = get_object_or_404(UserProfile, user=user)
        profile.birth_date = serializer.validated_data.get('birth_date')
        profile.contact_number = serializer.validated_data.get('contact_number')
        profile.address = serializer.validated_data.get('address')
        profile.save()

    def perform_destroy(self, instance):
        # as you are receiving queryset of Profile so
        # override this method in which you will explicitly delete
        # respective User and it will automatically delete its related records
        # User.id and Profile.id is same in our case
        # as a Profile is simultaneously created with a User
        User.objects.filter(id=instance['pk']).delete()


class FeedbackCreateView(generics.ListCreateAPIView):
    """
    Retrieves the list of previous feedback.
    Creates a new feedback.
    """
    serializer_class = FeedbackSerializer
    # a customer can only give feedback to a saloon for one time
    permission_classes = (permissions.IsAuthenticated, IsUserACustomer, CanMarkFeedback)

    def get_queryset(self):
        """
        Returns the attributes of feedback of respective saloon
        """
        return Feedback.objects.filter(saloon__pk=self.kwargs['pk']).values('id', 'saloon__id', 'rate', 'description',
                                                                            'user__id')

    def perform_create(self, serializer):
        try:
            saloon = Saloon.objects.get(id=self.kwargs['pk'])
            Feedback.objects.create(
                user=self.request.user,
                rate=serializer.validated_data.get('rate'),
                description=serializer.validated_data.get('description'),
                saloon=saloon,
            )
        except Saloon.DoesNotExist:
            return APIException({'message': 'Creation Failed !!!'})


class FeedbackListView(generics.ListAPIView):
    """
    Returns the list of feedback of respective saloon.
    """
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return Feedback.objects.filter(saloon__pk=self.kwargs['pk']).values('id', 'saloon__id', 'rate', 'description',
                                                                            'user__id')


class FeedbackDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves the details of single feedback using pk (lookup field) available in URL.
    Updates the respective feedback on update respect.
    Deletes the respective feedback on delete respect.
    """
    serializer_class = FeedbackSerializer
    # only a customer can perform the above mentioned actions
    permission_classes = (permissions.IsAuthenticated, IsUserACustomer)

    def get_queryset(self):
        """
        Returns the specific attributes of the user.
        """
        return Feedback.objects.filter(user=self.request.user).values('id', 'saloon__id', 'rate',
                                                                      'description', 'user__id')

    def perform_update(self, serializer):
        try:
            feedback = Feedback.objects.get(id=self.kwargs['pk'])
            feedback.rate = serializer.validated_data.get('rate')
            feedback.description = serializer.validated_data.get('description')
            feedback.save()
        except Feedback.DoesNotExist:
            APIException({'message': 'Feedback does not exist !!!'})

    def perform_destroy(self, instance):
        # because of the customization did above
        # the default behavior of this method is not working
        # so override it and explicitly delete the feedback entity
        Feedback.objects.filter(id=self.kwargs['pk']).delete()


class RequestAppointmentCreateView(generics.CreateAPIView):
    """
    Creates an appointment for the respective customer (user).
    """
    serializer_class = RequestAppointmentSerializer
    # only a customer can request an appointment
    permission_classes = (permissions.IsAuthenticated, IsUserACustomer)

    def perform_create(self, serializer):
        try:
            saloon = Saloon.objects.get(pk=self.kwargs['pk'])
        except Saloon.DoesNotExist:
            raise APIException('Saloon does not exist !!!')
        # at the beginning set the status of appointment to 'pending'
        Appointment.objects.create(
            customer=self.request.user,
            saloon=saloon,
            status='pending',
            description=serializer.validated_data.get('description')
        )


class SaloonAppointmentsListView(generics.ListAPIView):
    """
    Returns the list of appointments of specific saloon.
    """
    serializer_class = AppointmentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # TODO: remove this commented code
        # profile = get_object_or_404(Profile, user=self.request.user)
        # if profile.user_type == 'o':
        #     return Appointment.objects.filter(
        #         saloon__owner=self.request.user, status__in=APPOINTMENT_CHOICES, saloon__id=self.kwargs['pk']
        #     )
        return Appointment.objects.filter(status__in=APPOINTMENT_CHOICES, saloon__id=self.kwargs['pk'])


class ProcessAppointmentDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves the single appointment instance using pk (lookup field) available in URL.
    Updates the appointment on update request.
    Deletes the appointment on delete request.
    """
    serializer_class = ProcessAppointmentSerializer
    # only a saloon owner can process his/her appointments
    permission_classes = (permissions.IsAuthenticated, CanProcessAppointment)

    def __init__(self):
        """
        Initialize the attributes.
        Adds extra attribute appointment_saloon.
        """
        super().__init__()
        self.appointment_saloon = None

    def get_object(self):
        pk = int(self.kwargs['pk'])
        saloon = Saloon.objects.filter(owner=self.request.user)
        # only get that appointment which belongs to the user's saloon
        appointment = get_object_or_404(Appointment.objects.filter(saloon__in=saloon), id=pk)
        self.appointment_saloon = appointment.saloon
        return appointment

    def get_serializer_context(self):
        """
        Adds extra attributes to context data
        including 'booked_slots' and 'appointment_saloon'
        """
        context = super(ProcessAppointmentDetailsView, self).get_serializer_context()
        context.update({
            'booked_slots': self.get_booked_slots(),
            'appointment_saloon': self.appointment_saloon,
        })
        return context

    def get_booked_slots(self):
        """
        Returns the booked slots of the saloon
        """
        current_time = arrow.get(arrow.utcnow().format('YYYY-MM-DD HH:mm')).datetime
        # filter those appointments whose reporting time are greater than current time
        appointments = Appointment.objects.filter(saloon=self.appointment_saloon, time__gte=current_time)

        booked_slots = []
        for app in appointments:
            reporting_time = arrow.get(app.time)
            # calculate ending time of appointment by just adding duration of appointment in reporting time
            slot = [reporting_time.datetime, reporting_time.shift(minutes=app.duration).datetime, app.attender.id]
            booked_slots.append(slot)
        return booked_slots

    def perform_update(self, serializer):
        """
        Updates the appointment and while updating also
        considers the appointment time and attender validation.
        """
        reporting_time = arrow.get(serializer.validated_data.get('time'))
        duration = serializer.validated_data.get('duration')
        requested_slot = [
            reporting_time,
            reporting_time.shift(minutes=duration),
            serializer.validated_data.get('attender'),
        ]
        if self.validate_slot(requested_slot):
            serializer.save()
        else:
            raise APIException({'message': 'This slot has been already reserved !!!'})

    def validate_slot(self, requested_slot):
        """
        Validates requested slot.
        """
        booked_slots = self.get_booked_slots()
        for slot in booked_slots:
            slot[0] = arrow.get(slot[0])
            slot[1] = arrow.get(slot[1])
            # check that if the requested slot is clashing with the booked slots
            if (slot[0] <= requested_slot[0] <= slot[1]) or (slot[0] <= requested_slot[1] <= slot[1]):
                # check that in the clashing slot if the same attender is busy
                # if yes then this is an invalid slot
                if slot[2] == requested_slot[2].id:
                    return False
        return True


class CancelAppointmentView(generics.RetrieveUpdateAPIView):
    """
    Retrieves the appointment using pk (lookup field) available in URL.
    Updates its status to 'cancelled'.
    """
    serializer_class = RequestAppointmentSerializer
    # A customer can only cancel his/her appointments
    permission_classes = (permissions.IsAuthenticated, CanCancelAppointmet)

    def get_object(self):
        return get_object_or_404(Appointment, id=self.kwargs['pk'], customer=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['status'] = 'cancelled'
        serializer.save()


class UpdateUserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieves user on the basis of pk (lookup field) available in URL.
    Updates user on update request.
    """
    serializer_class = UserProfileSerializer
    # a user can only update his/her profile
    permission_classes = (permissions.IsAuthenticated, CanUpdateUserProfile)

    def get_queryset(self):
        """
        Returns the specific attributes of user and its related profile.
        """
        return UserProfile.objects.filter(user=self.request.user).values(
            'user__username', 'user__email', 'user__first_name', 'user__last_name', 'user_type', 'birth_date',
            'contact_number', 'address', 'userprofile_picture',
        )

    def perform_update(self, serializer):
        try:
            profile = get_object_or_404(UserProfile, user=self.request.user)
            user = get_object_or_404(User, id=profile.user.id)
        except Exception:
            raise APIException({'message': 'Updateion Filed !!!'})

        user.username = serializer.validated_data['user__username']
        user.first_name = serializer.validated_data['user__first_name']
        user.last_name = serializer.validated_data['user__last_name']
        user.email = serializer.validated_data['user__email']
        user.save()

        profile.contact_number = serializer.validated_data['contact_number']
        profile.birth_date = serializer.validated_data['birth_date']
        profile.address = serializer.validated_data['address']

        # if user does'nt upload profile picture then leave the profile picture same as it was before
        if serializer.validated_data['userprofile_picture'] is None:
            serializer.validated_data['userprofile_picture'] = profile.profile_picture
        else:
            self.manage_profile_picture()
            # getting image extension
            picture_name_tokens = serializer.validated_data['profile_picture'].name.split('.')
            # make the picture name by adding user id and username as a suffix
            new_picture_name = '{}___{}.{}'.format(user.id, user.username, picture_name_tokens[-1])
            serializer.validated_data['profile_picture'].name = new_picture_name
            profile.profile_picture = serializer.validated_data['profile_picture']
        profile.save()

    def manage_profile_picture(self):
        """
        Deletes the old profile picture of the user if it exists.
        """
        current_path = os.getcwd()
        # to make the paths compatible with both Windows and linux
        new_path = pathlib.Path('{}/{}'.format(current_path, 'media/images'))
        os.chdir(str(new_path))
        picture_names = os.listdir()
        my_picture_prefix = '{}___'.format(str(self.request.user.id))
        for picture_name in picture_names:
            if picture_name.startswith(my_picture_prefix):
                os.remove(picture_name)
                break
        os.chdir(current_path)
