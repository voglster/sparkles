import pytest
from sparkles.mongo_tools import (
    replace__id_with_id,
    mongo_query_to_list_of_dicts,
    clean_json,
)


class MockMongoEngObj:
    def to_mongo(self):
        return MockInner()


class MockInner:
    def to_dict(self):
        return {"_id": 123}


@pytest.fixture
def mongoengine_query():
    return [MockMongoEngObj()]


def test_replace__id_with_id_actually_replaces():
    data = {"_id": "3"}
    replace__id_with_id(data)
    assert data == {"id": "3"}


def test_replace__id_with_id_doesnt_fail_without_an_id():
    data = {"qid": 3}
    replace__id_with_id(data)
    assert data == {"qid": 3}


def test_replace__id_with_id_stringifies():
    data = {"_id": 3}
    replace__id_with_id(data)
    assert data == {"id": "3"}


def test_converting_mongo_query_result_is_list(mongoengine_query):
    result = mongo_query_to_list_of_dicts(mongoengine_query)
    assert type(result) is list


def test_converting_mongo_query_first_result_is_dict(mongoengine_query):
    result = mongo_query_to_list_of_dicts(mongoengine_query)
    assert type(result[0]) is dict


@pytest.fixture
def cleaned_mongo_json(mongoengine_query):
    return clean_json(mongoengine_query)


def test_clean_json_result_is_a_list(cleaned_mongo_json):
    assert type(cleaned_mongo_json) is list


def test_clean_json_first_result_is_a_dict(cleaned_mongo_json):
    assert type(cleaned_mongo_json[0]) is dict


def test_clean_json_results_dont_have__id(cleaned_mongo_json):
    assert not any("_id" in r for r in cleaned_mongo_json)
