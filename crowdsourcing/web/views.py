#User Management part of this file completly taken from: https://github.com/Horrendus/csrf_thesis/tree/master/django_forgebook
import json
import urllib2

from models import Task, Answer

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

#API functions

@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        body = json.loads(request.body,"ascii")
        possible_answers = json.dumps(body["possible_answers"])
        body["possible_answers"] = possible_answers
        task_instance = Task.objects.create(**body)
        return HttpResponse("{'id':%i}" % task_instance.id, content_type="application/json")

@csrf_exempt        
def answers(request):
    serializer = JSONSerializer()
    data = serializer.serialize(Answer.objects.all())
    return HttpResponse(data, content_type="application/json")

#Webinterface functions
def tasks(request):
    if request.method == 'GET':
        if str(request.user) == "AnonymousUser":
            tasks = Task.objects.none()
        else:
            answers = Answer.objects.filter(user=request.user)
            all_tasks = Task.objects.exclude(id__in=[a.task.id for a in answers])
            tasks = []
            for t in all_tasks:
                if not Answer.objects.filter(task=t).count() >= t.answers_wanted:
                    tasks += [t]
        return render_to_response('web/index.html', {'all_tasks': tasks}, context_instance=RequestContext(request))

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        possible_answers = json.loads(task.possible_answers)
        return render_to_response('web/detail.html', {'task': task, 'possible_answers': possible_answers}, context_instance=RequestContext(request))

@login_required
def answer_task(request, task_id):
    if request.method == 'POST':
        print request.user
        answer = request.POST.get('answer','')
        try:
            task = Task.objects.get(id=task_id)
            jsonDec = json.decoder.JSONDecoder()
            possible_answers = jsonDec.decode(task.possible_answers)
            existing_answers = Answer.objects.filter(task=task)
            if len(existing_answers) >= task.answers_wanted:
                messages.info(request, 'No more answers allowed for this task, please pick another one')
                return HttpResponseRedirect('/')
            for existing_answer in existing_answers:
                if existing_answer.user == request.user:
                    print "User already answered once, not allowed to do it twice"
                    messages.info(request, 'Already answered this question, you can\'t answer it again')
                    return HttpResponseRedirect('/')
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
                if len(existing_answers)+1 == task.answers_wanted:
                    print "last answer, sending callback"
                    serializer = JSONSerializer()
                    header = {'Content-type': 'application/json'}
                    data = serializer.serialize(Answer.objects.filter(task=task))
                    req = urllib2.Request(task.callback,data,header)
                    resp = urllib2.urlopen(req)
                    print resp.read()
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
        user = User.objects.create_user(username=username, password=password)
        user.save()
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