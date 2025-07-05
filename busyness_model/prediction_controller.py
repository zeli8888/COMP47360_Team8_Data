import numpy as np
import joblib
import pytz
import datetime
import holidays
from flask import Flask
from flask import request
def main(model, scaler, season_encoder, label_classes):
    ny_tz = pytz.timezone('America/New_York')
    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"

    app = Flask(__name__)
    
    @app.route('/api/predict_multi_zones', methods=['POST'])
    def predict_multi_zones():
        """
        predict busyness for multiple zones at a given time.

        Returns:
            jsonify: A json object containing the predicted busyness for each zone at the given time (200 OK).
        """
        try:
            zones_time = request.get_json()
            zones = zones_time['zoneIds']
            time = datetime.datetime.fromisoformat(zones_time['dateTime'])
            time = time.astimezone(ny_tz)
        except Exception as e:
            return {'error': str(e)}, 400
        
        zones = np.array(zones)
        hour_sin = np.sin(2 * np.pi * time.hour / 24) * np.ones(len(zones))
        hour_cos = np.cos(2 * np.pi * time.hour / 24) * np.ones(len(zones))
        is_weekend = np.array([1 if time.weekday() >= 5 else 0] * len(zones))
        is_holiday = np.array([int(time.date() in holidays.US(state='NY', years=time.year))] * len(zones))
        season_str = get_season(time.month)
        season_encoded = season_encoder.transform([season_str]) * np.ones(len(zones))
        features = np.hstack((zones.reshape(-1, 1), hour_sin.reshape(-1, 1), hour_cos.reshape(-1, 1), is_weekend.reshape(-1, 1), season_encoded.reshape(-1, 1), is_holiday.reshape(-1, 1)))
        features = scaler.transform(features)
        busyness = model.predict(features)
        busyness = label_classes.inverse_transform(busyness)
        return {'busyness': busyness}, 200
    
    @app.route('/api/predict_single_zone', methods=['POST'])
    def predict_single_zone():
        '''
        predict busyness for a single zone at a list of given times.

        Returns:
            jsonify: A json object containing the predicted busyness for the given zone at each time (200 OK).
        '''
        try:
            zone_times = request.get_json()
            zone = zone_times['zoneId']
            times = zone_times['zonedDateTimeList']
        except Exception as e:
            return {'error': str(e)}, 400
        
        zones = zone * np.ones(len(times))
        hour_sin = np.sin(2 * np.pi * np.array([time_obj.hour for time_obj in times]) / 24)
        hour_cos = np.cos(2 * np.pi * np.array([time_obj.hour for time_obj in times]) / 24)
        is_weekend = np.array([1 if time_obj.weekday() >= 5 else 0 for time_obj in times])
        is_holiday = np.array([int(time_obj.date() in holidays.US(state='NY', years=time_obj.year)) for time_obj in times])
        season_str = np.array([get_season(time_obj.month) for time_obj in times])
        season_encoded = season_encoder.transform(season_str)
        features = np.hstack((zones.reshape(-1, 1), hour_sin.reshape(-1, 1), hour_cos.reshape(-1, 1), is_weekend.reshape(-1, 1), season_encoded.reshape(-1, 1), is_holiday.reshape(-1, 1)))
        features = scaler.transform(features)
        busyness = model.predict(features)
        busyness = label_classes.inverse_transform(busyness)
        return {'busyness': busyness}, 200
    
    return app

if __name__ == "__main__":
    model = joblib.load("xgb_busyness_model.pkl")
    label_classes = np.load("label_classes.npy", allow_pickle=True)
    season_encoder = joblib.load("season_encoder.pkl")
    scaler = joblib.load("scaler.pkl")
    app = main(model, scaler, season_encoder, label_classes)
    app.run(host='0.0.0.0', port=5000, debug=False)