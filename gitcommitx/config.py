import os
from dotenv import load_dotenv
from pathlib import Path

# 取得專案根目錄
BASE_DIR = Path(__file__).resolve().parent.parent

# 載入 .env.dev 檔案
env_path = BASE_DIR / ".env.dev"
if env_path.exists():
    load_dotenv(env_path)
else:
    raise FileNotFoundError(f"❌ 找不到環境變數檔案：{env_path}")

# 取得 OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 驗證是否成功載入
if OPENAI_API_KEY:
    print(f"✅ 成功載入 OPENAI_API_KEY")
else:
    raise ValueError("❌ OPENAI_API_KEY 環境變數未設置！請檢查 .env.dev 檔案。")
