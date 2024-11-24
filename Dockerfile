FROM python:3.11-slim
LABEL author="Raison"

WORKDIR /app

COPY . /app

VOLUME ["/path/to/host/config"]
VOLUME ["/path/to/host/log"]

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 5000

CMD ["python", "main.py"]
