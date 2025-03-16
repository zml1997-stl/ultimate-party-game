from flask import Flask
from flask_socketio import SocketIO
import os

# Initialize Flask-SocketIO with async mode set to threading for Heroku compatibility
socketio = SocketIO(async_mode='threading')

def create_app():
    """
    Factory function to create and configure the Flask application.
    Returns the Flask app instance.
    """
    # Create Flask app instance with custom template folder
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_folder = os.path.join(base_dir, 'templates')
    app = Flask(__name__, template_folder=template_folder)
    print(f"Template folder: {os.path.abspath(app.template_folder)}")

    # Load configuration from config.py
    config_path = os.path.join(base_dir, 'config.py')
    app.config.from_pyfile(config_path, silent=True)

    # Ensure the instance folder exists (for potential future use)
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Secret key for session management (loaded from config.py or set as fallback)
    app.secret_key = app.config.get('SECRET_KEY', 'dev-secret-key-for-testing')

    # Initialize Flask-SocketIO with the app
    socketio.init_app(app, cors_allowed_origins="*")  # Allow cross-origin for testing

    # Register blueprints and sockets
    from . import routes, sockets
    app.register_blueprint(routes.bp)
    sockets.init_socketio(socketio)  # Custom function to initialize socket events

    return app

if __name__ == '__main__':
    # Run the app with SocketIO for local testing (not used in Heroku)
    socketio.run(app=create_app(), host='0.0.0.0', port=5000, debug=True)