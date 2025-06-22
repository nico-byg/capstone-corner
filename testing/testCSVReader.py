'''
testCSVReader.py - This module provides tests for the csvReader and mongoDriver modules.
Author: Nick Colby
'''
import unittest
from csvReader import read_csv_headers, export_headers_to_json  
from mongoDriver import connect_to_mongo, insert_data
import os
import json

class TestCSVReader(unittest.TestCase):
    def setUp(self):
        self.test_csv_file = 'test.csv'
        self.test_json_file = 'test.json'
        # Create a test CSV file with headers
        with open(self.test_csv_file, 'w', encoding='utf-8') as f:
            f.write('header1,header2,header3\n')

    def tearDown(self):
        # Remove test files after tests
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)
        if os.path.exists(self.test_json_file):
            os.remove(self.test_json_file)

    def test_read_csv_headers(self):
        headers = read_csv_headers(self.test_csv_file)
        self.assertEqual(headers, ['header1', 'header2', 'header3'])

    def test_export_headers_to_json(self):
        headers = read_csv_headers(self.test_csv_file)
        export_headers_to_json(headers, self.test_json_file)
        self.assertTrue(os.path.exists(self.test_json_file))
        with open(self.test_json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(data, {'header1': '', 'header2': '', 'header3': ''})
