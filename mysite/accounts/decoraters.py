from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated(view_func):
    def wrapper_func(request,*args,**kargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kargs)
            else:
                return HttpResponse("you are not allowed")
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request,*args,**kargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group=='customer':
            return redirect('user-page')
        if group=='Admin':
            return view_func(request,*args,**kargs)
    return wrapper_func