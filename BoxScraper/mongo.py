import json
from os import getenv
from typing import Iterator, Dict, Optional

from pymongo import MongoClient
from dotenv import load_dotenv


class Mongo:
    """ MongoDB Data Model """
    load_dotenv()
    db_url = getenv("DB_URL")
    db_name = getenv("DB_NAME")
    db_table = getenv("DB_TABLE")

    def search(self, search: str):
        return self.connect().find(
            {"$text": {"$search": search}},
            {"_id": False, "text": False},
        )

    def find(self, query: Dict) -> Iterator[Dict]:
        return self.connect().find(query, {"_id": False})

    def find_one(self, query: Dict) -> Optional[Dict]:
        return self.connect().find_one(query, {"_id": False})

    def find_all(self):
        return self.connect().find({}, {"_id": False})

    def count(self, query: Dict):
        return self.connect().count_documents(query)

    def insert(self, data: Dict):
        self.connect().insert_one(data)

    def update(self, query: Dict, data_update: Dict):
        self.connect().update_one(query, {"$set": data_update})

    def delete(self, query: Dict):
        self.connect().delete_many(query)

    def connect(self):
        return MongoClient(self.db_url)[self.db_name][self.db_table]

    def add_tag(self, box_id: str, tag: str):
        self.connect().update({'box_id': box_id}, {'$push': {'tags': tag}})

    def remove_tag(self, box_id: str, tag: str):
        self.connect().update({'box_id': box_id}, {'$pull': {'tags': tag}})

    def backup(self):
        data = list(self.connect().find({}, {"_id": False}))
        file_name = "data.json"
        with open(file_name, "w") as file:
            json.dump(data, file)
