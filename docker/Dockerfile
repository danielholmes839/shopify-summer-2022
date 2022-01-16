FROM python:3.8-slim-buster

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py main.py
COPY schema.graphql schema.graphql
COPY app app

ENV CONTEXT=LOCAL

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]