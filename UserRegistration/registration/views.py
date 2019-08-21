from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import UserCreationForm
from .serializers import UserFormSerializer


def index(request):
    return render(request, 'registration/base.html')


@login_required
def home(request):
    return render(request, 'registration/home.html')


def signup(request):
    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        user = UserFormSerializer(data=user_creation_form.data)
        if user.is_valid():
            user.create(user.validated_data)
            email = user.validated_data.get('email')
            raw_password = user.validated_data.get('password_')
            user = authenticate(email=email, password=raw_password)
            login(request, user)

            return redirect('home')
    else:
        user_creation_form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': user_creation_form})

