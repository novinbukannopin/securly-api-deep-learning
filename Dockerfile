FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

# Buat direktori kerja
WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["python", "main.py"]
