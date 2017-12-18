from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django import views
from url_crawler.decorators import not_logged_in_required
from url_crawler.forms import LoginForm, SignUpForm, UrlForm
from url_crawler.models import WebPage


class Index(views.View):
    """
    View class responsible for generating index crawler page
    """

    @staticmethod
    def post(request):
        form = UrlForm(request.POST)
        context = {'form': form}

        if not form.is_valid():
            context['error'] = 'Enter a correct URL'
        else:
            try:
                page = WebPage.get_or_create(form.cleaned_data['url'])
                context.update({
                    'size': page.size_of_page,
                    'total_tags': page.tags_count,
                    'meta_tags': page.meta_tags_count,
                    'link_urls': [link.url for link in page.link_set.all()],
                    'link_tags': page.links_count
                })

            except TypeError:
                context['error'] = 'Response is not text. or Url is moved'
            except ConnectionError:
                context['error'] = 'Connection Failed to URL'

        return render(request, 'url_crawler/index.html', context)

    @staticmethod
    def get(request):
        return render(request, 'url_crawler/index.html', {'form': UrlForm()})


@method_decorator(not_logged_in_required, name='dispatch')
class Login(views.View):
    """
    Renders login page with form and on post requests logs user in
    """

    def get(self, request):
        return render(request, 'url_crawler/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        context = {'form': form}
        response = None

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                response = redirect('url_crawler:index')
            else:
                context['error'] = 'Email/Password is incorrect'
        if not response:
            response = render(request, 'url_crawler/login.html', context)
        return response


@method_decorator(not_logged_in_required, name='dispatch')
class SignUp(views.View):
    """
    Renders signup page for creating new users and accepts post request
    with user attributes to create users
    """

    def get(self, request):
        return render(request, 'url_crawler/signup.html', {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            response = redirect('url_crawler:index')
        else:
            response = render(request, 'url_crawler/signup.html', {'form': form})

        return response


def logout_user(request):
    logout(request)
    return redirect('url_crawler:login')
