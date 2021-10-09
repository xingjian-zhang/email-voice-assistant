# email-voice-assistant
Awesome web voice assistant for email. Course project of EECS 498-006 FA21@umich

## Backend
### Set up backend module
Recommend python3.7+
```
$ cd backend
$ pip install -e .
```
### Run backend module
```
$ ./bin/run_backend    # debug off
$ ./bin/debug_backend  # debug on
```
### HTTP requests
#### Execute command (method: `GET` with _json_)
- Mark as `read`/`unread`
- ...

```
{
   "id": 1,
   "command": "unread",
   "args":{}
}

```
