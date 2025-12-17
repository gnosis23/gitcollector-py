"""
@author wbh
"""

import os
import sys
import typing
from rich.console import Console
from rich.table import Table
import typer
from collections import defaultdict
from termcolor import colored
from collector import (
    count_commits,
    get_daily_commit_counts,
    get_daily_commit_hours,
    get_weekday,
)


def check_git():
    """check .git exist"""
    if os.path.exists(".git") and os.path.isdir(".git"):
        return
    print("not a git repository")
    sys.exit(-1)


def print_logo():
    """print logo"""
    print("")
    print("------------------------------------------------------")
    print("                   Git Collector ")
    print("------------------------------------------------------")
    print("")


def print_blank():
    """print blank line"""
    print("")


def print_title(title: str):
    """print title"""
    print(colored(title, "cyan"))


def main(locale: str = "en"):
    """
    Show statistics based on git.

    If --locale is used, show some text in specified language.
    """
    console = Console()

    print_logo()

    check_git()

    # commmit count
    total_commit = count_commits()
    print_title("commit count:")
    print(f"  {total_commit}")
    print_blank()

    # commit weekday
    daily_commits = get_daily_commit_counts()
    count_by_weekday: typing.DefaultDict[int, int] = defaultdict(int)
    weekdays = [
        "Sun",
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
    ]
    if locale == "zh":
        weekdays = [
            "星期日",
            "星期一",
            "星期二",
            "星期三",
            "星期四",
            "星期五",
            "星期六",
        ]

    print_title("commit group by weekday:")
    for day in daily_commits:
        nth = get_weekday(day.date)
        count_by_weekday[nth] += day.count

    table = Table(show_header=True, header_style="bold magenta", box=None)
    table.add_column("Weekday")
    table.add_column("Count", justify="right")
    table.add_column("Percent", justify="right")

    for i in range(7):
        percent = count_by_weekday[i] / total_commit * 100
        table.add_row(str(weekdays[i]), str(count_by_weekday[i]), f"{percent:.2f}%")

    console.print(table)

    print_blank()

    # commit hour
    count_by_hours: typing.DefaultDict[int, int] = defaultdict(int)
    daily_hours = get_daily_commit_hours()
    total_hours = 0

    print_title("commit group by hours:")
    for commit in daily_hours:
        for key in commit.hours:
            count_by_hours[key] += 1
            total_hours += 1

    table = Table(show_header=True, header_style="bold magenta", box=None)
    table.add_column("Clock", justify="right", width=7)
    table.add_column("Days", justify="right", width=5)
    table.add_column("Percent", justify="right")

    for i in range(24):
        percent = count_by_hours[i] / total_hours * 100 if total_hours else 0
        table.add_row(f"{i:>2}", str(count_by_hours[i]), f"{percent:.2f}%")

    console.print(table)

    print_blank()


if __name__ == "__main__":
    typer.run(main)
