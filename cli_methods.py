''' cli_methods.py - Provides command line interface methods for the application.
Author: Nick Colby
'''

import csvReader 
import mongoDriver
import json
from logger import write_to_log

def print_menu():
    """Prints the main menu options for the application."""
    print("\nPlease select an option:")
    print("1. Setup Migration")
    print("2. Make Migration")
    print("3. Exit")

def setup_migration():
    """Sets up the migration by creating a JSON file and prompting for CSV files and MongoDB connection string."""
    
    # Initial setup for the JSON file
    print("Setting up migration...")
    json_file = input("Enter the path to the output JSON file: ")
    # Creates the JSON file if it does not already exist
    if not json_file.endswith('.json'):
        json_file += '.json'  # Ensure the output file has a .json extension

    # Creates the migration setup keys in the json file
    template = {
        "numberOfFiles": 1,
        "csvFiles": {},
        "db_conn_string": "",
        "headers": {}
    }
    with open(json_file, 'w') as f:
        json.dump(template, f, indent=4)
    
    # Prompt user for number of csv files to process
    try:
        num_files = int(input("\nEnter the number of CSV files to process: "))
        if num_files < 1:
            raise ValueError("Number of files must be at least 1.")
        with open(json_file, 'r+') as f:
            data = json.load(f)
            data['numberOfFiles'] = num_files
            f.seek(0)  # Move the cursor to the beginning of the file
            json.dump(data, f, indent=4)
            f.truncate()
        
        for i in range(num_files):
            csv_file = input(f"\nEnter the path to CSV file {i + 1}: ")
            if not csv_file.endswith('.csv'):
                raise ValueError("File must be a CSV file.")
            # Update the JSON file with the CSV file path
            with open(json_file, 'r+') as f:
                data = json.load(f)
                data['csvFiles'][f'file_{i + 1}'] = csv_file
                f.seek(0)
                json.dump(data, f, indent=4)
            print(f"CSV file {i + 1} path added to JSON file.")

        for file in data['csvFiles'].values():
            csv_file = file.strip()
            headers = csvReader.read_csv_headers(csv_file)
            csvReader.export_headers_to_json(headers, json_file, csv_file)
            print(f"Headers from {file} exported to {json_file} successfully.")
            write_to_log('migration.log', f"Headers from {csv_file} exported to {json_file} successfully.", severity="DEBUG")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        write_to_log('migration.log', f"An error occurred during setup: {e}", severity="ERROR")

    # Prompt for MongoDB connection string and database name
    conn_string = input("\nEnter the MongoDB connection string: ")
    
    # Export the connection string to the JSON file
    with open(json_file, 'r+') as f:
        data = json.load(f)
        data['db_conn_string'] = conn_string  
        f.seek(0)  # Move the cursor to the beginning of the file
        json.dump(data, f, indent=4)
        f.truncate()  # Remove any leftover data from previous content

    print(f"\nMongoDB connection string saved to {json_file}.")
    print("Migration setup completed successfully. You can now proceed with the migration process.")

def make_migration():
    """ Performs the migration by reading the JSON file and inserting data into MongoDB."""
    
    # Get the migration setup file information
    migration_file = input("\nEnter the path to the migration setup JSON file: ")
    if not migration_file.endswith('.json'):
        print("Invalid file format. Please provide a JSON file.")
        return

    csv_files = json.load(open(migration_file, 'r'))['numberOfFiles']

    print(f"Making migration for {csv_files} CSV files...")
    conn_string = json.load(open(migration_file, 'r'))['db_conn_string']
    db_name = 'bidsData'  # Assuming a fixed database name for simplicity 
    collection = mongoDriver.get_mongo_collection(conn_string, db_name, 'bids')  

    for i in range(csv_files):
        csv_file = json.load(open(migration_file, 'r'))['csvFiles'][f'file_{i + 1}']
        data = csvReader.read_csv_data(csv_file)
        #print(data) # Debugging: print the data to be inserted
        mongoDriver.insert_data(collection, data)
        print(f"Data from {csv_file} inserted into MongoDB collection '{collection.name}'.")
        write_to_log('migration.log', f"Data from {csv_file} inserted into MongoDB collection '{collection.name}'.", severity="DEBUG")
    
    print("\nMigration completed successfully. All data has been inserted into MongoDB.")