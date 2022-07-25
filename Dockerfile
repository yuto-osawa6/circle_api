FROM python:3.7
# WORKDIR /app
RUN pip3 install fastapi uvicorn
# pipを使ってpoetryをインストール
RUN pip install poetry

# poetryの定義ファイルをコピー (存在する場合)
COPY pyproject.toml* poetry.lock* ./

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install; fi


COPY ./app /app
CMD ["uvicorn","--reload","app.main:app","--host","0.0.0.0","--port","8080"]