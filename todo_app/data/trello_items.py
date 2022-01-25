import os
from tokenize import String
import requests
from flask import session

def api_request_get():

    payload = {'key': os.getenv('API_KEY'), 'token': os.getenv('API_TOKEN')}
    board_ID = os.getenv('BOARD_ID')
    get_list_of_items = requests.get( f'https://api.trello.com/1/boards/{board_ID}/cards', params=payload)

    return get_list_of_items.json()
    
def api_request_post(title: String): 

    payload = {'name': title, 'idList': os.getenv('OPEN_LIST_ID'), 'key': os.getenv('API_KEY'), 'token': os.getenv('API_TOKEN')}
    requests.post( f'https://api.trello.com/1/cards', params=payload)

def api_request_put(title: String, card_id): 

    payload = {'key': os.getenv('API_KEY'), 'token': os.getenv('API_TOKEN')}
    requests.put( f'https://api.trello.com/1/cards/{card_id}', params=payload)

def get_items():
    
    items_dict = api_request_get()
                    
    return session.get('items', items_dict.copy())


def add_item(title):
    # post
    api_request_post(title)
    items = get_items()

    #session['items'] = items

    #return item


def save_item(item):
    #put
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item