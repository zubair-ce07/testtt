from django.core.exceptions import ValidationError
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

        response = None
        form = NewPostForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data.get('title')
            area = form.cleaned_data.get('area')
            country = form.cleaned_data.get('country')
            city = form.cleaned_data.get('city')
            street_or_block = form.cleaned_data.get('street_or_block')
            zip_code = form.cleaned_data.get('zip_code')
            description = form.cleaned_data.get('description')
            kind = form.cleaned_data.get('kind')
            contact_number = form.cleaned_data.get('contact_number')
            demand = form.cleaned_data.get('demand')
            expired_on = form.cleaned_data.get('expired_on')

            address = Address(zip_code=zip_code, street=street_or_block, city=city, country=country)
            address.save()
            Post(posted_by=request.user, title=title, area=area, location=address, description=description,
                 kind=kind, contact_number=contact_number, demanded_price=demand, expired_on=expired_on).save()
            response = redirect(reverse('my_posts'))

        else:
            response = render(request, self.template_name, dict(new_post_form=form))

        return response