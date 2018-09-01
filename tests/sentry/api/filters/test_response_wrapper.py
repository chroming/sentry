

from sentry.api.filters.response_wrapper import _remove_data_keys, _save_data_keys


def test_remove_data_keys():
    assert _remove_data_keys({}, {}) == {}
    assert _remove_data_keys({}, {'1': True}) == {}
    assert _remove_data_keys({'1': '2', '3': {'4': '5'}}, {'3': {'4': True}}) == {'1': '2', '3': {}}
    assert _remove_data_keys({'1': '2', '3': {'4': '5'}}, {'1': True}) == {'3': {'4': '5'}}
    assert _remove_data_keys({'1': '2', '3': {'4': '5'}}, {'1': False}) == {'1': '2', '3': {'4': '5'}}
    assert _remove_data_keys({'1': '2', '3': {'4': '5', '6': '7'}}, {'3': {'4': True}}) == {'1': '2', '3': {'6': '7'}}
    assert _remove_data_keys({'1': '2', '3': {'4': '5', '6': '7'}}, {'3': {'4': True, '6': True}}) == {'1': '2', '3': {}}
    assert _remove_data_keys({'1': '2', '3': {'4': '5', '6': '7'}}, {'3': True}) == {'1': '2'}
    assert _remove_data_keys({'1': '2', '3': [{'4': '5'}, {'6': '7'}]}, {'3': {'4': True}}) == {'1': '2', '3': [{}, {'6': '7'}]}
    assert _remove_data_keys({'1': '2', '3': [{'4': '5'}, {'4': '7'}]}, {'3': {'4': True}}) == {'1': '2', '3': [{}, {}]}
    assert _remove_data_keys({'1': '2', '3': [{'4': '5'}, {'6': '7'}]}, {'1': True, '3': {'4': True}}) == {'3': [{}, {'6': '7'}]}


def test_save_data_keys():
    assert _save_data_keys({}, {}) == {}
    assert _save_data_keys({}, {'1': True}) == {}
    assert _save_data_keys({'1': '2', '3': {'4': '5'}}, {'3': {'4': True}}) == {'3': {'4': '5'}}
    assert _save_data_keys({'1': '2', '3': {'4': '5'}}, {'3': {'5': True}}) == {'3': {}}
    assert _save_data_keys({'1': '2', '3': {'4': '5'}}, {'1': True, '3': {'4': True}}) == {'1': '2', '3': {'4': '5'}}
    assert _save_data_keys({'1': '2', '3': {'4': '5'}}, {'1': True}) == {'1': '2'}
    assert _save_data_keys({'1': '2', '3': {'4': '5'}}, {'1': False}) == {}
    assert _save_data_keys({'1': '2', '3': {'4': '5', '6': '7'}}, {'3': {'4': True}}) == {'3': {'4': '5'}}
    assert _save_data_keys({'1': '2', '3': {'4': '5', '6': '7'}}, {'3': {'4': True, '6': True}}) == {'3': {'4': '5', '6': '7'}}
    assert _save_data_keys({'1': '2', '3': {'4': '5', '6': '7'}}, {'3': True}) == {'3': {'4': '5', '6': '7'}}
    assert _save_data_keys({'1': '2', '3': [{'4': '5'}, {'6': '7'}]}, {'3': {'4': True}}) == {'3': [{'4': '5'}, {}]}
    assert _save_data_keys({'1': '2', '3': [{'4': '5'}, {'4': '7'}]}, {'3': {'4': True}}) == {'3': [{'4': '5'}, {'4': '7'}]}
    assert _save_data_keys({'1': '2', '3': [{'4': '5'}, {'6': '7'}]}, {'1': True, '3': {'4': True}}) == {'1': '2', '3': [{'4': '5'}, {}]}









