import io
import json
from zoneinfo import ZoneInfo

from querystring_parser import parser
from django.utils import timezone
from datetime import datetime, timedelta
import base64
from _main_.utils.errors import APIError
import logging
from dateutil import tz

log = logging.getLogger(__name__)


def custom_timezone_info(zone="UTC"):
    return ZoneInfo(zone)


def tz_aware_utc_now():
    return datetime.datetime.now(datetime.timezone.utc)


def get_date_and_time_in_milliseconds(**kwargs):
    hours = kwargs.get("hours", None)
    date = timezone.now()
    if hours:
        delta = timedelta(hours=hours)
        date = date + delta
    current_time_in_ms = date.timestamp() * 1000
    return current_time_in_ms


def get_request_contents(request, **kwargs):
    filter_out = kwargs.get("filter_out")
    try:
        if request.method != "POST":
            return request.GET.dict()

        args = {}
        if request.content_type == "application/x-www-form-urlencoded":
            args = parser.parse(request.POST.urlencode())
        elif request.content_type == "application/json":
            args = json.loads(request.body)
        elif request.content_type == "multipart/form-data":
            args = request.POST.dict()
            if request.FILES:
                for i in request.FILES.dict():
                    args[i] = request.FILES[i]
        else:
            args = request.POST.dict()

        if filter_out:
            for key in filter_out:
                args.pop(key, None)
        return args

    except Exception as e:
        log.error(str(e), exc_info=True)
        return {}


def parse_list(d):
    try:
        tmp = []
        if isinstance(d, str):
            tmp = d.strip().split(",") if d else []
        elif isinstance(d, dict):
            tmp = list(d.values())

        res = []
        for i in tmp:
            if i.isnumeric():
                res.append(i)
        return res

    except Exception as e:
        log.error(str(e), exc_info=True)
        return []


def parse_dict(d: object) -> object:
    try:
        return json.loads(d)
    except Exception as e:
        log.error(str(e), exc_info=True)
        return dict()


def parse_str_list(d):
    try:
        if d and isinstance(d, str):
            tmp = [t.strip() for t in d.strip().split(",") if t.strip()]
            return tmp
        return []
    except Exception as e:
        log.error(str(e), exc_info=True)
        return []


def parse_bool(b):
    if not b:
        return False
    return (
        (isinstance(b, bool) and b)
        or (b == "true")
        or (b == "1")
        or (b == 1)
        or (b == "True")
    )


def parse_string(s):
    try:
        s = str(s)
        if s == "undefined" or s == "null":
            return None
        return s
    except Exception as e:
        log.error(str(e), exc_info=True)
        return None


def parse_int(b):
    if not str(b).isdigit():
        raise ValueError("Input must be a digit")
    try:
        return int(b)
    except Exception as e:
        log.error(str(e), exc_info=True)
        return 1


def parse_date(d):
    try:
        if d == "undefined" or d == "null":  # providing date as 'null' should clear it
            return None
        if len(d) == 10:
            return datetime.strptime(d, "%Y-%m-%d").replace(
                tzinfo=custom_timezone_info()
            )
        else:
            return datetime.strptime(d, "%Y-%m-%d %H:%M").replace(
                tzinfo=custom_timezone_info()
            )

    except Exception as e:
        log.exception(e)
        return timezone.now()


def rename_field(args, old_name, new_name):
    oldVal = args.pop(old_name, None)
    if oldVal:
        args[new_name] = oldVal
    return args


def rename_fields(args, pairs):
    for old_name, new_name in pairs:
        args = rename_field(args, old_name, new_name)
    return args


def serialize_all(data, full=False, **kwargs):
    return [d.to_json() for d in data]


def serialize(data, full=False, **kwargs):
    info = (kwargs or {}).get("info", False)
    if not data:
        return {}

    if full:
        return data.full_json()
    elif info:
        return data.info()

    return data.to_json()


def check_length(args, field, min_length=5, max_length=40):
    data = args.get(field, None)
    if not data:
        return False, APIError(f"Please provide a {field} field")

    data_length = len(data)
    if data_length < min_length or data_length > max_length:
        return False, APIError(
            f"{field} has to be between {min_length} and {max_length}"
        )
    return True, None


def is_value(b):
    if b and b != "undefined" and b != "NONE":
        return True
    if b == "":  # an empty string is a string value
        return True
    return False


def _common_name(s):
    return (" ".join(s.split("_"))).title()


def validate_fields(args, checklist):
    for field in checklist:
        if field not in args:
            return False, APIError(f"You are missing: {_common_name(field)}")
    return True, None


def get_cookie(request, key):
    cookie = request.COOKIES.get(key)
    if cookie and len(cookie) > 0:
        return cookie
    else:
        return None


def set_cookie(response, key, value):
    MAX_AGE = 31536000
    response.set_cookie(key, value, MAX_AGE, samesite="Strict")


def local_time():
    local_zone = tz.tzlocal()
    dt_utc = tz_aware_utc_now()
    local_now = dt_utc.astimezone(local_zone)
    return local_now


def utc_to_local(iso_str):
    local_zone = tz.tzlocal()
    dt_utc = datetime.datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=custom_timezone_info()
    )
    local_now = dt_utc.astimezone(local_zone)
    return local_now


def encode_data_for_URL(data):
    return base64.b64encode(json.dumps(data).encode()).decode()
