import os
import json
import hashlib
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
        print(new_item)
        container.create_item(new_item)

    def get_groups(self):
        container = self.get_container("spatialist_organizations")
        res = container.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True
        )

        return list(res)

    def save_to_buffer(self, item):
        container = self.get_container("spatialist_swipes")
        container.create_item(item.serialize())

    def get_postits(self):
        container = self.get_container("spatialist_postits")
        res = container.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True
        )

        return list(res)

    def get_postits_by_username(self, username):
        container = self.get_container("spatialist_postits")
        res = container.query_items(
            query=f"SELECT * FROM c WHERE c.owner = '{username}'",
            enable_cross_partition_query=True
        )

        return list(res)

    def get_swipe_by_username(self, username):
        container = self.get_container("spatialist_swipes")

        # order by oldest first
        res = container.query_items(
            query=f"SELECT * FROM c WHERE c.owner= '{username}' ORDER BY c._ts ASC",
            enable_cross_partition_query=True
        )
        res_list = list(res)
        if len(res_list) == 0:
            return {"hasSwipe": False, "postit": None}

        # get the oldest item
        postit = res_list[0]
        # delete the item
        container.delete_item(postit, partition_key=postit["owner"])

        return {"hasSwipe": True, "postit": postit}


    def get_postits_anchor(self, anchor_id):
        container = self.get_container("spatialist_postits")
        res = container.query_items(
            query=f"SELECT * FROM c WHERE c.anchor_id = '{anchor_id}'",
            enable_cross_partition_query=True
        )

        return list(res)

    def delete_postit(self, id):
        container = self.get_container("spatialist_postits")
        targets = container.query_items(
            query=f"SELECT * FROM c WHERE c.id = '{id}'",
            enable_cross_partition_query=True
        )
        res = list(targets)
        print(res)
        if len(res) == 0:
            print("PostIt not found")
            raise Exception("PostIt not found")

        for target in res:
            print("deleting the item with id: " + target["id"] + " and owner: " + target["owner"])
            container.delete_item(target, partition_key=target["owner"])

    def get_anchors_by_group(self, group_name):
        """
        Return anchors where the owner is the group name
        """

        container = self.get_container("spatialist_anchors")
        # get all items
        print(group_name)
        res = container.query_items(
            query=f"SELECT * FROM c WHERE c.owner = '{group_name}'",
            enable_cross_partition_query=True
        )

        # return only 30 items
        res = list(res)
        if len(res) > 30:
            res = res[:30]
        return res

    def get_postits_hash(self):
        """
        Calculate a hash the modification time
        :return:
        """

        container = self.get_container("spatialist_postits")
        # get only the most recent item
        res = container.query_items(
            query="SELECT TOP 1 * FROM c ORDER BY c._ts DESC",
            enable_cross_partition_query=True
        )
        res = list(res)

        # calculate sha256
        sha256 = hashlib.sha256()
        sha256.update(json.dumps(res).encode("utf-8"))
        return sha256.hexdigest()

    def get_anchors_hash(self):
        """
        Calculate a hash the modification time
        :return:
        """

        container = self.get_container("spatialist_anchors")
        # get only the most recent item
        res = container.query_items(
            query="SELECT TOP 1 * FROM c ORDER BY c._ts DESC",
            enable_cross_partition_query=True
        )
        res = list(res)

        # calculate sha256
        sha256 = hashlib.sha256()
        sha256.update(json.dumps(res).encode("utf-8"))
        return sha256.hexdigest()

