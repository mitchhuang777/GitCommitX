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
    
    typer.echo("✨ AI 正在生成 Commit Message...")
    commit_message = generate_commit_message(diff)
    
    typer.echo(f"✅ 生成的 Commit Message: \n{commit_message}\n")
    
    confirm = typer.confirm("是否提交？")
    if confirm:
        subprocess.run(["git", "commit", "-m", commit_message])
        typer.echo("🎉 Commit 成功！")
    else:
        typer.echo("❌ 取消提交！")

if __name__ == "__main__":
    app()
