from flask import Flask
from extensions import db, init_app
from routes import api as api_blueprint

from config import DevelopmentConfig, TestConfig

def create_app(config_object=DevelopmentConfig):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_object)
    init_app(app)  # Initialize database and other extensions
    app.register_blueprint(api_blueprint, url_prefix='/api')
    return app


if __name__ == '__main__':
    app = create_app('config.DevelopmentConfig')  # Adjust the configuration as needed
    app.run(debug=True, port=8000)
