FROM python:3.8-slim-buster

WORKDIR /app
COPY . /app

RUN sudo apt update && sudo apt install awscli -y

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]