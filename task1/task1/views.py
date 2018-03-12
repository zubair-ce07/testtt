import re

from django.template.loader import get_template

from django.http import HttpResponse

from django.shortcuts import render


def home(request):
    t = get_template('home.html')
    html = t.render()
    return HttpResponse(html)


def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        results = extract_files_data(q)
        return render(
            request, 'search_results.html',
            {'lines': results['lines'],
             'result_list': results['result'],
             'query': q}
        )
    else:
        return HttpResponse('Please submit a search term.')


def extract_files_data(query):
    result = dict()
    result['lines'] = []
    result['result'] = []
    with open("/home/dawood/Desktop/search.text") as file:
        data = file.readlines()
        for row in data:
            match = re.findall('\\b' + query + '\\b', row)
            if match:
                result['lines'].append(row)
                words = row.split()
                result['result'] += [word for word in words if word == query]
    return result
