''' testMongoDriver.py - This module provides tests for the mongoDriver module.
Author: Nick Colby
'''
import unittest
import json
from mongoDriver import connect_to_mongo, insert_data, retrieve_data, delete_data
import os  

class TestMongoDriver(unittest.TestCase):
    def setUp(self):
        self.db_name = 'testDB' # Update this information
        self.collection_name = 'testCollection'
        self.collection = connect_to_mongo(self.db_name, self.collection_name)
        # Clear the collection before each test
        self.collection.delete_many({})

    def tearDown(self):
        # Drop the collection after each test
        self.collection.drop()

    def test_insert_data(self):
        data = {'name': 'Test', 'value': 123}
        insert_data(self.collection, data)
        retrieved_data = retrieve_data(self.collection)
        self.assertEqual(len(retrieved_data), 1)
        self.assertEqual(retrieved_data[0]['name'], 'Test')
        self.assertEqual(retrieved_data[0]['value'], 123)

    def test_retrieve_data(self):
        data1 = {'name': 'Test1', 'value': 456}
        data2 = {'name': 'Test2', 'value': 789}
        insert_data(self.collection, [data1, data2])
        retrieved_data = retrieve_data(self.collection)
        self.assertEqual(len(retrieved_data), 2)

    def test_delete_data(self):
        data = {'name': 'TestDelete', 'value': 321}
        insert_data(self.collection, data)
        delete_count = delete_data(self.collection, {'name': 'TestDelete'})
        self.assertEqual(delete_count, 1)
        retrieved_data = retrieve_data(self.collection)
        self.assertEqual(len(retrieved_data), 0)

