# バックエンド FastAPI 用（backend/ をビルドコンテキストにすること）
FROM python:3.12-slim

WORKDIR /app

# 依存インストール（passlib[argon2] は requirements.txt に含まれており security.py で使用）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコード
COPY . .

# コンテナ内では db:5432 で名前解決される
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
