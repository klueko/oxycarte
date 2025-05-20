from flask import Blueprint, request, jsonify
from db import get_connection

zones_bp = Blueprint('zones', __name__)

@zones_bp.route('/api/zones/by-city', methods=['GET'])
def get_zone_by_city():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City is required'}), 400

    query = "SELECT Id AS zone_id FROM Zones WHERE City = ?"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (city,))
    row = cursor.fetchone()

    if row:
        return jsonify({'zone_id': row.zone_id})
    else:
        return jsonify({'error': 'Zone not found'}), 404
