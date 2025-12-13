from collections import defaultdict
from collector.commit import count_commits, get_daily_commit_counts
from collector.util import get_weekday


def print_logo():
    print("")
    print("------------------------------------------------------")
    print("                   Git Collector ")
    print("------------------------------------------------------")
    print("")


def print_blank():
    print("")


def main():
    print_logo()

    total_commit = count_commits()
    print("commit count:")
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

    print("commit group by weekday:")
    for day in daily_commits:
        nth = get_weekday(day.date)
        count_by_weekday[nth] += day.count
    for i in range(7):
        percent = count_by_weekday[i] / total_commit * 100
        print(f"  {weekdays[i]:<3} {count_by_weekday[i]:>4} times ({percent:.2f}%)")

    print_blank()


if __name__ == "__main__":
    main()
