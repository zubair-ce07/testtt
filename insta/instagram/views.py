from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime
from instagram.forms import ContactForm
from django.core.mail import send_mail, get_connection
from django.shortcuts import render
from instagram.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login


def index(request):
    # def my_view(request):
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(username=username, password=password)
    # if user is not None:
    #     if user.is_active:
    #         login(request, user)
    #         # Redirect to a success page.
    #     else:
    #         # Return a 'disabled account' error message
    #         return HttpResponse("Error: Disabled Account")
    # else:
    #     # Return an 'invalid login' error message.
    #     return HttpResponse("Error: Invalid Login")
    # return HttpResponse("Hello, world. You're at the Instagram index.")
    values = request.META
    html = []
    for k in sorted(values):
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, values[k]))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


# def search_form(request):
#     return render(request, 'instagram/search_form.html')


def search(request):
    errors = []
    if 'query' in request.GET:
        query = request.GET['query']
        if not query:
            errors.append('Enter a search term')
            # return render(request, 'instagram/search_form.html',
                          # {'error': error})
        elif len(query)>20:
            errors.append('Please enter at most 20 characters')
        else:
            users = User.objects.filter(Q(username__icontains=query) | Q(name__icontains=query))
            return render(request, 'instagram/search_results.html',
                          {'users': users, 'query': query})
    return render(request, 'instagram/search_form.html',
                  {'errors': errors})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            con = get_connection('django.core.mail.backends.console.EmailBackend')
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],
                connection=con
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render(request, 'contact_form.html', {'form': form})


# def search(request):
#     # error = False
#     if 'query' in request.GET:
#         query = request.GET['query']
#         if not query:
#             error = True
#             return render(request, 'instagram/search_form.html',
#                           {'error': error})
#         users = User.objects.filter(Q(username__icontains=query) | Q(name__icontains=query))
#         return render(request, 'instagram/search_results.html',
#                       {'users': users, 'query': query})
    # else:
    #     return HttpResponse('Please submit a search term.')


# def login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user:
#         login(request, user)
#     else:
#         return