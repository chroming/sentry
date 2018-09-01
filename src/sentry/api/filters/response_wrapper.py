
import json
from functools import wraps

from rest_framework.response import Response


def _remove_data_keys(data, items):
    """
    Remove items from a dict.
    :param data: a dict data
    :param items: remove items, such as {"1":True, "2":{"3":True}}
    :return: changed data

    ATTENTION: THIS FUNCTION WILL CHANGE ORIGINAL DATA.

    """
    if isinstance(data, dict):
        for k, v in items.items():
            if v is True:
                data.pop(k, None)
            elif isinstance(v, dict):
                _remove_data_keys(data.get(k, {}), v)
    elif isinstance(data, list):
        for k in data:
            _remove_data_keys(k, items)
    return data


def _save_data_keys(data, items):
    """
    Change dict and only keep given items.
    :param data: a dict data
    :param items: keep items , such as {"1":True, "2":{"3":True}}
    :return: changed data
    """
    if isinstance(data, dict):
        new_data = {}
        for k, v in items.items():
            if k in data:
                if v is True:
                    new_data[k] = data[k]
                elif isinstance(v, dict):
                    new_v = _save_data_keys(data.get(k), v)
                    if new_v is not None:
                        new_data[k] = new_v
    elif isinstance(data, list):
        new_data = []
        for k in data:
            new_v = _save_data_keys(k, items)
            if new_v is not None:
                new_data.append(new_v)
    else:
        new_data = data if items is True else None
    return new_data


def change_data_keys(remove_items=None, save_items=None):
    """
    A wrapper for sentry api endpoints method.
    This wrapper will change the response.data
    with remove some items or keep some items.

    Usage:

    Class Endpoint():
        @change_data_keys(remove_items={"1":True, "2":{"3":True}})
        def get(request):
            pass

    Class Endpoint():
        @change_data_keys(save_items={"1":True, "2":{"3":True}})
        def get(request):
            pass

    """
    def decorate(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            response = func(*args, **kwargs)
            if remove_items:
                _remove_data_keys(response.data, remove_items)
            elif save_items:
                response.data = _save_data_keys(response.data, save_items)
            return response
        return wrap
    return decorate


def remove_data_keys(items):
    """Same as change_data_keys(remove_items=items)"""
    return change_data_keys(remove_items=items)


def save_data_keys(items):
    """Same as change_data_keys(save_items=items)"""
    return change_data_keys(save_items=items)


def add_post_method(cls):
    """
    Add post method to sentry api endpoint class.
    The post method will receive postdata
    with 'remove' key or 'save' key,
    then send key and data to change_data_keys

    """
    def post(self, request, *args, **kwargs):

        def _get_remove_and_save(data):
            return json.loads(data.get('remove', '{}')), json.loads(data.get('save', '{}'))

        if not request.user.is_authenticated():
            return Response(status=401)
        remove_data, save_data = _get_remove_and_save(request.DATA)
        return change_data_keys(remove_data, save_data)(self.get)(request, *args, **kwargs)

    setattr(cls, 'post', post)
    return cls
