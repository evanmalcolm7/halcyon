from time import time, sleep

ACTIVE_TASKS = []

#the loop that checks all tasks every x amount of time
def task_loop():
    while True:
        try:
            for task in ACTIVE_TASKS:
                task.check_progress()
            #this governs the amount of time between checks
            sleep(5)
        except KeyboardInterrupt:
            raise

class Task():

    instances = []

    def __init__(self, task_creator, hours_needed, end_func, player, arguments=[], result=''):
        #add self to instances for gamestate purposes
        self.__class__.instances.append(self)
        #used as a way to check what creature is involved in making this task happen
        #used for busy checks
        self.task_creator = task_creator
        self.task_creator.busy = True
        #calculates the end_time and saves it as an attribute
        #time() gets a relative number of seconds since the epoch
        #then, the number of hours (time_needed) is converted to seconds
        #the end time is set to the current time + the time needed
        self.end_time = time() + (hours_needed*3600)
        self.end_func = end_func
        #add self to active task list
        ACTIVE_TASKS.append(self)
        #saves the arguments that will be needed as a list
        self.arguments = arguments
        self.result = result
        #get client methods so it can be inspected
        self.client_methods = [('Inspect', self.__str__, None, False),]

    def __str__(self):
        return '%s in %s' % (self.result, self.check_progress())

    def check_progress(self):
        #if the end time has passed, call end_func())
        if self.end_time <= time():
            self.end_func(*self.arguments)
            self.task_creator.busy = False
            ACTIVE_TASKS.remove(self)
            return '%s was finished.' % self.result
        #otherwise, report the hours/minutes left until its done
        seconds_left = self.end_time - time()
        hours_left = int((seconds_left/3600))
        minutes_left = int((seconds_left/60))
        if hours_left != 0:
            minutes_left -= (hours_left*60)
        return '%s hours, %s minutes' % (hours_left, minutes_left)
