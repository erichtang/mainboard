from debugcolor import co

class Task:

    """
    The Task Object.

    Attributes:
        priority:    The priority level assigned to the task.
        frequency:   Number of times the task must be executed in 1 second (Hz).
        name:        Name of the task object for future reference
        color:       Debug color for serial terminal
    """

    priority = 10
    frequency = 1
    name = 'template'
    color = 'gray'

    def __init__(self, satellite):
        """
        Initialize the Task using the PyCubed cubesat object.
        
        :type satellite: Satellite
        :param satellite: The cubesat to be registered

        """
        self.cubesat = satellite
        
    def debug(self,msg,level=1,log=False):
        """
        Print a debug message formatted with the task name and color, can append logfile

        :param msg: Debug message to print
        :param level: > 1 will print as a sub-level
        :param log: appends logfile if True #added CH
        """
        if level==1:
            print('{:>30} {}'.format('['+co(msg=self.name,color=self.color)+']',msg))
        else:
            print('{}{}'.format('\t   └── ',msg))
        if log:
            self.cubesat.log(msg, print_flag = False)

    def settings_loader(self, fname):
        """
        Get persistent settings from SD card file for this task

            need to figure this oout but this is OK for now ish

        :param fname: file name with settings
        :param level: > 1 will print as a sub-level
        :param log: appends logfile if True #added CH
        """
        pass

    async def main_task(self, *args, **kwargs):
        """
        Contains the code for the user defined task. 

        :param `*args`: Variable number of arguments used for task execution.
        :param `**kwargs`: Variable number of keyword arguments used for task execution. 

        """
        pass
    

    
