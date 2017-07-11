from datetime import datetime


class UserTimeMiddleware(object):
    """
    Middleware that logs the current user and the timestamp
    on each request in a .txt file
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with open('userlog.txt', 'a') as f:
            f.write('User: %s | Time: %s\n' % (
                request.user, datetime.now()
            ))
        response = self.get_response(request)
        return response
