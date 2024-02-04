FROM python:3.8-slim

WORKDIR /honeygain-scrapper

RUN apt-get update && apt-get install -y gcc make

COPY main.py .
COPY updater.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py"]