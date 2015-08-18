from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View

from web.posts.forms.customized_search_form import CustomizedSearchForm
from web.posts.models import Post


class CustomizedSearchView(View):
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        response = None
        form = CustomizedSearchForm(request.POST)
        if form.is_valid():

            country = form.cleaned_data.get('country')
            state = form.cleaned_data.get('state')
            city = form.cleaned_data.get('city')
            route = form.cleaned_data.get('route')
            kind = form.cleaned_data.get('kind')
            max_price = form.cleaned_data.get('max_price')

            filter_criteria = Q(kind=kind, is_expired=False)
            if max_price:
                filter_criteria &= Q(demanded_price__range=[0, max_price])
            if country:
                filter_criteria &= Q(location__country=country)
            if state:
                filter_criteria &= Q(location__state=state)
            if city:
                filter_criteria &= Q(location__city=city)
            if route:
                filter_criteria |= Q(location__route=route)

            posts = Post.objects.filter(filter_criteria)
            posts = posts.order_by('-id') if posts.exists() else []
            response = render(request, 'posts/all_posts.html', dict(posts=posts))
        else:
            response = render(request, 'users/account.html', dict(customized_search_form=form))

        return response
