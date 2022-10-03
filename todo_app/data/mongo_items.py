import pymongo
import os
from todo_app.data.item import Item

#>>> client = pymongo.MongoClient('mongodb://todo-app-mongo-account:585FNKzPrduMQGxyxrJ4cxatCUHjmvBVPPfonOt6JnsvW7ByYzlpujwMkHvC2KNmyqqLSwuz8WPL137uhgkOew==@todo-app-mongo-account.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@todo-app-mongo-account@')
#>>> post = {"task": "Test task", "status": "to do"}
#>>> db = client.todo_app_mongodb
#>>> task=db.todo_list
#>>> id = task.insert_one(post).inserted_id  -- gives id when item added

## Need to work out how to get list of items

# Need to work out how to edit list -- e.g to move to done

def mongo_db():
        client = pymongo.MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
        database = client.todo_app_mongodb
        database.todo_list
        return database

def mongo_collection():
    return mongo_db().todo_list
    
def process_tasks():

    mungo_list = mongo_collection().find()

    return [Item.from_mungoDb(task) for task in mungo_list]

def get_items(): 

    return process_tasks()


def add_item(title):

    new_item = {"task" : title, "status" : "to do"}

    mongo_collection().insert_one(new_item)    

def complete_item(item_id):

    mongo_collection().update_one({"_id": item_id}, {"$set": {"status": "done"}})