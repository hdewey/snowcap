FROM python:3.9-buster

WORKDIR /app

RUN apt-get update && apt-get install -y gnupg2 apt-transport-https \
    && apt-get update && apt-get install -y gcc

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install "uvicorn[standard]"
RUN pip install fastapi
RUN pip install pyjwt
RUN pip uninstall jwt
RUN pip install redis

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["uvicorn", "main:app", "--reload", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]