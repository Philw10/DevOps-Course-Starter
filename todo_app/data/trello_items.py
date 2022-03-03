from todo_app.data.item import Item
from todo_app.data.trello_api_comms import api_request_get, api_request_post, api_request_put

task_list = []

def process_full_trello_records():
    
    items_dict = api_request_get()
    process_tasks(items_dict)
       
      
def process_tasks(items_dict):

    for i in range(len(items_dict)):
        list_name = items_dict[i]['name']
        for card in items_dict[i]['cards']:
            duplicate_task = False
            for task in task_list:
                if (card['id'] == task.id):
                    duplicate_task = True
                    task.status = list_name   
            if (duplicate_task == False):
                add_card_to_task_list(card, list_name)               


def add_card_to_task_list(card, status):
    new_task = Item.from_trello_cards(card, status)
    task_list.append(new_task)

def get_items(): 

    process_full_trello_records()

    return task_list


def add_item(title):

    trello_conf_added = api_request_post(title)

    id = trello_conf_added['id']  

    new_task = Item.from_trello_cards({'id': id, 'name': title}, 'To Do')
    task_list.append(new_task) 
    

def complete_item(item_id):

    for task in task_list:
        if task.id == item_id:
            task.status = "complete"
            api_request_put(item_id)    