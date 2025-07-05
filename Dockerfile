FROM python:3.12-slim

WORKDIR /home/planhattan-ml

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY prediction_controller.py .
COPY busyness_model/ busyness_model/

CMD ["gunicorn", "--preload", "--workers=3", "--bind=0.0.0.0:5000", "prediction_controller:app"]
