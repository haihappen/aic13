# import the MobileWorks library 
import mobileworks as mw 

#switches to sandbox mode and does the auth.
def auth():
	# to switch to the sandbox
	mw.sandbox()
	# provide your username/password 
	mw.username = 'aic13t2'
	mw.password = 'aic13' 
		
#creates a project and returns the project url
def createProject(_tasks):
	#the project for this exercise
	p = mw.Project()
	
	#adding the tasks to the project
	for task in _tasks:
		p.add_task(task)

	#publishing the project and all included tasks and retrieving the project url
	return p.post()
	
#creates a task and returns the task used for the project
def createTask(_instructions, _text):
	task = mw.Task() 
	#the instructions
	task.set_params(instructions = _instructions)
	#the scraped text
	task.set_params(resource = _text)
	#parallel workflow, multiple workers, one final answer
	#wont work in sandbox mode, only manual worklfow in sandbox
	task.set_params(workflow="p") 
	#type is text
	task.set_params(resourcetype="t")
	#number answer (1,-1,0)
	task.add_field("Answer", "n")
	return task

#creates the same task N-times
def createTaskNTimes(_instructions, _text, _n):
	tasks = []
	while _n > 0:
		tasks.append(createTask(_instructions, _text))
		_n = _n - 1
	return tasks
	
#returns the project
def getProjectID(id):
	return mw.Project.retrieve("https://sandbox.mobileworks.com/api/v2/project/" + _id + "/")

#returns the task
def getTaskByID(id):
	return mw.Task.retrieve("https://sandbox.mobileworks.com/api/v2/task/" + _id + "/")

#---scrap---
#auth()
#t1 = createTask("a or b", "take a")
#t2 = createTask("c or d", "take c")
#tasks = [t1,t2]	
#print createProject(tasks)

#auth()
#print createProject(createTaskNTimes("instr","text",5))

