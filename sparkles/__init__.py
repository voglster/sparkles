"""Just utilities made by Jim Vogel"""
import itertools
from collections import namedtuple
from datetime import datetime
from functools import wraps
from typing import Iterable, List
from subprocess import check_output

from loguru import logger
import pytz
import requests

from .mongo_tools import clean_json
from .data_utils import to_dicts
from .parsing import parse_float, parse_int, lower_string

__version__ = "0.1.24"


def logged_user(logger=logger):
    def logging_user_wrapper(func):
        function_name = func.__name__

        @wraps(func)
        def log(*args, **kwargs):
            user = kwargs.get("current_user")
            username = user.username if user else "Unknown User"

            logger.info(f"{username} ran {function_name}")
            return func(*args, **kwargs)

        return log

    return logging_user_wrapper


def now_utc():
    return datetime.now(pytz.utc).replace(second=0, microsecond=0, tzinfo=None)


def trunc_date(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def chunked(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


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


GpsCoords = namedtuple("GpsCoords", "lat,lon")


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


def parse_csl(value, lower=True):
    """
    reads a string that is a comma separated list and converts it into a list of strings
    stripping out white space along the way
    :param value: the string to parse
    :param lower: should we also lowercase everything (default true)
    :return: a list of strings
    """
    value = value.strip()
    if not value:
        return []
    if lower:
        return [t.strip() for t in value.lower().strip().split(",")]
    return [t.strip() for t in value.strip().split(",")]


def sorted_groupby(iterable, key, value=lambda x: x):
    """
    just like regular pythons regular group by except it sorts for you
    :param iterable: the thing to iterate through
    :param key: the key to both sort and group by
    :param value: a function to apply to the group before returning (defaults to groupby iterator)
    :return: iterable of tuples if (key_results, grouped_values)
    """
    return (
        (k, value(v))
        for k, v in itertools.groupby(sorted(iter(iterable), key=key), key=key)
    )


def counter(start=0, step=1):
    count = start
    while True:
        yield count
        count += step


def pairwise(iterable: Iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def get_stdout_lines(command: List[str]) -> List[str]:
    return check_output(command).decode().splitlines()


def lookup(iterable: Iterable, key: callable):
    return {key(i): i for i in iterable}
