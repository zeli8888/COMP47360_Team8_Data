import numpy as np
import joblib
import holidays

model = joblib.load("xgb_busyness_model.pkl")
label_classes = np.load("label_classes.npy", allow_pickle=True)
season_encoder = joblib.load("season_encoder.pkl")
scaler = joblib.load("scaler.pkl")

ny_holidays = holidays.US(state='NY', years=2023)

def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

def predict_busyness(location_id, time_obj):
    hour = time_obj.hour
    hour_sin = np.sin(2 * np.pi * hour / 24)
    hour_cos = np.cos(2 * np.pi * hour / 24)
    is_weekend = 1 if time_obj.weekday() >= 5 else 0
    season_str = get_season(time_obj.month)
    season_encoded = season_encoder.transform([season_str])[0]
    is_holiday = int(time_obj.date() in ny_holidays)
    features = np.array([[location_id, hour_sin, hour_cos, is_weekend, season_encoded, is_holiday]])
    features_scaled = scaler.transform(features)
    pred_idx = model.predict(features_scaled)[0]
    pred_label = label_classes[pred_idx]
    return pred_label
