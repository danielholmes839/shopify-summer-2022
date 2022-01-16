from datetime import datetime


def now() -> str:
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
