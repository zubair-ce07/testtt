from django.shortcuts import render
from django import views
from url_crawler.forms import UrlForm
from url_crawler.models import WebPage


class Index(views.View):

    @staticmethod
    def post(request):
        form = UrlForm(request.POST)
        context = {'form': form}

        if not form.is_valid():
            context['error'] = 'Enter a correct URL'
        else:
            page = WebPage.get_or_create(form.cleaned_data['url'])

            if page is None:
                context['error'] = 'Url Could not be visited'
            else:
                context.update({
                    'size': page.size_of_page,
                    'total_tags': page.tags_count,
                    'meta_tags': page.meta_tags_count,
                    'link_urls': [link.url for link in page.link_set.all()],
                    'link_tags': page.links_count
                })

        return render(request, 'url_crawler/index.html', context)

    @staticmethod
    def get(request):
        form = UrlForm()
        return render(request, 'url_crawler/index.html', {'form': form})
