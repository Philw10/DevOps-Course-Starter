class Item:
    def __init__(self, id, task, status = 'To Do'):
        self.id = id
        self.task = task
        self.status = status

    @classmethod
    def from_trello_cards(cls, list):
        return cls(list['id'], list['name'])