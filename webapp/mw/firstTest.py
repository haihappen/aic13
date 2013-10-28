# import the MobileWorks library 
import mobileworks as mw 

# to switch to the sandbox
mw.sandbox()

# provide your username/password 
mw.username = 'aic13t2'
mw.password = 'aic13' 

#the project for this exercise
p = mw.Project(instructions="This project is for rating texts, which are automatically scraped from Yahoo!Finance")

t1 = mw.Task() 
#the instructions
t1.set_params(instructions="Please rate the company/product in the given text either positiv(1), negativ(-1) or neutral(0)")
#the scraped text
t1.set_params(resource="The new Nexus5 will have NFC, Bluetooth, Wifi,...")
#parallel workflow, multiple workers, one final answer
t1.set_params(workflow="p") 
#type is text
t1.set_params(resourcetype="t")
#number answer (1,-1,0)
t1.add_field("Answer", "n") 

#adding the task to the project
p.add_task(t1)

#publishing the project and all included tasks and retrieving the project url
project_url = p.post()

print project_url