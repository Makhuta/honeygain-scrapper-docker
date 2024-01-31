FROM python:3.8-slim

WORKDIR /honeygain-scrapper

RUN apt-get update && apt-get install -y gcc make

COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]