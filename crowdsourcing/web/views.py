#User Management part of this file completly taken from: https://github.com/Horrendus/csrf_thesis/tree/master/django_forgebook
import json

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
        all_tasks = Task.objects.all()
        return render_to_response('web/index.html', {'all_tasks': all_tasks}, context_instance=RequestContext(request))

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        jsonDec = json.decoder.JSONDecoder()
        possible_answers = json.loads(task.possible_answers)#jsonDec.decode(task.possible_answers)
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
            print "Your Answer: %s" % answer
            print "Possible Answers: %s" % possible_answers
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
                #TODO: Check if the user is allowed to answer this task
                answer_instance = Answer.objects.create(task=task,user=request.user,answer=answer)
                answer_instance.save()
                messages.success(request, "Thanks for answering a Question!")
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
    messages.success( request, 'Sucessfully logged out' )
    return HttpResponseRedirect("/")

def update_user(request):
    #not implemented, but seems to be needed by admin interface
    return HttpResponseRedirect("/")