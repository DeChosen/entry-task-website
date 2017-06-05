from django.shortcuts import render, HttpResponseRedirect, render_to_response, RequestContext, get_object_or_404, \
    HttpResponse
from .forms import UserForm, AddEventForm, AddTagForm
from events.forms import UploadImageForm
from events.models import event, event_like, event_tags, event_comments, Photo, event_participants
from .models import user
from session.models import Session, expired, delete_session, logout
import time


def redirect_page(request):
    return HttpResponseRedirect('1/')

def home_page(request, page_num):
    session_key = request.COOKIES.get('sessionid', None)
    current_session = Session.objects.filter(sessionid=session_key)
    current_time = time.mktime(time.localtime())
    if not current_session:
        return HttpResponseRedirect('../')
    elif expired(current_time, current_session[0].time_created, 3600):
        delete_session(session_key)
        return HttpResponseRedirect('../../session_expired/')
    if 'logout' in request.POST:
        return logout(session_key)
    page_num = int(page_num)
    if page_num > 0:
        events = event.objects.all()[(page_num-1)*5:page_num*5:]
        page_button = request.GET.get('page_button', None)
        if page_button == 'Next Page' and events:
            return HttpResponseRedirect('../%s/' % (page_num + 1))
        elif page_button == 'Prev Page' and page_num > 1:
            return HttpResponseRedirect('../%s/' % (page_num - 1))
        elif page_button == 'Home':
            return HttpResponseRedirect('../')
    return render_to_response('admin/admin_home.html', locals(), RequestContext(request))

def show_event(request, event_id):
    current_event = get_object_or_404(event, id=event_id)
    current_event_likes = event_like.objects.filter(event_id = event_id)
    num_likes = len(current_event_likes)
    current_event_tags = event_tags.objects.filter(event_id = event_id)
    current_event_comments = event_comments.objects.filter(event_id = event_id)
    current_event_participants = event_participants.objects.filter(event_id=event_id)
    num_participants = len(current_event_participants)
    #current_event_photos = Photo.objects.filter(event_id = event_id)
    if request.method == 'POST':    
	if 'add_tag_button' in request.POST:
            return HttpResponseRedirect('addtag/')
	elif 'delete_tag' in request.POST:
            tag_to_delete = request.POST['delete_tag'][12:]
            event_tags.objects.filter(event_id=event_id, tag=tag_to_delete).delete()
            return HttpResponseRedirect('')
        if 'delete_photo' in request.POST:
            photo_to_delete = request.POST['delete_photo'][14:]
            Photo.objects.filter(id=photo_to_delete).delete()
            return HttpResponseRedirect('')
	if 'delete_comment' in request.POST:
	    comment_to_delete = request.POST['delete_comment'][16:]
	    event_comments.objects.filter(id=comment_to_delete).delete()
	    return HttpResponseRedirect('')
        if 'submit_button' in request.POST:
            action = request.POST['submit_button']
            if action == 'Home':
                return HttpResponseRedirect('../')
            else:
                delete_event(event_id)
                return HttpResponseRedirect('../')
    return render_to_response('admin/display_event.html', locals(), RequestContext(request))

def addtag(request, event_id):
    tag_form = AddTagForm(request.POST or None)
    if tag_form.is_valid() and tag_form.cleaned_data['tag']!='':
        tag = tag_form.cleaned_data['tag']
        instance = event_tags(event_id=event_id, tag=tag)
        instance.save()
        return HttpResponseRedirect('../')
    elif request.POST.get('submit_button', None) == 'Back':
        return HttpResponseRedirect('../')
    return render_to_response('admin/add_tag.html', locals(), RequestContext(request))

def session_expired(request):
    return render(request, 'session_expired.html')


def addevent(request):
    event_form = AddEventForm(request.POST or None)
    if event_form.is_valid():
        event_form.save(commit=False).save()
        return HttpResponseRedirect('../')
    elif request.POST.get('submit_button', None) == 'Home':
        return HttpResponseRedirect('../')
    return render_to_response('admin/add_event.html', locals(), RequestContext(request))

def submit_photo(request, event_id):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            image = form.cleaned_data['image']
            instance = Photo(image = image, event_id = event_id)
            instance.save()
            return HttpResponseRedirect('../')
    return render_to_response('admin/upload_image.html', locals(), RequestContext(request))

def delete_event(event_id):
    event_tags.objects.filter(event_id=event_id).delete()
    event_comments.objects.filter(event_id=event_id).delete()
    event_like.objects.filter(event_id=event_id).delete()
    event_participants.objects.filter(event_id=event_id).delete()
    event.objects.filter(id=event_id).delete()    
