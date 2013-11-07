#User Management part of this file completly taken from: https://github.com/Horrendus/csrf_thesis/tree/master/django_forgebook
import json
import urllib2
import itertools

from urllib2 import HTTPError

from models import Task, Answer, Companyuser

from http_basic_auth import logged_in_or_basicauth

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import ObjectDoesNotExist

from JSONSerializer import JSONSerializer

#Helper functions
def get_tasks(user):
    if str(user) == "AnonymousUser":
        return Task.objects.none()
    if not user.companyuser_set.all():
        answers = Answer.objects.filter(user=user)
        unanswered_tasks = Task.objects.exclude(id__in=[a.task.id for a in answers])
        tasks = [t for t in unanswered_tasks if t.answer_set.all().count() < t.answers_wanted]
        return tasks
    else:
        return Task.objects.none()

def get_notallowed_message(task,user):
    message = ""
    existing_answers = task.answer_set.all()
    if len(existing_answers) >= task.answers_wanted:
        message =  'No more answers allowed for this task, please pick another one'
    if [a for a in existing_answers if a.user == user]:
        message = 'Already answered this question, you can\'t answer it again'
    if user.companyuser_set.all():
        message = 'Company Users are not allowed to answer questions'
    return message

#API functions
@csrf_exempt
@logged_in_or_basicauth()
def add_task(request):
    users = request.user.companyuser_set.all()
    if not users:
        return HttpResponse('only company users can create tasks',status=403)
    if request.method == 'POST':
        companyuser = users[0]
        body = json.loads(request.body,"ascii")
        possible_answers = json.dumps(body["possible_answers"])
        body["possible_answers"] = possible_answers
        task_instance = Task.objects.create(companyuser=companyuser,**body)
        return HttpResponse("{'id':%i}" % task_instance.id, content_type="application/json")

@csrf_exempt
@logged_in_or_basicauth()
def answers(request):
    users = request.user.companyuser_set.all()
    if not users:
        return HttpResponse('only company users can view answers to their tasks',status=403)
    companyuser = users[0]
    answersets = [t.answer_set.all() for t in companyuser.task_set.all()]
    answers = list(itertools.chain.from_iterable(answersets))
    serializer = JSONSerializer()
    data = serializer.serialize(answers)
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
@logged_in_or_basicauth()
def block_user(request, user_id):
    users = request.user.companyuser_set.all()
    if not users:
        return HttpResponse('only company users can block users from answering their tasks',status=403)
    companyuser = users[0]
    return HttpResponse("{'status':'not implemented yet'}", content_type="application/json")

#Webinterface functions
def tasks(request):
    if request.method == 'GET':
        tasks = get_tasks(request.user)
        return render_to_response('web/index.html', {'all_tasks': tasks}, context_instance=RequestContext(request))

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        if task in get_tasks(request.user):
            possible_answers = json.loads(task.possible_answers)
            return render_to_response('web/detail.html', {'task': task, 'possible_answers': possible_answers}, context_instance=RequestContext(request))
        else:
            messages.info(request, get_notallowed_message(task,request.user))
            return HttpResponseRedirect('/')


@login_required
def answer_task(request, task_id):
    if request.method == 'POST':
        print request.user
        answer = request.POST.get('answer','')
        try:
            task = Task.objects.get(id=task_id)
            if not task in get_tasks(request.user):
                messages.info(request, get_notallowed_message(task,request.user))
                return HttpResponseRedirect('/')

            jsonDec = json.decoder.JSONDecoder()
            possible_answers = jsonDec.decode(task.possible_answers)
            correct = False
            if len(possible_answers) > 1:
                if answer in possible_answers:
                    print "Correct Answer"
                    correct = True
                else:
                    print "Incorrect Answer, stupid User"
            else:
                #Open Question, we can't decide if answer is correct
                correct = True
            if correct:
                answer_instance = Answer.objects.create(task=task,user=request.user,answer=answer)
                answer_instance.save()
                messages.success(request, "Thanks for answering a Question!")
                existing_answers = task.answer_set.all()
                if len(existing_answers) == task.answers_wanted:
                    print "last answer, sending callback"
                    serializer = JSONSerializer()
                    header = {'Content-type': 'application/json'}
                    data = serializer.serialize(Answer.objects.filter(task=task))
                    req = urllib2.Request(task.callback,data,header)
                    try:
                        resp = urllib2.urlopen(req)
                        print resp.read()
                    except HTTPError:
                        print "callback not available"
                return HttpResponseRedirect('/')
            else:
                messages.info(request, 'Incorrect Answer, try again')
                return HttpResponseRedirect('/tasks/%i/' % task.id)
        except ObjectDoesNotExist:
            messages.error(request, "error, Task does not exist")
            return HttpResponseRedirect('/')

#User Management
#taken from: https://github.com/Horrendus/csrf_thesis/tree/master/django_forgebook
def users(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        usertype = request.POST.get('type','')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        if usertype == "company":
            companyuser = Companyuser.objects.create(user=user)
            companyuser.save()
        return HttpResponseRedirect("/")

def new_user(request):
    return render_to_response('web/signup.html', context_instance=RequestContext(request))

def sessions(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            messages.success( request, 'Sucessfully logged in' )
            next_url = request.POST.get('next','/')
            if len(next_url) is 0:
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect(next_url)
                
        else:
            messages.error( request, 'Could not log in' )
            return HttpResponseRedirect("/")

def destroy_session(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def update_user(request):
    #not implemented, but seems to be needed by admin interface
    return HttpResponseRedirect("/")