from django.shortcuts import redirect


def not_logged_in_required(original):
    """
    Decorator to limit access to only those user that are not logged in

    Arguments:
        original (callable): function to which limit access

    Returns:
        wrapper (callable): wrapped original function but with limiting access
    """
    def wrapper(request):
        if request.user.is_authenticated:
            response = redirect('users:index')
        else:
            response = original(request)
        return response
    return wrapper
