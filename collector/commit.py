"""
some helpers in git
"""

import sh  # type: ignore
from collections import defaultdict
from datetime import datetime
import typing
from .types import DailyCommitCount, DailyCommitHours, ParsedTimestamp


def exec(command: list[str]) -> str:
    """
    运行另一个程序并返回输出
    """
    return sh.git(*command)


def count_commits() -> int:
    """
    统计 commit 数量
    """
    try:
        command = ["rev-list", "--count", "HEAD"]
        output = exec(command)

        counts = int(output)

        return counts
    except sh.ErrorReturnCode as e:
        print(f"failed to run, ${e.stderr}")
        raise e


def get_daily_commit_counts() -> list[DailyCommitCount]:
    """
    获取每日提交数量
    """
    try:
        command = [
            "--no-pager",
            "log",
            "--format=%an <%ae>|%cd|%ai",
            "--date=format:%Y-%m-%d",
        ]
        output = exec(command)

        counts = parse_daily_commit_counts(output)

        return counts
    except sh.ErrorReturnCode as e:
        print(f"failed to run, ${e.stderr}")
        raise e


def parse_daily_commit_counts(output: str) -> list[DailyCommitCount]:
    """parse count from logs"""
    lines = output.split("\n")
    daily_counts: typing.DefaultDict[str, int] = defaultdict(int)

    for line in lines:
        trimmed = line.strip()
        if not trimmed:
            continue

        parts = trimmed.split("|")
        if len(parts) < 3:
            continue

        date = parts[1]
        daily_counts[date] += 1

    counts = []
    for key, val in daily_counts.items():
        counts.append(DailyCommitCount(key, val))

    counts.sort()
    return counts


def get_daily_commit_hours() -> list[DailyCommitHours]:
    """
    获取每日提交小时数
    """
    try:
        command = [
            "--no-pager",
            "log",
            "--format=%an <%ae>|%cd|%ai",
            "--date=format:%Y-%m-%dT%H:%M:%S",
        ]
        output = exec(command)

        counts = parse_daily_commit_hours(output)

        return counts
    except sh.ErrorReturnCode as e:
        print(f"failed to run, ${e.stderr}")
        raise e


def parse_daily_commit_hours(output: str) -> list[DailyCommitHours]:
    """parse hours from logs"""
    lines = output.split("\n")
    daily_hours: dict[str, set[int]] = {}

    for line in lines:
        trimmed = line.strip()
        if not trimmed:
            continue

        parts = trimmed.split("|")
        if len(parts) < 3:
            continue

        timestamp = parts[1]

        parsed = parse_local_timestamp(timestamp)
        if not parsed:
            continue

        if parsed.date_key not in daily_hours:
            daily_hours[parsed.date_key] = set()
        daily_hours[parsed.date_key].add(parsed.hour)

    counts = []
    for key, val in daily_hours.items():
        counts.append(DailyCommitHours(key, val))

    counts.sort()

    return counts


def parse_local_timestamp(timestamp: str) -> ParsedTimestamp | None:
    """尝试解析 YYYY-MM-DD HH:MM 格式"""
    try:
        dt_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # 如果失败，尝试解析 YYYY-MM-DDTHH:MM 格式
        try:
            dt_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            # 两种格式都解析失败，返回 None
            return None

    # 成功解析，提取并返回数据
    return ParsedTimestamp(
        date_key=dt_obj.strftime("%Y-%m-%d"), hour=dt_obj.hour, minute=dt_obj.minute
    )
