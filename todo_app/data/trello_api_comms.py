import requests
import os
from tokenize import String

def api_request_get():

    payload = {'key': os.getenv('API_KEY'), 'token': os.getenv('API_TOKEN')}
    list_ID = os.getenv('OPEN_LIST_ID')
    get_list_of_items = requests.get( f'https://api.trello.com/1/lists/{list_ID}/cards/', params=payload)

    return get_list_of_items.json()
        
def api_request_post(title: String): 

    payload = {'name': title, 'idList': os.getenv('OPEN_LIST_ID'), 'key': os.getenv('API_KEY'), 'token': os.getenv('API_TOKEN')}
    new_item = requests.post( f'https://api.trello.com/1/cards', params=payload)

    return new_item.json()

def api_request_put(card_id): 
    # Request moves the card into the completed list.  Completed list ID is passed in the payload as idList

    payload = {'key': os.getenv('API_KEY'), 'token': os.getenv('API_TOKEN'), 'idList': os.getenv('CLOSED_LIST_ID')}
    requests.put( f'https://api.trello.com/1/cards/{card_id}', params=payload)