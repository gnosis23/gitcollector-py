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
