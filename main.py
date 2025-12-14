"""
@author wbh
"""

from collections import defaultdict
from termcolor import colored
from collector.commit import (
    count_commits,
    get_daily_commit_counts,
    get_daily_commit_hours,
)
from collector.util import get_weekday


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


def main():
    """main"""
    print_logo()

    # commmit count
    total_commit = count_commits()
    print_title("commit count:")
    print(f"  {total_commit}")
    print_blank()

    daily_commits = get_daily_commit_counts()
    count_by_weekday = defaultdict(int)
    weekdays = [
        "Sun",
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
    ]

    # commit weekday
    print_title("commit group by weekday:")
    for day in daily_commits:
        nth = get_weekday(day.date)
        count_by_weekday[nth] += day.count
    for i in range(7):
        percent = count_by_weekday[i] / total_commit * 100
        print(f"  {weekdays[i]:<3} {count_by_weekday[i]:>5} times ({percent:.2f}%)")

    print_blank()

    # commit hour
    count_by_hours = defaultdict(int)
    daily_hours = get_daily_commit_hours()
    total_hours = 0

    # commit hours
    print_title("commit group by hours:")
    for commit in daily_hours:
        for key in commit.hours:
            count_by_hours[key] += 1
            total_hours += 1
    for i in range(24):
        percent = count_by_hours[i] / total_hours * 100 if total_hours else 0
        print(f"  {i:>2} clock   {count_by_hours[i]:>4} days ({percent:.2f}%)")

    print_blank()


if __name__ == "__main__":
    main()
