from flask import Blueprint, request, jsonify
from db import get_connection

pollution_bp = Blueprint("pollution", __name__)

@pollution_bp.route("/latest", methods=["GET"])
def get_latest_pollution():
    zone_id = request.args.get("zone_id", None)
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT TOP 24
            pd.Timestamp, pd.PM25, pd.PM10, pd.NO2, pd.O3, pd.CO, pd.PollenLevel, pd.AQI,
            z.City, z.District
        FROM PollutionData pd
        JOIN Zones z ON pd.ZoneId = z.Id
        WHERE (@zone_id IS NULL OR pd.ZoneId = ?)
        ORDER BY pd.Timestamp DESC
    """

    params = (zone_id,) if zone_id else (None,)
    cursor.execute(query, params)

    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()
    return jsonify(results)

@pollution_bp.route("/avg-by-city", methods=["GET"])
def get_avg_pollution_by_city():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
        z.City,
        AVG(pd.PM25) AS Avg_PM25,
        AVG(pd.PM10) AS Avg_PM10,
        AVG(pd.NO2) AS Avg_NO2,
        AVG(pd.O3) AS Avg_O3,
        AVG(pd.CO) AS Avg_CO,
        AVG(pd.AQI) AS Avg_AQI,
        MAX(pd.Timestamp) AS LastUpdate,
        AVG(z.Latitude) AS Latitude,
        AVG(z.Longitude) AS Longitude
    FROM PollutionData pd
    JOIN Zones z ON pd.ZoneId = z.Id
    WHERE pd.Timestamp >= DATEADD(HOUR, -24, SYSDATETIME())
    GROUP BY z.City
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()
    return jsonify(results)
