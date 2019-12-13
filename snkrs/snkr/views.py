import csv
import io

from django.contrib import messages
from django.shortcuts import render

from snkr.models import Description, ImageUrls, Skus, Snkr


def upload_file(request):
    template = "upload_file.html"

    if request.method == "GET":
        return render(request, template, {})

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):

        messages.error(request, 'This is not CSV File')

    for column in csv.reader(csv_file):

        urls = column[4]
        skus = column[7]
        description = column[2]

        product, created = Snkr.objects.update_or_create(
            brand=column[0],
            category=column[1],
            gender=column[3],
            name=column[5],
            retailer_sku=column[6],
            url=column[8]
        )

        urls_split = urls.split(',')

        for url_index in urls_split:

            urls_image = ImageUrls()

            urls_image.url = url_index
            urls_image.image_product = product
            urls_image.save()

        skus_split = skus.split('}')

        for skus_index in skus_split:

            skus_ = Skus()

            original_skus = skus_index + "}"
            original_skus = original_skus.replace(',', '', 1)
            skus_.sku = original_skus
            skus_.sku_product = product
            skus_.save()

        description_split = description.split(',')

        for description_index in description_split:

            description_ = Description()

            description_.description = description_index
            description_.product_description = product
            description_.save()

    return render(request, template, {})


def show_data(request):
    template = "show_data.html"

    snkr = Snkr.objects.all()

    context = {'snkrs': snkr}
    return render(request, template, context)


def search(request):
    template = "search.html"

    if request.method == "POST":
        snkr = Snkr()
        search = request.POST.get('search')
        query = Snkr.objects.filter(brand__contains=search)
        context = {'products': query}

        return render(request, template, context)
