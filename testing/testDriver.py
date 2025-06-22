# FIXTHIS: Update this file to use the test classes that are defined in the other files
# in this folder instead of manually testing the functions you're working on. 

# System level imports to get parent directory items
import sys
import os

# Local imports for csvReader and mongoDriver modules
# Get the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)
import csvReader
import mongoDriver

def test_csv_import():
    ''' Tests the ability for the csv import to read the csv
        and import into the mongoDB database 
        
    '''

    collection = mongoDriver.connect_to_mongo('bidsData', 'bids')
    #print(collection)

    csv_file = 'res/sample_data.csv'  # Path to the CSV file containing the data
    database = 'bidsData'
    collection_name = 'bids'

    # Test inserting the data from the CSV file into MongoDB
    inserted_data = csvReader.read_csv_data(csv_file)
    mongoDriver.insert_data(collection, inserted_data)

    print(f"Inserted {len(inserted_data)} records into the MongoDB collection '{collection_name}' in database '{database}'.")

print("Testing MongoDB connection...")
# FIXTHIS: Update this to pull in the connection string from a config file
conn_string = "mongodb://dataUser:Passw0rd%5E@localhost:27017/?authSource=bidsData"
# Test connection to MongoDB using the connection string
collection = mongoDriver.get_mongo_collection(conn_string, 'bidsData', 'bids')

print(collection)

if collection is not None:
    print("MongoDB connection successful.")
    
else:
    print("Failed to connect to MongoDB.")

# Get some collection data
print("Testing CSV import...")