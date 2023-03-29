# 2023-03-28
# api/utils/helper_funcs.py

from datetime import datetime

def getMaxLastModifiedHeader(myList):
    datetime_max = max(myList) if len(myList) > 0 else None
    return toLastModifiedHeader(datetime_max)

def toLastModifiedHeader(myDate):
    timestamp = None
    if isinstance(myDate, datetime):
        timestamp = myDate.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return timestamp
