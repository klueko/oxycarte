from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from routes.user_routes import user_bp
    from routes.pollution_routes import pollution_bp
    from routes.prediction_routes import prediction_bp
    from routes.zone_routes import zones_bp

    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(pollution_bp, url_prefix="/api/pollution")
    app.register_blueprint(prediction_bp, url_prefix="/api/predict")
    app.register_blueprint(zones_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
