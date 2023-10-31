from uuid import uuid4 as uid

from pydantic import BaseModel

from connector import *

"""
CONNECTION SETTINGS

"""

CNX = Connector()

"""
Define a post-it note model
"""


class PostIt:
    """
    A post-it note
    """
    container_name = "spatialist_postits"

    id: str = None
    anchor_id: str = ""
    owner: str = ""
    title: str = ""
    type: str = ""
    text_content: str = ""
    media_content: str = ""
    scale: float = 1.0
    rot_x: float = 0.0
    rot_y: float = 0.0
    rot_z: float = 0.0

    def __init__(self, anchor_id, owner, title, type, scale, rot_x, rot_y, rot_z, text_content='', media_content=''):
        self.id = uid().hex
        self.anchor_id = anchor_id
        self.owner = owner
        self.title = title
        self.type = type
        self.text_content = text_content
        self.media_content = media_content
        self.scale = scale
        self.rot_x = rot_x
        self.rot_y = rot_y
        self.rot_z = rot_z

    def check(self):
        if not self.anchor_id:
            raise Exception("anchor_id is required")
        if not self.owner:
            raise Exception("owner is required")
        if not self.title:
            raise Exception("title is required")
        if not self.type:
            raise Exception("type is required")

        if self.type != "text" and self.type != "media":
            raise Exception("type must be either text or media, got: " + self.type)

        if self.type == "text" and not self.text_content:
            raise Exception("text_content is required for text type")
        if self.type == "media" and not self.media_content:
            raise Exception("media_content is required for media type")


    def save(self):
        self.check()
        CNX.create_item(self)
        return self

    def serialize(self):
        item = {
            "id": self.id,
            "anchor_id": self.anchor_id,
            "owner": self.owner,
            "title": self.title,
            "type": self.type,
            "text_content": self.text_content,
            "media_content": self.media_content,
            "scale": self.scale,
            "rot_x": self.rot_x,
            "rot_y": self.rot_y,
            "rot_z": self.rot_z
        }
        return item

    def __str__(self):
        return json.dumps(self.serialize())

class PostItJSON(BaseModel):
    anchor_id: str = ""
    owner: str = ""
    title: str = ""
    type: str = ""
    text_content: str = ""
    media_content: str = ""
    scale: float = 1.0
    rot_x: float = 0.0
    rot_y: float = 0.0
    rot_z: float = 0.0

    def deserialize(self):
        return PostIt(
            anchor_id=self.anchor_id,
            owner=self.owner,
            title=self.title,
            type=self.type,
            text_content=self.text_content,
            media_content=self.media_content,
            scale=self.scale,
            rot_x=self.rot_x,
            rot_y=self.rot_y,
            rot_z=self.rot_z
        )


"""

UserGroupJoin model

Adding this item to the database will add a user to a group / create the group if it doesn't exist

"""


class UserGroupJoinJSON(BaseModel):
    group_name: str = ""
    username: str = ""

    def execute(self):
        container = CNX.get_container("spatialist_organizations")

        """ Get or create a new group """
        group = container.query_items(
            query=f"SELECT * FROM c WHERE c.group_name = '{self.group_name}'",
            enable_cross_partition_query=True
        )
        group = list(group)
        if len(group) == 0:
            group = {
                "id": uid().hex,
                "group_name": self.group_name,
                "users": [self.username]
            }
            container.create_item(group)
        else:
            group = group[0]
            if self.username not in group["users"]:
                group["users"].append(self.username)
                container.replace_item(group["id"], group)

        return group


