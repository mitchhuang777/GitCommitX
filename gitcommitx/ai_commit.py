import os
from openai import OpenAI
from gitcommitx.config import OPENAI_API_KEY  # 確保從 config.py 取得 API Key

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_commit_message(commit_type="auto", diff_text=None):
    """
    生成符合 Conventional Commit 規範的 Commit Message。
    
    - `commit_type`:
        - 如果提供明確的 `type`（如 `feat`, `fix`），AI 只需生成 `description`
        - 如果 `commit_type="auto"`，AI 會根據 `diff_text` 自動判斷最適合的 `type`
    """

    if not diff_text or diff_text.strip() == "":
        print("⚠️ DEBUG: `diff_text` is empty! AI cannot generate commit message.")
        return "Error: No changes detected. Please stage your changes using `git add`."


    # 使用者指定 `commit_type`，AI 只需產生 `description`
    if commit_type == "auto":
        prompt = f"""
        你是一個專業的 Git Commit Message 生成器，請根據以下變更內容，自行選擇最適合的 `type` 並生成符合 Conventional Commit 規範的提交訊息。

        **變更內容**：
        ```
        {diff_text}
        ```

        **請產生 Commit Message，格式如下**
        ```
        <type>(scope): <description>
        ```

        **Commit Message 必須符合以下 `type` 類型**
        - `feat`：新增功能
        - `fix`：修復錯誤
        - `docs`：文件變更
        - `style`：程式碼格式變更（不影響功能）
        - `refactor`：程式碼重構（無新功能，無 Bug 修復）
        - `test`：測試新增或修改
        - `chore`：建置工具或輔助工具的變更
        - `build`：影響建置系統或依賴管理（如 npm, Docker, Makefile）
        - `ci`：修改 CI/CD 配置
        - `perf`：提升效能的變更
        - `revert`：還原先前的提交

        **描述（description）**

        - 以 **現在式動詞撰寫**，例如：「修正 API 回應錯誤」、「優化快取機制」、「新增授權驗證」。
        - **描述應該包含修正的問題與解法，而不只是 "correct bug" 這種模糊詞**。
        - **不要產生與變更無關的說明**，**只輸出 commit message**。
        - **舉例**
        - `fix(auth): 修正 JWT 驗證邏輯，避免 Token 過期後仍然能存取`
        - `feat(api): 支援批量查詢使用者，減少 API 延遲`
        - `refactor(database): 優化索引查詢，提升 20% 效能`

        """

    # `commit_type = "auto"`，AI 需要根據 `diff_text` 自動判斷 `type`
    else:
        prompt = f"""
        你是一個專業的 Git Commit Message 生成器，請根據以下變更內容，生成符合 Conventional Commit 規範的提交訊息。

        **變更內容**：
        ```
        {diff_text}
        ```

        **請直接輸出 Commit Message，格式如下**：
        ```
        {commit_type}(scope): <description>
        ```

        **描述（description）**

        - 以 **現在式動詞撰寫**，例如：「修正 API 回應錯誤」、「優化快取機制」、「新增授權驗證」。
        - **描述應該包含修正的問題與解法，而不只是 "correct bug" 這種模糊詞**。
        - **不要產生與變更無關的說明**，**只輸出 commit message**。
        - **舉例**
        - `fix(auth): 修正 JWT 驗證邏輯，避免 Token 過期後仍然能存取`
        - `feat(api): 支援批量查詢使用者，減少 API 延遲`
        - `refactor(database): 優化索引查詢，提升 20% 效能`

        """
        
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )

    # 取得 AI 回應內容，確保去除不必要的符號
    commit_message = response.choices[0].message.content.strip()

    # 處理可能的 Markdown 格式，移除首尾的 ` 或 ``` 
    while commit_message.startswith("`") and commit_message.endswith("`"):
        commit_message = commit_message[1:-1].strip()

    return response.choices[0].message.content.strip()