class Item:
    def __init__(self, id, task, status):
        self.id = id
        self.task = task
        self.status = status

    @classmethod
    def from_trello_cards(cls, card, status):
        return cls(card['id'], card['name'], status)