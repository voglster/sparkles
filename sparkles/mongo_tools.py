from typing import Dict, Any


def replace__id_with_id(r: Dict[str, Any]):
    if "_id" in r:
        r["id"] = str(r["_id"])
        del r["_id"]


def mongo_query_to_list_of_dicts(object_query):
    return [o.to_mongo().to_dict() for o in object_query]


def replace_all_ids(query_results):
    for result in query_results:
        replace__id_with_id(result)


def clean_json(mongoengine_query):
    query_results = mongo_query_to_list_of_dicts(mongoengine_query)
    replace_all_ids(query_results)
    return query_results
