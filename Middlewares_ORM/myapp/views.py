from django.contrib.auth import login, authenticate
from django.shortcuts import render_to_response
from django.template import RequestContext
from myapp.forms import UserForm
import logging


logger = logging.getLogger(__name__)


def login_view(request):

    if request.user.is_authenticated():
        user = request.user
        user_form = UserForm()
        error = None
        logger.debug("User already logged in")
        return render_to_response(
            'myapp/login.html',
            {'form': user_form, 'user': user, 'error': error}
        )

    else:
        context = RequestContext(request)
        user_form = UserForm(data=request.POST)
        error = None

        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
            else:
                logger.error("Incorrect username or password")
                error = "Username or password is incorrect"

        else:
            user = UserForm()

        return render_to_response(
            'myapp/login.html',
            {'form': user_form, 'user': user, 'error': error}, context
        )
