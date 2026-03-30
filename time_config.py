from datetime import datetime
from zoneinfo import ZoneInfo

RIYADH_TZ = ZoneInfo("Asia/Riyadh")
DATEPARSER_SETTINGS = {"TIMEZONE": "Asia/Riyadh", "RETURN_AS_TIMEZONE_AWARE": False}


def riyadh_now_naive():
    return datetime.now(RIYADH_TZ).replace(tzinfo=None)
