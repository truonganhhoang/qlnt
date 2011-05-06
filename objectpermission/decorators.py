from functools import wraps
from django.http import HttpResponseForbidden
from django.utils.decorators import available_attrs

def object_permission_required(perm, value):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.has_perm(perm, value):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return _wrapped_view
    return decorator
