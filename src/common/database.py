import os

import pymongo

class Database(object):  #get general Database class as well as object you defined below
    uri = os.environ.get("MONGOLAB_URI")
    DATABASE = None
    # with out initialize method, since all database need to access the same uri and database

    @staticmethod  #tell python we are not using self in this method
    def initialize():
        db = pymongo.MongoClient(Database.uri) #access uri through Database class, that's why we called static
        Database.DATABASE = db['heroku_90spfz55']

    @staticmethod
    def insert(collection,data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query) ##not return a cursor, cursor start at begin of the collection and output one by one

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query) #return jason object

    @staticmethod
    def replace_data(collection,search,replacement):
        Database.DATABASE[collection].replace_one(search,replacement)
        #clients = [a for client in collection.find({})] # put client in collection.find({}) to a as a list
        # #we can use if statment: if client['Risklevel'] >100  or access things like a['age']
        #print(a)

