from flask import Blueprint, render_template, request, jsonify, session
from app import socketio  # Import SocketIO instance for later use

# Create a Blueprint for routes
bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    """Render the main landing page."""
    return render_template('index.html')

@bp.route('/mode_selection', methods=['GET', 'POST'])
def mode_selection():
    """Handle mode selection (single-player or multiplayer)."""
    if request.method == 'POST':
        mode = request.form.get('mode')
        if mode == 'single':
            session['mode'] = 'single'
            return jsonify({'status': 'success', 'redirect': '/game'})
        elif mode == 'multi':
            session['mode'] = 'multi'
            return jsonify({'status': 'success', 'redirect': '/game'})
        return jsonify({'status': 'error', 'message': 'Invalid mode'})
    return render_template('mode_selection.html')

@bp.route('/game')
def game():
    """Render the main game interface."""
    mode = session.get('mode', 'multi')  # Default to multiplayer if not set
    return render_template('index.html', mode=mode)

@bp.route('/api/start_game', methods=['POST'])
def start_game():
    """API endpoint to start a game session."""
    mode = session.get('mode', 'multi')
    # Placeholder for game session initialization
    return jsonify({'status': 'success', 'mode': mode, 'game_id': 'temp_game_id'})