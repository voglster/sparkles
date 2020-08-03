"""Just utilities made by Jim Vogel"""

from collections import namedtuple
from datetime import datetime
from functools import wraps
from typing import List, Iterable

from loguru import logger
import pytz
import requests

__version__ = "0.1.4"


def logged_user(func):
    @wraps(func)
    def log(*args, **kwargs):
        logger.info(f"{kwargs['current_user'].username} ran {func.__name__}")
        return func(*args, **kwargs)

    return log


def clean_json(object_query):
    ret = [o.to_mongo().to_dict() for o in object_query]
    for r in ret:
        if "_id" in r:
            r["id"] = str(r["_id"])
            del r["_id"]
    return ret


def to_dicts(ds):
    if not ds:
        return []
    header = ds[0]
    return [dict(zip(header, row)) for row in ds[1:]]


def parse_float(value: str):
    return float(value.replace(",", ""))


def now_utc():
    return datetime.now(pytz.utc).replace(second=0, microsecond=0, tzinfo=None)


def add_key_from_id(data: Iterable[dict]):
    for row in data:
        row["key"] = row["id"]


def quick_search(query, model, fields=None, base_raw_query=None):
    fields = fields or model.quick_search_fields
    query = query.lower()
    ret = []
    for title, field_name in fields:
        values_with_query_in_it = [
            f
            for f in model.objects(__raw__=base_raw_query or {}).distinct(
                field=field_name
            )
            if query in f.lower()
        ]

        options = []
        for value in values_with_query_in_it:
            row_count = len(
                model.objects(__raw__={**(base_raw_query or {}), field_name: value})
            )
            options.append(
                {"label": value, "count": row_count, "filter": {field_name: value}}
            )
        if options:
            ret.append({"title": title, "options": options})

    return ret


def pairwise(items):
    items = list(items)
    return zip(items[:-1], items[1:])


GpsCoords = namedtuple("GpsCoords", "lat,lon")


def counter(start=0, step=1):
    count = start
    while True:
        yield count
        count += step


def build_send_slack_message(prefix, slack_webhook):
    def send_slack_message(message):
        from notifiers import get_notifier

        message = f"{prefix} | {message}"

        lines = message.splitlines(keepends=True)
        line_count = len(lines)
        if line_count > 10:
            url, worked = send_to_haste_bin(message)
            if worked:
                slack_message = "".join(
                    [lines[0], f"{line_count} lines long, pasted here: {url}"]
                )
            else:
                slack_message = message + "\n" + url
        else:
            slack_message = message

        notifier = get_notifier("slack")
        try:
            notifier.notify(webhook_url=slack_webhook, message=slack_message)
        except Exception:
            pass

    return send_slack_message


HASTEBIN = "https://hastebin.com/"


def send_to_haste_bin(message):
    try:
        response = requests.post(f"{HASTEBIN}documents", message.encode("utf-8"))
        return f'{HASTEBIN}{response.json()["key"]}', True
    except Exception:
        import traceback

        return f"Failed to send to hastebin, {traceback.format_exc()}", False
