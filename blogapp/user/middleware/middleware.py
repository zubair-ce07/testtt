from datetime import datetime as time


class ResponseTime(object):

    request_time = None

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.request_time = time.now()
        return self.get_response(request)

    def process_template_response(self, request, response):
        response.context_data.update({'time_delta': time.now() - self.request_time})
        return response
