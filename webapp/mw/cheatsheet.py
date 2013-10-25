# import the MobileWorks library 
import mobileworks as mw 


# to switch to the sandbox
mw.sandbox()


# provide your username/password 
mw.username = 'username'
mw.password = 'password' 


# create a task object 
t = mw.Task(instructions="This question is created with Python2.7") 


# set some parameters 
t.set_params(resource="just_some_url")
 
 
# add the required fields 
t.add_field("Name", "t") 


# finally, post it and get the url of the newly created task 
task_url = t.post()


# use the task url that we got above (when we posted the task)
task_info = mw.Task.retrieve(task_url)

# use the task object that you posted
t.delete()


#approving a completed task
t.accept()


# create a project object 
p = mw.Project(instructions="What is the name on this business card?") 
# add the required fields 
p.add_field("Name", "t") 
# add some tasks 
p.add_task(mw.Task(resource="http://www.mybusinesscards.com/card_one.png")) 
p.add_task(mw.Task(resource="http://www.mybusinesscards.com/card_two.png")) 
# finally, post it and get the url of the newly created project 
project_url = p.post()


# using the project url we got above (when we posted the project) 
project_info = mw.Project.retrieve( project_url )


# use the project object that you posted 
p.delete()


#response of a task request
#-status ('n' - new task, 'r' - has to be reviewed, 'd' - task done)
#-results
#--workerid
#--timestamp
#--location
#--answers


#parameters for task
#-taskId
#-resource (url to resource)
#-resourceType (t - text, i - image, l - link, a - audio, v - video)
#-priority (int > 0)
#-workflow (p,i,s,m)
#-redundancy (int > 0)
#-payment (float > 0 cents)


#parameters for filtering workers
#-blocked (array of user ids)
#-location (array of country code strings)
#-age_min (int > 0)
#-age_max (int > 0)
#-gender (m,f)

#parameters for project
#-tasks (required)
#-webhooks (url will be called if the entire project is completed)
#-projectid (string, optional - server will generate one)