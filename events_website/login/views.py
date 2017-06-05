from django.shortcuts import HttpResponseRedirect, render_to_response, RequestContext
from session.models import Session
from admin.models import user
from admin.forms import UserForm
from django.utils.crypto import get_random_string
import string

VALID_KEY_CHARS = string.ascii_lowercase + string.digits

def redirect_login_page(request):
    return HttpResponseRedirect('/login/')

def login_page(request):
    form = UserForm(request.GET or None)
    if form.is_valid() and form.clean():
        session_key = get_random_string(32, VALID_KEY_CHARS)
        while Session.objects.filter(sessionid=session_key):
            session_key = get_random_string(32, VALID_KEY_CHARS)
        name = request.GET['username']
        if user.objects.filter(username = str(name))[0].type == 'admin':
            response = HttpResponseRedirect('../admin/home/')
        else:
            response = HttpResponseRedirect('../home/')
        response.set_cookie('sessionid', session_key)
        Session.objects.create(sessionid=session_key, username = name)
        return response
    return render_to_response('login/login.html', locals(), RequestContext(request))
