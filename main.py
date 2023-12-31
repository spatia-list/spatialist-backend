from fastapi import FastAPI
from models import *
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse('static/index.html')


@app.get("/swipe")
async def root():
    return FileResponse('static/swipe.html')

@app.get("/list")
async def root():
    return FileResponse('static/list.html')

@app.get("/listbygroup")
async def root():
    return FileResponse('static/listbygroup.html')

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
POST /anchor
"""


@app.post("/anchor")
async def create_anchor(data: LocalAnchorJSON):
    print(data)
    data.deserialize().save()
    return {"message": "Anchor created"}


"""
DEL /postit
"""


@app.delete("/postit/{id}")
async def delete_postit(id: str):
    try:
        CNX.delete_postit(id)
    except Exception as e:
        return {"message": "PostIt not deleted::" + str(e)}
    return {"message": "PostIt deleted"}


@app.delete("/postits")
async def delete_postits():
    try:
        CNX.remove_all_postits()
    except Exception as e:
        return {"message": "PostIts not deleted::" + str(e)}
    return {"message": "All postits deleted"}

@app.get("/redirect")
async def redirect():
    response = RedirectResponse(url='/static/poster.html')
    return response

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

@app.delete("/group/{name}")
async def delete_group(name: str):
    CNX.delete_group(name)
    return {"message": "Group deleted"}


"""
GET /postits
"""


@app.get("/postits")
async def get_postits():
    postits = CNX.get_postits()
    return {"postits": postits}

@app.get("/postitsUser/{username}")
async def get_postits_by_username(username: str):
    postits = CNX.get_postits_by_username(username)
    return {"postits": postits}


"""
GET /postits/{anchor_id}
"""


@app.get("/postits/{anchor_id}")
async def get_postits_by_anchor(anchor_id: str):
    postits = CNX.get_postits_anchor(anchor_id)
    return {"postits": postits}


"""
GET /anchors/{group}
"""


@app.get("/anchors/{group_name}")
async def get_anchors_by_group(group_name: str):
    anchors = CNX.get_anchors_by_group(group_name)
    return {"anchors": anchors}


@app.delete("/anchors")
async def delete_anchors():
    CNX.remove_all_anchors()
    return {"message": "All anchors deleted"}

"""
GET /currentHash
"""


@app.get("/postitsHash")
async def get_current_hash():
    return {"hash": CNX.get_postits_hash()}

@app.get("/anchorsHash")
async def get_anchors_hash():
    return {"hash": CNX.get_anchors_hash()}


"""
Postit swipe system

1 - Register a postit in the buffer (POST /createFromSwipe)
2 - Client queries to see if buffer for their username has a new postit (GET /hasSwipe)
"""


@app.post("/createFromSwipe")
async def create_from_swipe(data: SwipeJSON):
    print(data)
    msg = data.deserialize()
    CNX.save_to_buffer(msg)
    return {"message": "Swipe PostIt created"}

@app.get("/hasSwipe/{username}")
async def has_swipe(username: str):
    return CNX.get_swipe_by_username(username)
