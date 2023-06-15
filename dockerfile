FROM python:3.8-slim

COPY ["main.py", "flask_test.py", "config.ini", "requirements.txt", "Conversation.py", "/TelegramBot/"]
WORKDIR /TelegramBot

RUN apt update &&\
    pip install -r requirements.txt

# EXPOSE 5000
CMD ["python3", "main.py"]

