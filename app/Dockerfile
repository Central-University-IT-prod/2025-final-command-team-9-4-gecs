FROM python:3.13-alpine3.21

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD uvicorn src.main:app --port ${PORT} --host=${HOST}