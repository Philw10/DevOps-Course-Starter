from todo_app.data.item import Item
from todo_app.data.trello_api_comms import api_request_get, api_request_post, api_request_put

     
def process_tasks():

    items_dict = api_request_get()
    task_list = []
    for trello_list in items_dict:
        list_name = trello_list['name']
        for card in trello_list['cards']:
            task_list.append(Item.from_trello_cards(card, list_name))
    return task_list 

def get_items(): 

    return process_tasks()


def add_item(title):

    api_request_post(title)
    

def complete_item(item_id):

    api_request_put(item_id)    