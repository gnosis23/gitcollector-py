from collector.commit import count_commits, get_daily_commit_counts


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

    commit_counts = count_commits()
    print("commit count:")
    print(f"  {commit_counts}")
    print_blank()

    daily_commits = get_daily_commit_counts()
    print("commit group by weekday:")
    for day in daily_commits:
        print(f"  {day.date} {day.count}")
    print_blank()


if __name__ == "__main__":
    main()
