import subprocess


def get_daily_commit_counts() -> int:
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
