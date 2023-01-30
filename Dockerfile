FROM python:3.11.1-alpine

ENV PYTHONUNBUFFERED True

COPY requirements.txt .
RUN apk add --no-cache --virtual build-dependencies libpq-dev build-base \
    && pip install -r requirements.txt \
    && apk del --no-cache build-dependencies

COPY app /app

WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
EXPOSE 8080