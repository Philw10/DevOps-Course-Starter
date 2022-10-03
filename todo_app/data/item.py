class Item:
    def __init__(self, id, task, status):
        self.id = id
        self.task = task
        self.status = status

    @classmethod
    def from_mungoDb(cls, mungo):
        return cls(mungo['_id'], mungo['task'], mungo['status'])