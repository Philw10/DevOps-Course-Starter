class Item:
    def __init__(self, id, task, status):
        self.id = id
        self.task = task
        self.status = status

    @classmethod
    def from_mongoDb(cls, mongo):
        return cls(mongo['_id'], mongo['task'], mongo['status'])