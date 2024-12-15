FROM python:3.9
WORKDIR /app
COPY . /app
ADD main.py .
RUN pip install yandex-cloud-ml-sdk chromadb pypdf pyTelegramBotAPI pandas
CMD ["python", "./main.py"]