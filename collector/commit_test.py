from .commit import parse_daily_commit_counts


def test_parse_daily_commit_counts():
    output = """
    WANG <test@gmail.com>|2025-12-08|2025-12-08 21:35:21 +0800
    WANG <test@gmail.com>|2025-12-08|2025-12-08 21:28:39 +0800
    WANG <test@gmail.com>|2025-12-08|2025-12-08 21:24:19 +0800
    WANG <test@gmail.com>|2025-12-08|2025-12-08 21:00:52 +0800
    """
    commit = parse_daily_commit_counts(output)
    assert len(commit) == 1
    assert commit[0].date == "2025-12-08"
    assert commit[0].count == 4
