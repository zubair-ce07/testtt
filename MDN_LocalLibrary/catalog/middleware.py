class ContextRequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with open('userbooklog.txt', 'a') as booklog:
            booklog.write('Request: {}\n'.format(request.user))
        return self.get_response(request)

    def process_template_response(self, request, response):
        with open('userbooklog.txt', 'a') as booklog:
            booklog.write('Book: {}\n'.format(response.context_data))
        return response
