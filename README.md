# COMP47360_Team8_Data
# 🧠 NYC Busyness Prediction Model

This repository contains the trained XGBoost classification model and associated preprocessing tools for predicting **busyness levels** across NYC taxi zones. The model is trained on 2023 yellow taxi drop-off data, and exposed via a Flask-based REST API for use in downstream applications.

---

## 📦 Contents

- `xgb_busyness_model.pkl` — Trained XGBoost model
- `scaler.pkl` — `MinMaxScaler` used for normalization
- `season_encoder.pkl` — `LabelEncoder` for season values
- `label_classes.npy` — Numpy array of class labels (`["high", "low", "medium"]`)
- `app.py` — Flask API for making predictions
- `predict_demo.py` — Example script to call the prediction API

---

## 🚀 How It Works

### 🧩 Input Features

The model expects the following inputs per record:

| Feature          | Description                          |
|------------------|--------------------------------------|
| `LocationID`     | NYC taxi zone integer ID             |
| `hour`           | Hour of the day (0–23), cyclical encoded as `sin` and `cos` |
| `is_weekend`     | Boolean: 1 if Saturday/Sunday        |
| `season`         | Categorical: Spring, Summer, Autumn, Winter |
| `is_holiday`     | Boolean: 1 if US/NY public holiday   |

All features are **preprocessed** (encoded & normalized) consistently between training and inference.

---

## 📈 Model Performance

| Metric        | Train Set | Test Set |
|---------------|-----------|----------|
| Accuracy      | 0.87      | 0.86     |
| Macro F1      | 0.87      | 0.86     |
| Weighted F1   | 0.87      | 0.86     |

Model: **XGBoostClassifier**  
Key hyperparameters:
```python
XGBClassifier(
  n_estimators=200,
  max_depth=7,
  learning_rate=0.1,
  subsample=0.8,
  colsample_bytree=0.8,
  reg_alpha=0.1,
  reg_lambda=1
)
