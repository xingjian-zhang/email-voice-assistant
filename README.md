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
---

## NLP
### Set up NLP module
Recommend python3.7+
```
$ cd nlp
$ pip install -e .
```
### Run backend module
```
$ ./bin/run_nlp    # debug off
$ ./bin/debug_nlp  # debug on
```
---

## Frontend
### Set up frontend dependencies
For local test, require node>=14.0.0 and npm>=5.6
```
$ cd frontend
$ yarn install
```
### Run frontend module
```
$ yarn start
```