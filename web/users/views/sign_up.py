from django.shortcuts import render, redirect
from django.views.generic import View
from web.users.forms.sign_up_form import SignUpForm
from web.users.models import Address, User


class SignUpView(View):

    template_name = 'users/sign_up.html'

    def get(self, request):
        return render(request, self.template_name, dict(sign_up_form=SignUpForm()))

    def post(self, request):

        response = None
        form = SignUpForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            country = form.cleaned_data.get('country')
            city = form.cleaned_data.get('city')
            street_or_block = form.cleaned_data.get('street_or_block')
            zip_code = form.cleaned_data.get('zip_code')
            gender = form.cleaned_data.get('gender')
            date_of_birth = form.cleaned_data.get('date_of_birth')

            try:
                address = Address(zip_code=zip_code, street=street_or_block, city=city, country=country)
                address.save()
                User.objects.create_user(email=email, first_name=first_name, last_name=last_name,
                                         address=address, gender=gender, dob=date_of_birth, password=password)
                response = redirect('/')
            except:
                response = render(request, self.template_name, dict(sign_up_form=form))

        else:
            response = render(request, self.template_name, dict(sign_up_form=form))

        return response
