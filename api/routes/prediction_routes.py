from flask import Blueprint, request, jsonify
from db import get_connection
import pandas as pd
from predict.prophet_model import predict_pollution

prediction_bp = Blueprint('predict', __name__)

@prediction_bp.route("/zone", methods=["GET"])
def predict_for_zone():
    zone_id = request.args.get("zone_id", type=int)
    pollutant = request.args.get("pollutant", "PM25")

    conn = get_connection()
    query = f"""
        SELECT TOP 300 Timestamp, {pollutant}
        FROM PollutionData
        WHERE ZoneId = ?
        ORDER BY Timestamp DESC
    """
    df = pd.read_sql(query, conn, params=(zone_id,))
    conn.close()

    if df.empty:
        return jsonify([])

    forecast = predict_pollution(df, pollutant)
    return jsonify(forecast.to_dict(orient="records"))

@prediction_bp.route("/personalized", methods=["GET"])
def predict_personalized():
    zone_name = request.args.get("city")
    pathology = request.args.get("pathology", "asthme").lower()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT Id FROM Zones WHERE City = ?", zone_name)
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Zone not found"}), 404
    zone_id = row[0]

    # Choisir le polluant selon la pathologie
    polluant_mapping = {
        "asthme": "PM25",
        "bpco": "PM10",
        "bronchite chronique": "NO2"
    }
    pathology_cleaned = pathology.strip().lower()
    pollutant = polluant_mapping.get(pathology_cleaned, "PM25")

    # Charger les données SQL Server
    query = f"""
        SELECT TOP 200 Timestamp, {pollutant}
        FROM PollutionData
        WHERE ZoneId = ?
        ORDER BY Timestamp DESC
    """
    df = pd.read_sql(query, conn, params=(zone_id,))
    conn.close()

    if df.empty:
        return jsonify([])

    # Prédiction Prophet
    forecast = predict_pollution(df, pollutant)
    forecast = forecast.tail(24)  # 24h seulement
    return jsonify(forecast.to_dict(orient="records"))


