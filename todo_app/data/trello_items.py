from flask import session
from todo_app.data.item import Item
from todo_app.data.trello_api_comms import api_request_get, api_request_post, api_request_put

task_list = []

def process_trello_records():
    
    items_dict = api_request_get()
    
    for card in items_dict:
        duplicate = False
        for task in task_list:
            if (card['id'] == task.id):
                duplicate = True
        if (duplicate == False):        
            new_task = Item.from_trello_cards(card)
            task_list.append(new_task)            
    

def get_items(): 

    process_trello_records()

    return task_list


def add_item(title):

    trello_conf_added = api_request_post(title)

    id = trello_conf_added['id']    

    new_task = Item.from_trello_cards({'id': id, 'name': title})
    task_list.append(new_task) 
    

def complete_item(item_id):

    for task in task_list:
        if task.id == item_id:
            task.status = "complete"
    
    #Updates Trello but not linked to the default items set as yet
    api_request_put(item_id)    