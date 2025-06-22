'''
csvReader.py - this module provides functions to read a CSV file and export its headers 
               into a JSON file with blank values
Author: Nick Colby
'''

import csv
import json 
import os

import mongoDriver

def read_csv_headers(file_path):
    """
    Reads the headers from a CSV file and returns them as a list.
    
    :param file_path: Path to the CSV file.
    :return: List of headers from the CSV file.
    """
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the first row as headers
        #print(headers)  # Print the headers for debugging purposes
    return headers

def export_headers_to_json(headers, output_file, key_name):
    """
    Appends the headers list to the existing 'headers' key in a JSON file under key_name.
    If the file does not exist, it will not create a new one.

    :param headers: List of headers to export.
    :param output_file: Path to the existing JSON file.
    :param key_name: The key name for the headers object.
    """
    if not os.path.exists(output_file):
        print(f"File {output_file} does not exist. No changes made.")
        return

    with open(output_file, 'r', encoding='utf-8') as jsonfile:
        existing_data = json.load(jsonfile)

    # Ensure 'headers' is a dict
    if 'headers' not in existing_data or not isinstance(existing_data['headers'], dict):
        existing_data['headers'] = {}

    # Append or create the key_name entry
    if key_name in existing_data['headers']:
        # If already a list, append; otherwise, convert to list
        if isinstance(existing_data['headers'][key_name], list):
            existing_data['headers'][key_name].append(headers)
        else:
            existing_data['headers'][key_name] = [existing_data['headers'][key_name], headers]
    else:
        existing_data['headers'][key_name] = [headers]

    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(existing_data, jsonfile, indent=4)

def read_csv_data(file_path):
    """
    Reads the data from a CSV file and returns it as a list of dictionaries.
    
    :param file_path: Path to the CSV file.
    :return: List of dictionaries representing the rows in the CSV file.
    """
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Read the CSV file as a dictionary
        data = [row for row in reader]  # Convert each row to a dictionary
    return data

def insert_data_to_mongo(collection, data):
    """
    Inserts data into a MongoDB collection.
    
    :param collection: MongoDB collection object where data will be inserted.
    :param data: List of dictionaries representing the data to be inserted.
    """
    if data:
        collection.insert_many(data)  # Insert multiple documents into the collection
        print(f"Inserted {len(data)} documents into the collection.")  # Debugging print statement
    else:
        print("No data to insert.")  # Debugging print statement