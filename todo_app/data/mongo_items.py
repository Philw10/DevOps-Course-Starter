import pymongo
import os
from todo_app.data.item import Item

def mongo_db():
        client = pymongo.MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
        database = client[os.getenv('MONGO_DATABASE_NAME')]
        return database

def mongo_collection():

    collection_name = os.getenv('MONGO_COLLECTION_NAME')
    
    return mongo_db()[collection_name]
    
def get_tasks_as_items():

    mongo_list = mongo_collection().find()

    return [Item.from_mongoDb(task) for task in mongo_list]

def get_items(): 

    return get_tasks_as_items()

def add_item(title):

    new_item = {"task" : title, "status" : "To Do"}

    mongo_collection().insert_one(new_item)  

def doing_item(item_id):

    mongo_collection().update_one({"_id": item_id}, {"$set": {"status": "Doing"}}) 

def complete_item(item_id):

    mongo_collection().update_one({"_id": item_id}, {"$set": {"status": "Done"}})