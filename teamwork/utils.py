from datetime import datetime, timedelta

def json_serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, timedelta):
        # return duration in hours
        return round(obj.total_seconds() / 3600, 1)
    else:
        raise TypeError ('Type not serializable')
