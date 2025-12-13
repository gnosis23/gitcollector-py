"""
type definitions
"""

from dataclasses import dataclass


@dataclass(order=True)
class DailyCommitCount:
    """
    定义每日提交计数的结构。
    Date: YYYY-MM-DD 格式的字符串
    Count: 整数，表示提交数
    """

    date: str
    count: int


@dataclass(order=True)
class DailyCommitHours:
    """
    定义每日提交小时的结构。
    Date: YYYY-MM-DD 格式的字符串
    """

    date: str
    hours: map


@dataclass(order=True)
class ParsedTimestamp:
    """parsed timestamp in git log"""

    date_key: str
    hour: int
    minute: int
