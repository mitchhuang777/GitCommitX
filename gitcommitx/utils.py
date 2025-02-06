import subprocess

def get_git_diff():
    """取得 staged 變更內容"""
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True,
        encoding="utf-8",  # 明確指定 UTF-8 避免 Windows 預設 CP950 問題
    )
    return result.stdout.strip() if result.stdout else ""
