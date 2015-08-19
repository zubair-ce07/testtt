from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View

from web.posts.forms.customized_search_form import CustomizedSearchForm
from web.posts.models import Post


class CustomizedSearchView(View):
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        customized_search_form = CustomizedSearchForm(request.POST)
        if customized_search_form.is_valid():

            country = customized_search_form.cleaned_data.get('country')
            state = customized_search_form.cleaned_data.get('state')
            city = customized_search_form.cleaned_data.get('city')
            route = customized_search_form.cleaned_data.get('route')
            kind = customized_search_form.cleaned_data.get('kind')
            max_price = customized_search_form.cleaned_data.get('max_price')

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
            response = render(request, 'users/home.html', dict(customized_search_form=customized_search_form))

        return response
