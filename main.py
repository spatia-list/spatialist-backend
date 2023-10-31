from fastapi import FastAPI
from models import *

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


"""
POST /postit
"""


@app.post("/postit")
async def create_postit(data: PostItJSON):
    print(data.deserialize())
    data.deserialize().save()
    return {"message": "PostIt created"}


"""
POST /joingroup
"""


@app.post("/joingroup")
async def join_group(data: UserGroupJoinJSON):
    data.execute()
    return {"message": "UserGroupJoin created"}


"""
GET /groups
"""


@app.get("/groups")
async def get_groups():
    groups = CNX.get_groups()
    return {"groups": groups}


"""
GET /postits
"""


@app.get("/postits")
async def get_postits():
    postits = CNX.get_postits()
    return {"postits": postits}
