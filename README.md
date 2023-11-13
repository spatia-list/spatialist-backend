# Spatialist Backend

### Quickstart

To run the backend, use `make run` (or `make local` to build and run a docker container).
You might need to manually install dependencies if you choose not to use docker.

## API documentation

### Hello  `[GET]/`  
Returns hello world, used to test if the server is running.

### Create a PostIt  `[POST]/postit`

Create a new postit.

JSON format:
```json
{
    "anchor_id": ID of the associated spatial anchor,
    "owner": name of owner,
    "title": title of the postit,
    "type": type of the postit {"text", "media"},
    "text_content": REQUIRED if "text" - text content of the postit,
    "media_content": REQUIRED if "media" - media content of the postit,
    "rgb": [R value, G value, B value] - color of the postit,
    "position": [x,y,z] transform relative to the anchor,
    "rotation": [x,y,z,w] rotation relative to the anchor,
}
```

Example:
```json
{
    "anchor_id": "1234567890",
    "owner": "John Doe",
    "title": "My first postit",
    "type": "text",
    "text_content": "Hello world!",
    "rgb": [255, 0, 0],
    "position": [0,0,0],
    "rotation": [0,0,0,1]
}
```

### Delete a PostIt  `[DEL]/postit/<postit_id>`
Delete a postit.

Returns a message in JSON format:
```json
{
    "message": "PostIt deleted"
}
```
or
```json
{
    "message": "PostIt not deleted::<reason>"
}
```

### Get all PostIts  `[GET]/postits`
Get all postits.

Example result:
```json
{
    "postits": [
        {
            "id": "1ca219c09bff4c6d8989c75b48efd0b5",
            "anchor_id": "1",
            "owner": "mrztti",
            "title": "A third postit",
            "type": "text",
            "text_content": "Hello World!",
            "media_content": "",
            "rgb": [
                255,
                100,
                100
            ],
            "_rid": "WOMYALEiAvwGAAAAAAAAAA==",
            "_self": "dbs/WOMYAA==/colls/WOMYALEiAvw=/docs/WOMYALEiAvwGAAAAAAAAAA==/",
            "_etag": "\"2b010907-0000-0d00-0000-6548b9150000\"",
            "_attachments": "attachments/",
            "_ts": 1699264789
        },
        {
            "id": "095dd744953c42ad8ae258fa471975a6",
            "anchor_id": "1",
            "owner": "mrztti",
            "title": "A third postit",
            "type": "text",
            "text_content": "Hello World!",
            "media_content": "",
            "rgb": [
                255,
                100,
                100
            ],
            "pose": {
                "position": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "orientation": {
                    "w": 1,
                    "x": 0,
                    "y": 0,
                    "z": 0
                }
            },
            "_rid": "WOMYALEiAvwHAAAAAAAAAA==",
            "_self": "dbs/WOMYAA==/colls/WOMYALEiAvw=/docs/WOMYALEiAvwHAAAAAAAAAA==/",
            "_etag": "\"06039996-0000-0d00-0000-6552388a0000\"",
            "_attachments": "attachments/",
            "_ts": 1699887242
        }
    ]
}
```

### Get PostIts by Anchor  `[GET]/postit/<postit_id>`

Specify an anchor ID to filter only based on the surrounding found anchors.

Same result as `GET /postits` but filtered by anchor ID.

### Get all user groups  `[GET]/groups`

Returns all available groups and their users.

Example:
```json
{
    "groups": [
        {
            "id": "e2a6e0300f6e4fe682a20a03e597e067",
            "group_name": "Test Group",
            "users": [
                "mrztti",
                "mrztti",
                "mrztti2",
                "test"
            ],
            "_rid": "WOMYAMCt-IUCAAAAAAAAAA==",
            "_self": "dbs/WOMYAA==/colls/WOMYAMCt-IU=/docs/WOMYAMCt-IUCAAAAAAAAAA==/",
            "_etag": "\"8f00927a-0000-0d00-0000-6543afb80000\"",
            "_attachments": "attachments/",
            "_ts": 1698934712
        }
    ]
}
```

### Join/Create group `[POST]/joingroup`

Create a request to either join a group or create a new group.

JSON format:
```json
{
    "group_name": name of the group,
    "user": name of the user
}
```

Example:
```json
{
    "group_name": "Test Group",
    "user": "mrztti"
}
```



