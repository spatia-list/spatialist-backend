import os
import json
from uuid import uuid4 as uid

from azure.cosmos import CosmosClient

from dotenv import load_dotenv
load_dotenv()

DATABASE_NAME = "test"

DB_URL = os.getenv("DB_URL")
DB_KEY = os.getenv("DB_KEY")

class Connector:
    client = None

    def __init__(self):
        self.client = CosmosClient(url=DB_URL, credential=DB_KEY)


    def get_container(self, name):
        return self.client.get_database_client(DATABASE_NAME).get_container_client(name)
    def create_item(self, item):
        new_item = item.serialize()
        container = self.get_container(item.container_name)
        container.create_item(new_item)

    def get_groups(self):
        container = self.get_container("spatialist_organizations")
        res = container.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True
        )

        return list(res)

    def get_postits(self):
        container = self.get_container("spatialist_postits")
        res = container.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True
        )

        return list(res)