from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View

from web.posts.forms.new_post_form import NewPostForm
from web.posts.models import Post
from web.users.models import Address


class NewPostView(View):
    template_name = 'posts/new_post.html'

    def get(self, request):
        return render(request, self.template_name, dict(new_post_form=NewPostForm()))

    def post(self, request):

        new_post_form = NewPostForm(request.POST, request.FILES)
        if new_post_form.is_valid():

            title = new_post_form.cleaned_data.get('title')
            area = new_post_form.cleaned_data.get('area')
            country = new_post_form.cleaned_data.get('country')
            city = new_post_form.cleaned_data.get('city')
            street_or_block = new_post_form.cleaned_data.get('street_or_block')
            route = new_post_form.cleaned_data.get('route')
            state = new_post_form.cleaned_data.get('state')
            zip_code = new_post_form.cleaned_data.get('zip_code')
            description = new_post_form.cleaned_data.get('description')
            kind = new_post_form.cleaned_data.get('kind')
            contact_number = new_post_form.cleaned_data.get('contact_number')
            demand = new_post_form.cleaned_data.get('demand')
            expired_on = new_post_form.cleaned_data.get('expired_on')

            address = Address(zip_code=zip_code, route=route, street=street_or_block, city=city, state=state,
                              country=country)
            address.save()
            Post(posted_by=request.user, title=title, area=area, location=address, description=description,
                 kind=kind, contact_number=contact_number, demanded_price=demand, expired_on=expired_on).save()

            response = redirect(reverse('my_posts'))

        else:
            response = render(request, self.template_name, dict(new_post_form=new_post_form))

        return response