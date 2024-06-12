# FROM python:3.9

# WORKDIR /app

# COPY ./requirements.txt .

# RUN pip3 install --no-cache-dir -r ./requirements.txt

# COPY ./run.py .

# CMD [ "python", "run.py"]


# Sử dụng một image Python làm base
FROM python:3.9

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép requirements.txt vào thư mục làm việc
COPY requirements.txt .

# Cài đặt các thư viện Python cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ nội dung của thư mục hiện tại vào thư mục làm việc
COPY . .

# Expose cổng mà ứng dụng Flask của bạn sẽ chạy
EXPOSE 5001

# Đặt biến môi trường cần thiết
ENV DATABASE_PORT='mongodb+srv://root:hello123@vdt.2w2zlck.mongodb.net/?retryWrites=true&w=majority&appName=vdt'
ENV JWT_SECRET='VDT2024'

# Chạy lệnh để khởi động ứng dụng Flask
CMD ["python", "run.py"]
