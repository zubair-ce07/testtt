from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


def register(request):
    if request.user.is_authenticated:
        return redirect('/portal')
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('login')
 
    else:
        f = UserCreationForm()
 
    return render(request, 'register.html', {'form': f})