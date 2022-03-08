import requests
import os
import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app

@pytest.fixture
def client():
    #Set .env to the test config instead of the real one
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create a new app
    test_app = app.create_app()

    # Use app to create test client
    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', get_lists_stub)
    response = client.get('/')
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

def get_lists_stub(url, params):
    test_board_id = os.environ.get('BOARD_ID')
    fake_response_data = None
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '123', 'name': 'Test card'}]
        },{
            'id': 'abc123',
            'name': 'Doing',
            'cards': [{'id': '124', 'name': 'Test card2'}]
        },{
            'id': 'a1b2c3',
            'name': 'Done',
            'cards': [{'id': '125', 'name': 'Test card3'}]
        }]

    return StubResponse(fake_response_data)    