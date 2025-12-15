FROM python:3.12-slim

RUN pip install flask

WORKDIR /app

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

