from django.shortcuts import redirect


def login_required(*d_args, **d_kwargs):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.session.get('id_user') != None:
                return view_func(request, *args, **kwargs)
            return redirect(d_kwargs['login_url'])
        return wrapper
    return decorator


def only_unauth(*d_args, **d_kwargs):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.session.get('id_user') != None:
                return redirect(d_kwargs['home_url'])
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
