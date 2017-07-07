from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import BookInstance


class ContextRequestMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with open('userbooklog.txt', 'a') as booklog:
            booklog.write('Request: {}\n'.format(request.user))

        booklog.close()

        response = self.get_response(request)

        return response

    def process_template_response(self, request, response):
        with open('userbooklog.txt', 'a') as booklog:
            booklog.write('Book: {}\n'.format(response.context_data))
        booklog.close()
        return response

    # def process_response(self, request, response):
    #     print('bla')
    #     with open('userbooklog.txt', 'a') as booklog:
    #         booklog.write('Book: {}\n'.format(
    #             response))
    #         # booklog.close()
    #     return response
        # if request.user.is_authenticated():
        #     try:
        #         books = BookInstance.objects.filter(
        #             borrower=request.user)
        #         count = books.count()
        #         if not count:
        #             count = 0
        #         with open('userbooklog.txt', 'a') as booklog:
        #             booklog.write('Count: {}\n'.format(response.context))
        #         booklog.close()
        #         return response
        #     except Exception:
        #         print ('bla')  # Fix possible errors
        #         return response
        # else:
        #     return response
