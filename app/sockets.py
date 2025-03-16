from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import session

def init_socketio(socketio: SocketIO):
    """Initialize SocketIO event handlers."""
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection."""
        mode = session.get('mode', 'multi')
        emit('connection_response', {'status': 'connected', 'mode': mode})

    @socketio.on('join_game')
    def handle_join_game(data):
        """Handle a player joining a game room."""
        game_id = data.get('game_id', 'default_room')
        join_room(game_id)
        emit('player_joined', {'game_id': game_id, 'message': 'Player joined'}, room=game_id)

    @socketio.on('leave_game')
    def handle_leave_game(data):
        """Handle a player leaving a game room."""
        game_id = data.get('game_id', 'default_room')
        leave_room(game_id)
        emit('player_left', {'game_id': game_id, 'message': 'Player left'}, room=game_id)

    @socketio.on('buzz')
    def handle_buzz(data):
        """Handle a trivia buzz-in event."""
        game_id = data.get('game_id', 'default_room')
        emit('buzz_received', {'player_id': data.get('player_id'), 'timestamp': data.get('timestamp')}, room=game_id)

    @socketio.on('drawing_update')
    def handle_drawing_update(data):
        """Handle real-time Pictionary drawing updates."""
        game_id = data.get('game_id', 'default_room')
        emit('drawing_broadcast', {'drawing_data': data.get('drawing_data')}, room=game_id)

    @socketio.on('submit_answer')
    def handle_submit_answer(data):
        """Handle answer submissions (e.g., Scattergories, Pictionary guesses)."""
        game_id = data.get('game_id', 'default_room')
        emit('answer_received', {
            'player_id': data.get('player_id'),
            'answer': data.get('answer'),
            'phase': data.get('phase')
        }, room=game_id)

    @socketio.on('vote')
    def handle_vote(data):
        """Handle Cards Against Humanity voting."""
        game_id = data.get('game_id', 'default_room')
        emit('vote_received', {
            'player_id': data.get('player_id'),
            'vote_for': data.get('vote_for')
        }, room=game_id)
