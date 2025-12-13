from collections import defaultdict
from datetime import datetime
import subprocess
from .types import DailyCommitCount, DailyCommitHours, ParsedTimestamp


def count_commits() -> int:
    """
    统计 commit 数量
    """
    try:
        command = ["git", "rev-list", "--count", "HEAD"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        output = result.stdout.strip()
        counts = int(output)

        return counts
    except subprocess.CalledProcessError as e:
        print(f"failed to run, ${e.stderr}")
        raise "get_daily_commit_counts failed"


def get_daily_commit_counts() -> list[DailyCommitCount]:
    """
    获取每日提交数量
    """
    try:
        command = ["git", "log", "--format=%an <%ae>|%cd|%ai", "--date=format:%Y-%m-%d"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        output = result.stdout.strip()
        counts = parse_daily_commit_counts(output)

        return counts
    except subprocess.CalledProcessError as e:
        print(f"failed to run, ${e.stderr}")
        raise "get_daily_commit_counts failed"


def parse_daily_commit_counts(output: str) -> list[DailyCommitCount]:
    lines = output.split("\n")
    daily_counts = defaultdict(int)

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
            "git",
            "log",
            "--format=%an <%ae>|%cd|%ai",
            "--date=format:%Y-%m-%dT%H:%M:%S",
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        output = result.stdout.strip()
        counts = parse_daily_commit_hours(output)

        return counts
    except subprocess.CalledProcessError as e:
        print(f"failed to run, ${e.stderr}")
        raise "get_daily_commit_hours failed"


def parse_daily_commit_hours(output: str) -> list[DailyCommitHours]:
    lines = output.split("\n")
    daily_hours = {}

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

        if parsed.dateKey not in daily_hours:
            daily_hours[parsed.dateKey] = {}
        daily_hours[parsed.dateKey][parsed.hour] = True

    counts = []
    for key, val in daily_hours.items():
        counts.append(DailyCommitHours(key, val))

    counts.sort()

    return counts


def parse_local_timestamp(timestamp: str) -> ParsedTimestamp:
    # 尝试解析 YYYY-MM-DD HH:MM 格式
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
        dateKey=dt_obj.strftime("%Y-%m-%d"), hour=dt_obj.hour, minute=dt_obj.minute
    )
