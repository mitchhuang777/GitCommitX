import typer
import subprocess
from gitcommitx.utils import get_git_diff
from gitcommitx.ai_commit import generate_commit_message

app = typer.Typer(help="GitCommitX CLI")  # 設定頂層說明

@app.callback()
def main():
    """
    GitCommitX CLI 工具
    """
    # 這裡可以做一些全局初始化動作
    pass

@app.command()
def commit():
    """AI 生成 Commit Message 並提交"""
    diff = get_git_diff()
    if not diff:
        typer.echo("❌ 沒有變更內容，請先使用 `git add` 添加檔案！")
        raise typer.Exit()
    
    # 讓使用者選擇 commit type，使用 `typer.Choice()`
    commit_type = typer.prompt(
        "請選擇 Commit 類型",
        default="auto"
    )

    valid_types = [
        "auto", "feat", "fix", "docs", "style", "refactor",
        "test", "chore", "build", "ci", "perf", "revert"
    ]

    while commit_type not in valid_types:
        typer.echo("❌ 無效的類型，請選擇有效的 Commit 類型。")
        commit_type = typer.prompt("請選擇 Commit 類型", default="auto")
    
    typer.echo("✨ AI 正在生成 Commit Message...")
    commit_message = generate_commit_message(commit_type, diff)
    
    typer.echo(f"✅ 生成的 Commit Message: \n{commit_message}\n")
    
    confirm = typer.confirm("是否提交？")
    if confirm:
        subprocess.run(["git", "commit", "-m", commit_message])
        typer.echo("🎉 Commit 成功！")
    else:
        typer.echo("❌ 取消提交！")

if __name__ == "__main__":
    app()
