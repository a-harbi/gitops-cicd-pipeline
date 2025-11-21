FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install flask

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
