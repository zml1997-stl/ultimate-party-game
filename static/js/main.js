// Initialize SocketIO connection
const socket = io.connect(location.protocol + '//' + location.host);

// Global variables
let gameId = null;
let currentPhase = null;

$(document).ready(function() {
    // Handle SocketIO connection
    socket.on('connect', function() {
        $('#gameStatus').text('Connected to game server');
        socket.emit('join_game', { game_id: 'default_room' });
    });

    // Display player join/leave events
    socket.on('player_joined', function(data) {
        $('#gameStatus').append(`<br>${data.message}`);
    });

    socket.on('player_left', function(data) {
        $('#gameStatus').append(`<br>${data.message}`);
    });

    // Start game button
    $('#startGame').click(function() {
        $.post('/api/start_game', function(response) {
            if (response.status === 'success') {
                gameId = response.game_id;
                $('#gameStatus').text(`Game started in ${response.mode} mode (ID: ${gameId})`);
                $('#startGame').hide();
                // Placeholder for phase activation (to be expanded later)
                startPhase('trivia');
            }
        });
    });

    // Buzz button (Trivia)
    $('#buzzButton').click(function() {
        socket.emit('buzz', { game_id: gameId, player_id: 'player_' + socket.id, timestamp: Date.now() });
    });

    socket.on('buzz_received', function(data) {
        $('#gameStatus').append(`<br>Player ${data.player_id} buzzed in!`);
    });
});

// Function to switch game phases (placeholder for now)
function startPhase(phase) {
    $('.game-phase').hide();
    currentPhase = phase;
    switch (phase) {
        case 'trivia':
            $('#triviaPhase').show();
            $('#triviaQuestion').text('Waiting for trivia question...');
            break;
        // Add other phases later
    }
}