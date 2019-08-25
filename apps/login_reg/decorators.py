from django.shortcuts import redirect
from django.contrib import messages


# decorator used to ensure user in in session
def required_login(views_func):
    def _wrapped_views_func(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, "Please register an account or log in to proceed.", extra_tags="not_in_session")
            return redirect('/')
        else:
            return views_func(request, *args, **kwargs)
    return _wrapped_views_func