from pymongo import MongoClient
from bson.json_util import dumps


class UserList:

  client: MongoClient

  def __init__(self, client: MongoClient):
    self.client = client
    db = client['username_db']
    self.collection = db['usernames']

  def is_banned(self, username):
    if username in dumps(self.collection.find({'username': username})): return False
    return True
  
  def add_user(self, username):
    if username in dumps(self.collection.find({'username': username})): return
    self.collection.insert_one({
      'username': username
    })

  def delete_user(self, username):
    self.collection.delete_one({'username': username})