from dataclasses import dataclass
from uuid import uuid4 as uid

from pydantic import BaseModel

from connector import *

"""
CONNECTION SETTINGS

"""

CNX = Connector()

@dataclass
class Quaternion:
    x: float
    y: float
    z: float
    w: float

    def serialize(self):
        return {
            "w": self.w,
            "x": self.x,
            "y": self.y,
            "z": self.z
        }

    def __str__(self):
        return json.dumps(self.serialize())

    def __repr__(self):
        return self.__str__()

@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def serialize(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }

    def __str__(self):
        return json.dumps(self.serialize())

    def __repr__(self):
        return self.__str__()

@dataclass
class Pose:
    position: Vector3
    orientation: Quaternion

    def serialize(self):
        return {
            "position": self.position.serialize(),
            "orientation": self.orientation.serialize()
        }

    def __str__(self):
        return json.dumps(self.serialize())

    def __repr__(self):
        return self.__str__()

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
    rgb = None
    pose: Pose = None

    def __init__(self, anchor_id, owner, title, type, pose, text_content='', media_content='', rgb=None):
        self.id = uid().hex
        self.anchor_id = anchor_id
        self.owner = owner
        self.title = title
        self.type = type
        self.text_content = text_content
        self.media_content = media_content
        self.rgb = rgb
        self.pose = pose

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

        if self.rgb:
            # check that we have 3 values
            if len(self.rgb) != 3:
                raise Exception("rgb must be an array of 3 values")

            # check that each value is an integer between 0 and 255
            for val in self.rgb:
                if not isinstance(val, int):
                    raise Exception("rgb values must be integers")
                if val < 0 or val > 255:
                    raise Exception("rgb values must be between 0 and 255")
        else:
            self.rgb = [0, 255, 255]

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
            "rgb": self.rgb,
            "pose": self.pose.serialize() if self.pose else None
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
    rgb: list | None = [0, 255, 255]
    position: list | None = [0.0, 0.0, 0.0]
    rotation: list | None = [0.0, 0.0, 0.0, 1.0]

    def deserialize(self):
        pose = Pose(
            position=Vector3(
                x=self.position[0],
                y=self.position[1],
                z=self.position[2]
            ),
            orientation=Quaternion(
                x=self.rotation[0],
                y=self.rotation[1],
                z=self.rotation[2],
                w=self.rotation[3]
            )
        )
        return PostIt(
            anchor_id=self.anchor_id,
            owner=self.owner,
            title=self.title,
            type=self.type,
            text_content=self.text_content,
            media_content=self.media_content,
            rgb=self.rgb,
            pose=pose
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

class LocalAnchor:
    """
    A local anchor
    """
    container_name = "spatialist_anchors"

    id: str = None
    anchor_id: str = ""
    owner: str = ""

    def __init__(self, anchor_id, owner):
        self.id = uid().hex
        self.anchor_id = anchor_id
        self.owner = owner

    def check(self):
        if not self.anchor_id:
            raise Exception("anchor_id is required")
        if not self.owner:
            raise Exception("owner is required")

    def save(self):
        self.check()
        CNX.create_item(self)
        return self

    def serialize(self):
        item = {
            "id": self.id,
            "anchor_id": self.anchor_id,
            "owner": self.owner
        }
        return item

    def __str__(self):
        return json.dumps(self.serialize())

class LocalAnchorJSON(BaseModel):
    anchor_id: str = ""
    owner: str = ""

    def deserialize(self):
        return LocalAnchor(
            anchor_id=self.anchor_id,
            owner=self.owner
        )


