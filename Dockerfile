FROM python:3.10-alpine3.16

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# CMD ["python", "app.py"]
CMD ["gunicorn", "-b", "0.0.0.0", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "app:app"]