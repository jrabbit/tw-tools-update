from datetime import datetime, date


def isObsolete(lastUpdated: datetime) -> bool:
    return (date.today() - lastUpdated.date()).days > 3 * 365