import os
from tokenize import String
import requests
from flask import session
from todo_app.data.item import Item

def api_request_get():

    payload = {'key': os.getenv('API_KEY'), 'token': os.getenv('API_TOKEN')}
    list_ID = os.getenv('OPEN_LIST_ID')
    get_list_of_items = requests.get( f'https://api.trello.com/1/lists/{list_ID}/cards/', params=payload)

    return get_list_of_items.json()
    
def api_request_post(title: String): 

    payload = {'name': title, 'idList': os.getenv('OPEN_LIST_ID'), 'key': os.getenv('API_KEY'), 'token': os.getenv('API_TOKEN')}
    requests.post( f'https://api.trello.com/1/cards', params=payload)

def api_request_put(card_id): 
    # Request moves the card into the completed list.  Completed list ID is passed in the payload as idList

    payload = {'key': os.getenv('API_KEY'), 'token': os.getenv('API_TOKEN'), 'idList': os.getenv('CLOSED_LIST_ID')}
    requests.put( f'https://api.trello.com/1/cards/{card_id}', params=payload)

def process_trello_records():

    task_list = set()  #Using a set to avoid duplication
    items_dict = api_request_get()

    for card in items_dict:
        new_task = Item.from_trello_cards(card)
        task_list.add(new_task)

    return task_list

def get_items():

    task_list = process_trello_records()
        
    return session.get('items', task_list.copy())


def add_item(title):

    api_request_post(title)
    

def complete_item(item_id):

    api_request_put(item_id)    