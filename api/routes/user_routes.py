from flask import Blueprint, request, jsonify
from db import get_connection
from datetime import datetime

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO UserProfile (
                email, pathology,
                age, created_at, family_members
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('email'),
            data.get('pathology'),
            data.get('age'),
            data.get('created_at'),
            data.get('family_members')
        ))
        conn.commit()
        return jsonify({"message": "Utilisateur ajouté avec succès."}), 201
    except Exception as e:
        print(f"Error creating user: {str(e)}")  # Add logging
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@user_bp.route("/profile", methods=["GET"])
def get_user_profile():
    try:
        email = request.args.get("email")
        if not email:
            return jsonify({"error": "Missing email"}), 400

        conn = get_connection()
        cursor = conn.cursor()
        # Update table name to match database (UserProfile instead of Users)
        cursor.execute("SELECT pathology, zone_id FROM UserProfile WHERE email = ?", (email,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "pathology": row[0].lower(),
            "zone_id": row[1]
        })
    except Exception as e:
        print(f"Error fetching user profile: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()