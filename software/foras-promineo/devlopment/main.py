"""
PyCubed Foras Promineo Devlopment Software
    - 


M. Brodke, C. Hillis
"""

print('\n{lines}\n{:^40}\n{lines}\n'.format('Foras Promineo Dev',lines='-'*40))

print('Initializing PyCubed Hardware...')
import os, tasko
from pycubed import cubesat

# create asyncio object 
cubesat.tasko=tasko

# Dict to store scheduled objects by name
cubesat.scheduled_tasks={}

print('Loading Tasks...',end='')

""" Unsure of the significance of this. The cubesat already logs thru cubesat.log?
I do see use for saving camera data, but per documentation that should be saved in it's subsequent task or the pycubed.py file.

# ------------------------------------------ Start Section v

cubesat.new_file("user_file")
cubesat.new_directory("camera_data")

# ------------------------------------------ End Section ^
"""

# schedule all tasks in directory
for file in os.listdir('Tasks'):
    # remove the '.py' from file name
    file=file[:-3]

    # ignore these files
    if file in ("template_task", "test", "check_batteries", "game_manager", "check_batteries", "attitude_control", "beacon_task"): ## added more tasks to ignore. MB, CH
        continue

    print(f"importing {file}")

    # auto-magically import the task file
    exec('import Tasks.{}'.format(file))
    
    # create a helper object for scheduling the task
    task_obj=eval('Tasks.'+file).task(cubesat) # this why all task classes need to be called task

    # determine if the task wishes to be scheduled later
    if hasattr(task_obj,'schedule_later'):
        schedule=cubesat.tasko.schedule_later
    else:
        schedule=cubesat.tasko.schedule

    # schedule each task object and add it to our dict
    cubesat.scheduled_tasks[task_obj.name]=schedule(task_obj.frequency,task_obj.main_task,task_obj.priority)
print(len(cubesat.scheduled_tasks),'total')

print("Running....")
cubesat.tasko.run() #delete for flight
""" UNCOMMENT THIS SECTION AND DELTE LINE ABOVE FOR FLIGHT
#try:
    # should run forever
    cubesat.tasko.run()
#except Exception as e:
#    cubesat.send_to_ground('ERROR in main loop: {}'.format(e).encode('utf-8'))
#    try:
        # increment our NVM error counter
#        cubesat.c_state_err+=1
        # try to log everything
#        cubesat.log('{},{},{}'.format(e,cubesat.c_state_err,cubesat.c_boot))
#    except:
#        pass

# we shouldn't be here!
# uncomment before flight, this catches errors in the main loop
# can use this to run a different file next boot up if the board ever gets here
#supervisor.set_next_code_file(SEE DOCS)
#print('Engaging fail safe: hard reset')
#from time import sleep
#sleep(10)
#cubesat.micro.on_next_reset(cubesat.micro.RunMode.NORMAL)
#cubesat.micro.reset()
"""