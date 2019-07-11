# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .forms import BasicInformationForm, EducationForm, ExperienceForm
from .models import BasicInformation, Experience, Education
from django.core.files.storage import FileSystemStorage


def home(request):
    return render(request, 'home.html')


def basic_information(request):
    if request.method == "POST" and request.FILES['image']:
        form = BasicInformationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            image = request.FILES['image']
            fs = FileSystemStorage()
            image_name = fs.save(image.name, image)
            user_id = request.POST.get('user_id') or render(request, 'login.html')
            name = request.POST['name'] or ""
            email = request.POST["email"]or ''
            date_of_birth = request.POST['date_of_birth']or ''
            contact_number = request.POST['contact_number']or ''
            address = request.POST["address"]or ''
            skill1 = request.POST.get('skill1') or ''
            skill1_level = request.POST.get('skill1_level') or ''
            skill2 = request.POST.get('skill2') or ''
            skill2_level = request.POST.get('skill2_level') or ''
            skill3 = request.POST.get('skill3') or ''
            skill3_level = request.POST.get('skill3_level') or ''
            skill4 = request.POST.get('skill4') or ''
            skill4_level = request.POST.get('skill4_level') or ''
            skill5 = request.POST.get('skill5') or ''
            skill5_level = request.POST.get('skill5_level') or ''
            hobby1 = request.POST['hobby1'] or ''
            hobby2 = request.POST['hobby2'] or ''
            hobby3 = request.POST['hobby3'] or ''
            reference1 = request.POST['reference1'] or ''
            reference2 = request.POST['reference2'] or ''

            BasicInformation.objects.create(
                user_id=user_id,
                image=image_name,
                name=name,
                date_of_birth=date_of_birth,
                contact_number=contact_number,
                address=address,
                email=email,
                skill1=skill1,
                skill2=skill2,
                skill3=skill3,
                skill4=skill4,
                skill5=skill5,
                skill1_level=skill1_level,
                skill2_level=skill2_level,
                skill3_level=skill3_level,
                skill4_level=skill4_level,
                skill5_level=skill5_level,
                hobby1=hobby1,
                hobby2=hobby2,
                hobby3=hobby3,
                reference1=reference1,
                reference2=reference2,
                )
        else:
            print(form.errors)

    return render(request, 'basic_information.html')


def experience(request):
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id') or render(request, 'login.html')
            organization = request.POST['organization']
            position = request.POST["position"]
            starting_date = request.POST['starting_date']
            ending_date = request.POST['ending_date'] or None
            city = request.POST["city"]
            job_description = request.POST["job_description"]

            Experience.objects.create(
                user_id=user_id,
                organization=organization,
                position=position,
                starting_date=starting_date,
                ending_date=ending_date,
                job_description=job_description,
                city=city,
                person=BasicInformation.objects.get(user_id=user_id)
            )
        else:
            print(form.errors)

    return render(request, 'experience.html')


def education(request):
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id') or render(request, 'login.html')
            degree = request.POST['degree']
            institute = request.POST["institute"]
            starting_date = request.POST['starting_date']
            ending_date = request.POST['ending_date'] or None
            city = request.POST["city"]
            description = request.POST["description"]

            Education.objects.create(
                user_id=user_id,
                degree=degree,
                institute=institute,
                starting_date=starting_date,
                ending_date=ending_date,
                city=city,
                description=description,
                person=BasicInformation.objects.get(user_id=user_id),
            )
        else:
            print(form.errors)

    return render(request, 'education.html')


def retrieve_cv(request, user_id):
    person = {'basic_information': BasicInformation.objects.get(user_id=user_id),
              'education_list': Education.objects.filter(user_id=user_id),
              'experience_list': Experience.objects.filter(user_id=user_id)}
    return render(request,
                  'cv.html',
                  {'person': person})
