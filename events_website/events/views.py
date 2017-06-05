from django.shortcuts import render, HttpResponseRedirect, render_to_response, RequestContext, HttpResponse, get_object_or_404
import time
from session.models import Session, expired, delete_session, logout
from .models import event, event_tags, event_participants, event_like, event_comments, event_tags, Photo
from .forms import CommentForm
from django import forms

def redirect_home(request):
    return HttpResponseRedirect('1/')

def home_page(request, page_num):
    session_key = request.COOKIES.get('sessionid', None)
    current_session = Session.objects.filter(sessionid=session_key)
    current_time = time.mktime(time.localtime())
    if not current_session:
        return HttpResponseRedirect('../')
    elif expired(current_time, current_session[0].time_created, 3600):
        delete_session(session_key)
        return HttpResponseRedirect('../session_expired/')
    if 'logout' in request.POST:
        return logout(session_key)
    page_num = int(page_num)
    events = event.objects.all()[(page_num - 1) * 5:page_num * 5]
    if not events:
        return HttpResponseRedirect('../%s/' % (page_num - 1))
    if request.method == 'GET':
	page_button = request.GET.get('page_button', None)
        if page_button == 'Next Page':
            return HttpResponseRedirect('../%s/' % (page_num + 1))
        elif page_button == 'Prev Page' and page_num > 1:
            return HttpResponseRedirect('../%s/' % (page_num - 1))
        elif page_button == 'Home':
            return HttpResponseRedirect('../')
        if 'submit_search' in request.GET:
            search_text = request.GET.get('search_text')
            event_match = event_tags.objects.filter(tag=search_text).order_by('event_id')
            if not event_match:
                error_text = 'No events with tag %s' % search_text
                return render_to_response('user/user_home.html', locals(), RequestContext(request))
            event_match_ids = []
            for event_found in event_match:
                event_match_ids += [event_found.event_id]
            response = HttpResponseRedirect('../search/1/')
            response.set_cookie('search_text', search_text)
            response.set_cookie('event_match', list(set(event_match_ids)))
            return response
    event_labels = [(5*(page_num-1)+i) for i in range(1, 6)]
    return render_to_response('user/user_home.html', locals(), RequestContext(request))

def search_event(request, page_num):
    session_key = request.COOKIES.get('sessionid', None)
    if 'logout' in request.POST:
        return logout(session_key)
    page_num = int(page_num)
    event_match_ids = request.COOKIES['event_match']
    events = []
    if page_num == 1:
        counter = 0
    elif page_num == 2:
        counter = 17
    elif page_num==3:
        counter = 33
    elif page_num>3 and page_num<21:
        counter = 33+(page_num-3)*20
    else:
        counter = 353 + (page_num-19)*25
    id = 0
    is_next_page = True
    a = 1
    while len(events)<5 and a<100:
        try:
            char = event_match_ids[counter]
            if char == '[':
                counter += 1
                id = int(event_match_ids[counter])
            elif char == ']':
                break
            else:
                id = int(event_match_ids[counter])
                counter += 1
                char = event_match_ids[counter]
                while char != ',' and char != ']' and char != ' ':
                    id = int(str(id)+char)
                    counter+=1
                    char = event_match_ids[counter]
        except IndexError:
            is_next_page = False
            break
        except:
            a += 1
	    counter+=1
            continue
        events += list(event.objects.filter(id=id))
        counter += 1
    page_button = request.GET.get('page_button', None)
    if page_button == 'Next Page' and is_next_page:
        return HttpResponseRedirect('../%s/' % (page_num + 1))
    elif page_button == 'Prev Page' and page_num > 1:
        return HttpResponseRedirect('../%s/' % (page_num - 1))
    elif page_button == 'Home':
        return HttpResponseRedirect('../../')
    return render_to_response('user/search.html', locals(), RequestContext(request))


def display_event(request, id):
    session_id = request.COOKIES.get('sessionid', None)
    name = get_object_or_404(Session, sessionid=session_id).username
    time_created = time.mktime(time.localtime())

    current_event = event.objects.filter(id = id)[0]
    current_event_likes = event_like.objects.filter(event_id=id)
    num_likes = len(current_event_likes)
    current_event_tags = event_tags.objects.filter(event_id=id)
    current_event_comments = event_comments.objects.filter(event_id=id)
    for comment in current_event_comments:
        comment.date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment.date))
    current_event_photos = Photo.objects.filter(event_id=id)
    current_event_participants = event_participants.objects.filter(event_id=id)
    num_participants = len(current_event_participants)

    if request.method == 'POST':
        if 'submit comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.cleaned_data['comment']
                instance = event_comments(event_id = id, commenter_name = str(name), date = time_created, comment = str(comment))
                instance.save()
                return HttpResponseRedirect('')
        if 'like' in request.POST:
            if not event_like.objects.filter(liker_name = str(name), event_id = id):
                instance = event_like(event_id = id, liker_name = str(name))
                instance.save()
        if 'participate' in request.POST:
            is_participating = event_participants.objects.filter(participant_name = str(name), event_id = id)
            if request.POST.get('participate') == 'Participate' and \
                    not is_participating:
                instance = event_participants(event_id = id, participant_name = str(name))
                instance.save()
                return HttpResponseRedirect('')
            elif request.POST.get('participate') == "Unparticipate" and is_participating:
                event_participants.objects.filter(event_id=id, participant_name = str(name)).delete()
        if 'logout' in request.POST:
            return logout(session_id)
    return render_to_response('user/user_event.html', locals(), RequestContext(request))
