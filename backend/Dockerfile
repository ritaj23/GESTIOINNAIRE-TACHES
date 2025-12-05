FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
client = MongoClient("mongodb://mongo:27017/")  # mongo هو اسم الخدمة في docker-compose
db = client["gestionnaire"]
