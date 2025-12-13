from datetime import datetime


def get_weekday(date: str) -> int:
    """
    get_weekday 的 Docstring

    :param date: YYYY-MM-DD
    :type date: str
    :return: 0-sunday 1-monday ...
    :rtype: int
    """
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")

        weekday = date_obj.weekday()

        target_weekday = (weekday + 1) % 7

        return target_weekday
    except ValueError:
        raise ValueError(f"Invalid date format ${date}")
