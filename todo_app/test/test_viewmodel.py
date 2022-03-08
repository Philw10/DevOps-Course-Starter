import pytest
from todo_app.data.view_model import ViewModel

class StubResponse():
    def __init__(self, id, task, status):
        self.id = id
        self.task = task
        self.status = status

    @classmethod
    def stub(cls, card):
        return cls(card['id'], card['name'], card['status'])

@pytest.fixture
def tasks():
    return [{'id':'101','name': 'Wash up', 'status':'To Do'},
             {'id':'102','name':'Haircut','status':'Doing'},
             {'id':'103','name':'Cook dinner','status':'Done'},
             {'id':'104','name':'Clean car','status':'To Do'},
             {'id':'105','name': 'Do project','status':'Doing'},
             {'id':'106','name':'Pay bills','status':'Done'}]

def test_DoingItemsPassedBack (tasks):

    task_list = []

    for task in tasks:
        task_list.append(StubResponse.stub(task))       

    task_item = ViewModel(task_list)
    
    doing_list = task_item.doing_items

    assert len(doing_list) == 2
    assert doing_list[0].status == 'Doing'
    assert type(doing_list) == list 

def test_ToDoItemsPassedBack (tasks):

    task_list = []

    for task in tasks:
        task_list.append(StubResponse.stub(task))       

    task_item = ViewModel(task_list)
    
    to_do_list = task_item.to_do_items

    assert len(to_do_list) == 2
    assert to_do_list[0].status == 'To Do' 
    assert type(to_do_list) == list 

def test_DoneItemsPassedBack (tasks):

    task_list = []

    for task in tasks:
        task_list.append(StubResponse.stub(task))       

    task_item = ViewModel(task_list)
    
    done_list = task_item.done_items

    assert len(done_list) == 2
    assert done_list[0].status == 'Done'
    assert type(done_list) == list   

