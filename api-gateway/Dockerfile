FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install flask-jwt-extended

COPY . .

CMD ["python", "gateway.py"]
