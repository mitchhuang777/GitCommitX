import os
from openai import OpenAI
from gitcommitx.config import OPENAI_API_KEY  # 確保從 config.py 取得 API Key

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_commit_message(diff_text):
    prompt = f"""
    你是一個專業的 Git commit 訊息生成器。請根據以下程式碼變更內容，生成符合 Conventional Commit 格式的訊息：
    {diff_text}
    只返回 commit 訊息，不需要額外解釋。
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
