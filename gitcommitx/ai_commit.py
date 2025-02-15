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
        你是一個專業的 Git Commit Message 生成器，請根據以下變更內容，自行選擇最適合的 `type`，並生成符合 Conventional Commit 規範的提交訊息。

        **變更內容：**

        ```
        {diff_text}
        ```

        **請用英文直接輸出 Commit Message，不要用反引號 (`) 或三個反引號 (```) 包住，格式如下：**
        **不要產生與變更無關的說明**，**只輸出 commit message**。
        **字數限制 80 字元以內**。

        ```
        <type>(scope): <description>
        ```

        ## **🔹 Commit Message 類型規則**
        - `feat`：如果**新增了功能**，請使用 `feat`。
        - `fix`：如果**修復了 bug**，請使用 `fix`。
        - `refactor`：如果**重構程式碼但沒有新增功能**，請使用 `refactor`。
        - `docs`：如果變更的是 **`.md` 文件或純註解**，請使用 `docs`。
        - `style`：如果只是**格式調整（如 PEP8 修正、空格、換行）**，請使用 `style`。
        - `test`：如果變更的是**測試檔案**，請使用 `test`。
        - `chore`：如果變更的是 **建置工具、Git Hook、腳本或設定檔**，請使用 `chore`。
        - `build`：如果變更影響 **環境、Docker、npm、依賴管理**，請使用 `build`。
        - `ci`：如果變更影響 **CI/CD 配置**，請使用 `ci`。
        - `perf`：如果變更**提升效能**，請使用 `perf`。
        - `revert`：如果**還原某次 commit**，請使用 `revert`。

        ## **🔹 Scope 規則**
        - **Scope 必須根據變更的「檔案名稱」，而非所在資料夾，例如：**
        - `gitcommitx/hooks.py` → `type(hooks): <description>`
        - `gitcommitx/config.js` → `type(config): <description>`
        - `database/models.ts` → `type(models): <description>`
        - `router/user.go` → `type(user): <description>`

        - **專案根目錄的設定檔，請使用檔案名稱作為 Scope**
        - `.env` → `chore(env): update environment variables`
        - `.gitignore` → `chore(gitignore): update ignored files`
        - `package.json` → `chore(package): update dependencies`
        - `pyproject.toml` → `chore(pyproject): modify poetry dependencies`

        - **確保輸出的 commit message 直接符合 Conventional Commit 規範！**

        **舉例**
        - `fix(auth): 修正 JWT 驗證邏輯，避免 Token 過期後仍然能存取`
        - `feat(api): 支援批量查詢使用者，減少 API 延遲`
        - `refactor(database): 優化索引查詢，提升 20% 效能`
        - `docs(readme): 更新 README 文件，補充安裝說明`
        - `chore(hooks): 移除 Git Hook 設定功能`
        - `style(linter): 修正 PEP8 格式`

        """

    # `commit_type = "auto"`，AI 需要根據 `diff_text` 自動判斷 `type`
    else:
        prompt = f"""
        你是一個專業的 Git Commit Message 生成器，請根據以下變更內容，自行選擇最適合的 `type`，並生成符合 Conventional Commit 規範的提交訊息。

        **變更內容**：
        ```
        {diff_text}
        ```

        **請用英文直接輸出 Commit Message，不要用反引號 (`) 或三個反引號 (```) 包住，格式如下：**
        **不要產生與變更無關的說明**，**只輸出 commit message**。
        **字數限制 80 字元以內**。

        ```
        {commit_type}(scope): <description>
        ```

        ## **🔹 Scope 規則**
        - **Scope 必須根據變更的「檔案名稱」，而非所在資料夾，例如：**
        - `gitcommitx/hooks.py` → `type(hooks): <description>`
        - `gitcommitx/config.js` → `type(config): <description>`
        - `database/models.ts` → `type(models): <description>`
        - `router/user.go` → `type(user): <description>`

        - **專案根目錄的設定檔，請使用檔案名稱作為 Scope**
        - `.env` → `chore(env): update environment variables`
        - `.gitignore` → `chore(gitignore): update ignored files`
        - `package.json` → `chore(package): update dependencies`
        - `pyproject.toml` → `chore(pyproject): modify poetry dependencies`

        - **確保輸出的 commit message 直接符合 Conventional Commit 規範！**

        **舉例**
        - `fix(auth): 修正 JWT 驗證邏輯，避免 Token 過期後仍然能存取`
        - `feat(api): 支援批量查詢使用者，減少 API 延遲`
        - `refactor(database): 優化索引查詢，提升 20% 效能`
        - `docs(readme): 更新 README 文件，補充安裝說明`
        - `chore(hooks): 移除 Git Hook 設定功能`
        - `style(linter): 修正 PEP8 格式`

        """
        
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )

    # 取得 AI 生成的 commit message
    commit_message = response.choices[0].message.content.strip()

    # 強制移除可能的 Markdown 反引號 (` 或 ```)
    while commit_message.startswith("`") and commit_message.endswith("`"):
        commit_message = commit_message[1:-1].strip()

    return commit_message