from collections import defaultdict
import subprocess
from .types import DailyCommitCount


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
