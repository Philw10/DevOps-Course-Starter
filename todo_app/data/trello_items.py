import os
import requests
from flask import session

def api_request(request_type, title):
    payload = {'key': os.getenv('API_KEY'), 'token': os.getenv('API_TOKEN')}
    board_ID = os.getenv('BOARD_ID')

    if request_type == 'get all':
        get_list_of_items = requests.get( f'https://api.trello.com/1/boards/{board_ID}/cards', params=payload)
        return get_list_of_items.json()
    elif request_type == 'post':
        #code to add new action  updated and correct URL required
        requests.post( f'https://api.trello.com/1/boards/{board_ID}/cards', params=payload)
        
    elif request_type == 'put':
        #code to update action updated and correct URL required
        requests.get( f'https://api.trello.com/1/boards/{board_ID}/cards', params=payload)

    

def get_items():
    
    items_dict = api_request('get all', None)
    is_this_the_name = items_dict[0]['name']
            
    return session.get('items', items_dict.copy())


def add_item(title):
    # post
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    id = items[-1]['id'] + 1 if items else 0

    item = { 'id': id, 'title': title, 'status': 'Not Started' }

    # Add the item to the list
    items.append(item)
    session['items'] = items

    return item


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