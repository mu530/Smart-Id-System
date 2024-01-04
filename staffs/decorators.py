from django.http import Http404


def role_required(role_names):
    def check_role(user):
        if user.is_superuser:
            return True

        return user.role == role_names

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not check_role(request.user):
                raise Http404
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
