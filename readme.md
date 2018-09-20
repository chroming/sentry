This fork add two API to releases/9.0.x:

+ Delete single event;
+ Filter response for endpoint;

## Usage

### Delete single event

Like https://docs.sentry.io/api/events/get-project-event-details , just change method "GET" to "DELETE":

`DELETE /api/0/projects/{organization_slug}/{project_slug}/events/{event_id}/`

A demo with python:

```python
import requests

BASE_URL = "http://sentry_server:9000/api/0/projects/sentry/python/events/"

HEADERS = {
    "Authorization": "Bearer *********************************************************" # API token
}


def delete_event(event_id):
    return requests.delete(BASE_URL + event_id + '/', headers=HEADERS).status_code


if __name__ == '__main__':
    print(delete_event('**********************'))  # Event id
```

### Filter result with post method


Like https://docs.sentry.io/api/events/get-project-event-details , 
just change method "GET" to "POST" and choice one post body: "remove":{key:true} (for remove some key)
or "save":{key:true} (for leave only some key)


If you want to change the response in GET method, you can add a wrapper like this:

```python
from sentry.api.filters.response_wrapper import change_data_keys 

Class Endpoint():
    @change_data_keys(remove_items={"1":True, "2":{"3":True}})
    def get(request):
        pass

Class Endpoint():
    @change_data_keys(save_items={"1":True, "2":{"3":True}})
    def get(request):
        pass

```


Original sentry [readme](README.rst)