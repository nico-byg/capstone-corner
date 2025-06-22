'''
mongoDriver.py - this module provides functions to connect to a MongoDB database,
                insert data into a collection, and retrieve data from a collection.
Author: Nick Colby
'''

import pymongo
from pymongo import MongoClient
import json
import os

def get_mongo_collection(conn_string, db_name, collection_name):
    """
    Connects to a MongoDB database and returns the specified collection.
    
    :param conn_string: Connection string for MongoDB.
    :param db_name: Name of the database to connect to.
    :param collection_name: Name of the collection to access.
    :return: Collection object from the specified database.
    """
    client = MongoClient(conn_string)  # Connect to MongoDB using the connection string
    db = client[db_name]               # Access the specified database
    collection = db[collection_name]   # Access the specified collection
    return collection                  # Return the collection object

def insert_data(collection, data, key=None):
    """
    Inserts data into the specified MongoDB collection. If a key is provided,
    checks for existing documents with the same key value and updates them instead of inserting duplicates.

    :param collection: Collection object where data will be inserted.
    :param data: Data to be inserted (can be a dictionary or a list of dictionaries).
    :param key: (Optional) Field name to check for existing documents.
    """
    if isinstance(data, list):
        for item in data:
            if key and key in item:
                collection.update_one({key: item[key]}, {"$set": item}, upsert=True)
            else:
                collection.insert_one(item)
    else:
        if key and key in data:
            collection.update_one({key: data[key]}, {"$set": data}, upsert=True)
        else:
            collection.insert_one(data)

def retrieve_data(collection, query=None):
    """
    Retrieves data from the specified MongoDB collection.
    
    :param collection: Collection object from which data will be retrieved.
    :param query: Query to filter the data (default is None, which retrieves all documents).
    :return: List of documents matching the query.
    """
    if query is None:
        return list(collection.find())  # Retrieve all documents
    else:
        return list(collection.find(query))  # Retrieve documents matching the query
    
def delete_data(collection, query):
    """
    Deletes data from the specified MongoDB collection based on a query.
    
    :param collection: Collection object from which data will be deleted.
    :param query: Query to filter the documents to be deleted.
    """
    result = collection.delete_many(query)  # Delete documents matching the query
    return result.deleted_count  # Return the number of documents deleted

