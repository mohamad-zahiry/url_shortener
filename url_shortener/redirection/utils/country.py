import json

from requests import get


IP_API_URL = "http://ip-api.com/json/%s?fields=country"


def country_name_by_ip(ip: str):
    try:
        name = json.loads(get(IP_API_URL % ip).text)["country"]
    except Exception:
        name = ""
    return name
