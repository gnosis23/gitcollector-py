from collector.commit import get_daily_commit_counts


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

    commit_counts = get_daily_commit_counts()
    print("commit count:")
    print(f"  {commit_counts}")
    print_blank()


if __name__ == "__main__":
    main()
