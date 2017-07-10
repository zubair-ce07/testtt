from datetime import datetime

class UserTimeMiddleware(object):
    '''
    Middleware that logs the current user and the timestamp
    on each request
    '''
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        with open('userlog.txt', 'a') as f:
            f.write('User: %s | Time: %s\n' % (
                request.user, datetime.now()
            ))
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response
