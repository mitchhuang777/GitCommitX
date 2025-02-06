import os
import subprocess

def setup_git_hook():
    """設置 Git Hook 來自動填寫 Commit Message"""
    hook_path = ".git/hooks/prepare-commit-msg"
    script = "python -m commitx.cli commit"
    with open(hook_path, "w") as hook_file:
        hook_file.write(script)
    os.chmod(hook_path, 0o755)
    print("✅ Git Hook 安裝成功！")