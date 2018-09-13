from django.contrib.auth.decorators import user_passes_test


def anonymous_required(function, redirect_to='/'):
    """
    Decorator for views that checks that the user is NOT logged in, redirecting
    to the homepage if necessary.
    """
    verify_anonymous = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_to
    )
    if function:
        return verify_anonymous(function)
    return verify_anonymous
