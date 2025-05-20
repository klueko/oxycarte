import pandas as pd
from prophet import Prophet

def predict_pollution(df: pd.DataFrame, pollutant: str = "PM25"):
    if pollutant not in df.columns:
        raise ValueError(f"{pollutant} not found in dataframe")

    # Préparation des données pour Prophet
    df_prophet = df[["Timestamp", pollutant]].rename(columns={
        "Timestamp": "ds",
        pollutant: "y"
    })

    model = Prophet()
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=48, freq='H')  # 48h
    forecast = model.predict(future)

    # On retourne les colonnes utiles
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(48)
