FROM python:3.11-alpine
WORKDIR /tasker_message_brokers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -v --no-cache-dir
COPY . .
ENV RABBITMQ_HOST=rabbitmq
CMD ["python", "src/message_brokers.py"]
