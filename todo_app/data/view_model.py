class ViewModel:
    def __init__(self, tasks):
        self._tasks = tasks

    @property
    def tasks(self):
        return self._tasks

    @property
    def doing_items(self):
        doing_list = []
        for task in self._tasks:
            if task.status == 'Doing':
                doing_list.append(task)
        return doing_list

    @property
    def to_do_items(self):
        to_do_list = []
        for task in self._tasks:
            if task.status == 'To Do':
                to_do_list.append(task)
        return to_do_list  

    @property
    def done_items(self):
        done_list = []
        for task in self._tasks:
            if task.status == 'Done':
                done_list.append(task)
        return done_list    
