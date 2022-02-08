import os
import requests
from flask import session
from todo_app.data.item import Item
from todo_app.data.trello_api_comms import api_request_get, api_request_post, api_request_put

def process_trello_records():

    task_list = []
    
    items_dict = api_request_get()

    for card in items_dict:
        new_task = Item.from_trello_cards(card)
        task_list.append(new_task)

    return task_list

task_list = process_trello_records()

def get_items():    
        
    return session.get('items', task_list.copy())


def add_item(title):

    trello_conf_added = api_request_post(title)

    items = task_list

    id = trello_conf_added['id']    

    new_task = Item.from_trello_cards({'id': id, 'name': title})
    items.append(new_task)  
    

def complete_item(item_id):

    items = task_list

    for task in items:
        t = task.id
        if task.id == item_id:
            task.status = "Complete"
    
    #Updates Trello but not linked to the default items set as yet
    api_request_put(item_id)    