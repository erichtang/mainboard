from debugcolor import co
import config

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

    # d_cfg = {
    #     'priority' : 10,
    #     'frequency' : 1,
    # }

    def __init__(self, satellite):
        """
        Initialize the Task using the PyCubed cubesat object.
        
        :type satellite: Satellite
        :param satellite: The cubesat to be registered

        """
        self.cubesat = satellite

        # self.cfg = self.d_cfg
        # self.load_cfg(self.cfg, self.name)
        
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

    async def main_task(self, *args, **kwargs):
        """
        Contains the code for the user defined task. 

        :param `*args`: Variable number of arguments used for task execution.
        :param `**kwargs`: Variable number of keyword arguments used for task execution. 

        """
        pass
    
    def load_cfg(self, cfg, name, sd=True):
        #loading of different named configs for different operating modes is possible by passing differnet names
        #load prev prio and freq if they exist
        try:
            prev_prio = cfg['priority']
            prev_freq = cfg['frequency']
        except:
            prev_prio = None
            prev_freq = None
        #update config
        config.load_cfg(cfg, name, self.cubesat.log, sd)
        #if new prio and freq we update the self.cubesat.scheduled tasks attribute
        try:
            if cfg['priority'] != prev_prio:
                self.cubesat.scheduled_tasks[self.name].change_priority(cfg['priority'])
            if cfg['frequency'] != prev_freq:
                self.cubesat.scheduled_tasks[self.name].change_rate(cfg['frequency'])
        except:
            self.cubesat.log("[ERROR][PRIORITY / FREQ UPDATE][{}][FAIL]".format(name))

    def save_cfg(self, cfg, name, sd=True):
        #literally the same for save cfg i think.
        config.save_config(cfg, name, self.cubesat.log, sd)

    
