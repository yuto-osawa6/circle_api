FROM python:3.9-buster
WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
# RUN pip3 install fastapi uvicorn

# pipを使ってpoetryをインストール
RUN pip install poetry

# poetryの定義ファイルをコピー (存在する場合)
COPY pyproject.toml* poetry.lock* ./

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install; fi

# Redisをインストール
RUN apt-get update && \
    apt-get install -y redis-server && \
    rm -rf /var/lib/apt/lists/*


COPY ./app /app
# CMD ["poetry", "run","uvicorn","--reload","app.main:app","--host","0.0.0.0","--port","8000"]
CMD ["poetry", "run", "uvicorn", "--reload", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "debug", "--access-log"]
