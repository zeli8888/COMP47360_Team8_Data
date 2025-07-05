FROM python:3.12-slim

WORKDIR /home/planhattan-ml

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY prediction_controller.py .
COPY busyness_model/ busyness_model/

ENV GUNICORN_WORKERS=1
CMD ["sh", "-c", "gunicorn --workers=${GUNICORN_WORKERS} --bind=0.0.0.0:5000 prediction_controller:app"]