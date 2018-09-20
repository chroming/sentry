import requests

BASE_URL = "http://192.168.68.128:9000/api/0/projects/sentry/python/events/"

HEADERS = {
    "Authorization": "Bearer *********************************************************"
}


def delete_event(event_id):
    return requests.delete(BASE_URL + event_id + '/', headers=HEADERS).status_code


if __name__ == '__main__':
    print(delete_event('**********************'))