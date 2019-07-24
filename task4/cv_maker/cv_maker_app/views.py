# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import BasicInformationForm, EducationForm, ExperienceForm
from .models import BasicInformation, Experience, Education, Job
from .serializers import JobSerializer


class HomeView(FormView):
    def get(self, request):
        return render(request, 'home.html')


class BasicInformationView(FormView):

    @method_decorator(login_required)
    def post(self, request):
        form = BasicInformationForm(request.POST, request.FILES)
        if form.is_valid() and request.FILES['image']:
            form.save()
            image = request.FILES['image']
            fs = FileSystemStorage()
            image_name = fs.save(image.name, image)
            user_id = request.POST.get('user_id')
            BasicInformation.objects.create(
                user_id=user_id,
                image=image_name,
                name=request.POST.get('name') or "",
                date_of_birth=request.POST.get('date_of_birth') or '',
                contact_number=request.POST.get('contact_number')or '',
                address=request.POST.get("address")or '',
                email=request.POST.get("email") or '',
                skill1=request.POST.get('skill1') or '',
                skill2=request.POST.get('skill2') or '',
                skill3=request.POST.get('skill3') or '',
                skill4=request.POST.get('skill4') or '',
                skill5=request.POST.get('skill5') or '',
                hobby1=request.POST.get('hobby1') or '',
                hobby2=request.POST.get('hobby2') or '',
                hobby3=request.POST.get('hobby3') or '',
                reference1=request.POST.get('reference1') or '',
                reference2=request.POST.get('reference2') or '',
                )
        else:
            print(form.errors)
        return render(request, 'basic_information.html', {'form': form})

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'basic_information.html', {'form': BasicInformationForm()})


class ExperienceView(FormView):

    @method_decorator(login_required)
    def post(self, request):
        form = ExperienceForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            Experience.objects.create(
                user_id=user_id,
                organization=request.POST.get('organization'),
                position=request.POST.get("position"),
                starting_date=request.POST.get('starting_date'),
                ending_date=request.POST.get('ending_date') or None,
                job_description=request.POST.get("job_description"),
                city=request.POST.get("city"),
                person=BasicInformation.objects.get(user_id=user_id)
            )
        else:
            print(form.errors)
        return render(request, 'experience.html', {'form': form})

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'experience.html')


class EducationView(FormView):

    @method_decorator(login_required)
    def post(self, request):
        form = EducationForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            Education.objects.create(
                user_id=user_id,
                degree=request.POST.get('degree'),
                institute=request.POST.get("institute"),
                starting_date=request.POST.get('starting_date'),
                ending_date=request.POST.get('ending_date') or None,
                city=request.POST.get("city"),
                description=request.POST.get("description"),
                person=BasicInformation.objects.get(user_id=user_id),
            )
        else:
            print(form.errors)
        return render(request, 'education.html', {'form': form})

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'education.html')


class RetrieveCvView(DetailView):
    @method_decorator(login_required)
    def get(self, request):
        if BasicInformation.objects.filter(user_id=request.user.id):
            person = {'basic_information': BasicInformation.objects.get(user_id=request.user.id),
                      'education_list': Education.objects.filter(user_id=request.user.id),
                      'experience_list': Experience.objects.filter(user_id=request.user.id)}
            return render(request,
                          'cv.html',
                          {'person': person})
        else:
            return HttpResponse("<h1 align='center'> Please enter your information first </h1>")


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
