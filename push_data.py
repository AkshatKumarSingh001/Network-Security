import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()

## Reading data from the source
import pandas as pd
import numpy as np
import pymongo
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            json_records = list(json.loads(data.T.to_json()).values())
            return json_records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_to_mongodb(self, json_records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.json_records = json_records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.json_records)

            return (len(self.json_records))

        except Exception as e:
            raise NetworkSecurityException(e, sys)


def push_data_to_mongodb(
    file_path: str = r"Network_Data\phisingData.csv",
    database: str = "NetworkSecurity",
    collection: str = "NetworkData",
):
    networkobj = NetworkDataExtract()
    json_records = networkobj.csv_to_json(file_path=file_path)
    return networkobj.insert_data_to_mongodb(
        json_records=json_records,
        database=database,
        collection=collection,
    )
        
if __name__ == "__main__":
    no_of_records = push_data_to_mongodb()
    print(f"Number of records inserted: {no_of_records}")