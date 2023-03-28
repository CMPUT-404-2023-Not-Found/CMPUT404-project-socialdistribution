from datetime import datetime

def toLastModifiedHeader(myDate):
    timestamp = None
    if isinstance(myDate, datetime):
        timestamp = myDate.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return timestamp
