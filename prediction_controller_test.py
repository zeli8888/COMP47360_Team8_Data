import pytest
from datetime import datetime, timedelta

@pytest.fixture
def client():
    from prediction_controller import app
    return app.test_client()

def test_predict_multi_zones_success(client):
    data = {
        "zoneIds": [1, 2, 3],
        "dateTime": "2025-03-15T09:00:00.123456Z"
    }
    response = client.post('/api/predict_multi_zones', json=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data['busyness'], list)
    assert len(json_data['busyness']) == 3

def test_predict_multi_zones_invalid_datetime(client):
    data = {
        "zoneIds": [1],
        "dateTime": "invalid_time_string"
    }
    response = client.post('/api/predict_multi_zones', json=data)
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_predict_multi_zones_missing_field(client):
    data = {"zoneIds": [1]}  # lack dateTime
    response = client.post('/api/predict_multi_zones', json=data)
    assert response.status_code == 400

def test_predict_single_zone_success(client):
    data = {
        "zoneId": 5,
        "zonedDateTimeList": [
            "2025-03-15T09:00:00.123456Z",
            "2025-03-15T10:00:00.123456Z",
            "2025-03-15T11:00:00.123456Z"
        ]
    }
    response = client.post('/api/predict_single_zone', json=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data['busyness'], list)
    assert len(json_data['busyness']) == 3

def test_predict_single_zone_invalid_time(client):
    data = {
        "zoneId": 5,
        "zonedDateTimeList": ["invalid_time_string"]
    }
    response = client.post('/api/predict_single_zone', json=data)
    assert response.status_code == 400

def test_predict_single_zone_missing_field(client):
    data = {"zonedDateTimeList": ["2024-03-15T12:00:00-05:00"]}  # lack zoneId
    response = client.post('/api/predict_single_zone', json=data)
    assert response.status_code == 400
