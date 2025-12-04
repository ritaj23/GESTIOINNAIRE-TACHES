# 1️⃣ نحددو image أساسية
FROM python:3.10

# 2️⃣ نحددو working directory داخل container
WORKDIR /app

# 3️⃣ ننسخو ملف requirements.txt داخل container
COPY requirements.txt .

# 4️⃣ نثبتو المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ ننسخو كل الملفات تاع المشروع
COPY . .

# 6️⃣ نحددوا البورت
EXPOSE 8000

# 7️⃣ نحددوا command باش يشغل Flask
CMD ["python", "app.py"]
