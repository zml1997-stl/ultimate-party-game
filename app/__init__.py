from flask import Flask
from flask_socketio import SocketIO
import os

print("Starting app/__init__.py")

socketio = SocketIO(async_mode='threading')
print("SocketIO initialized")

def create_app():
    print("Entering create_app")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print(f"Base dir: {base_dir}")
    template_folder = os.path.join(base_dir, 'templates')
    app = Flask(__name__, template_folder=template_folder)
    print(f"Template folder: {os.path.abspath(app.template_folder)}")

    from config import app_config
    print("Imported app_config from config.py")
    app.config.from_object(app_config)
    print("Config loaded from app_config")

    try:
        os.makedirs(app.instance_path, exist_ok=True)
        print("Instance path created")
    except OSError as e:
        print(f"Error creating instance path: {e}")

    app.secret_key = app.config.get('SECRET_KEY', 'dev-secret-key-for-testing')
    print("Secret key set")

    socketio.init_app(app, cors_allowed_origins="*")
    print("SocketIO init_app called")

    from . import routes, sockets
    print("Imported routes and sockets")
    app.register_blueprint(routes.bp)
    sockets.init_socketio(socketio)
    print("Blueprints and sockets registered")

    return app

# Create global app instance
app = create_app()

if __name__ == '__main__':
    print("Running locally")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)