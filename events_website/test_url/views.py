from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response, RequestContext
from events.forms import UploadImageForm
from events.models import Photo

def test_stuff(request):
    return render(request, 'index.html')

def test_stuff2(request, path):
    return HttpResponse('%s \n %s %s %s' % (path, request.META, request.POST, request.GET))
