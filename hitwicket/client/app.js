let socket = new WebSocket('ws://localhost:8765');
let currentPlayer = 'A'; // Start with Player A
let selectedCharacter = null;

socket.onopen = function() {
    console.log('WebSocket connection established');
    initializeGame();
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Message received:', data);

    if (data.type === 'state_update') {
        updateBoard(data.board);
        currentPlayer = data.turn;  // Update current player based on the server's response
        document.getElementById('status').innerText = `Player ${currentPlayer}'s turn`;
        selectedCharacter = null; // Reset selected character after state update
    } else if (data.type === 'invalid_move') {
        alert('Invalid move! Try again.');
        selectedCharacter = null; // Reset selected character on invalid move
    } else if (data.type === 'game_over') {
        updateBoard(data.board);
        alert(`Player ${data.winner} wins!`);
        document.getElementById('status').innerText = `Player ${data.winner} wins!`;
        selectedCharacter = null; // Reset selected character on game over
    }
};

socket.onerror = function(error) {
    console.log('WebSocket Error:', error);
    alert('WebSocket Error: ' + error.message);
};

socket.onclose = function(event) {
    console.log('WebSocket connection closed:', event);
};

function initializeGame() {
    console.log('Initializing game');
    const playerA = ['A-P1', 'A-H1', 'A-H2', 'A-P2', 'A-P3'];
    const playerB = ['B-P1', 'B-H1', 'B-H2', 'B-P2', 'B-P3'];

    const initMessage = JSON.stringify({
        type: 'initialize',
        playerA: playerA,
        playerB: playerB
    });

    console.log('Sending initialization message:', initMessage);
    socket.send(initMessage);
}

// Function to update the game board display
function updateBoard(boardState) {
    console.log('Updating board:', boardState);
    const board = document.getElementById('game-board');
    board.innerHTML = '';
    for (let row = 0; row < 5; row++) {
        for (let col = 0; col < 5; col++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            const content = boardState[row][col];
            if (content) {
                cell.classList.add(content.startsWith('A') ? 'playerA' : 'playerB');
                cell.innerText = content;
                cell.dataset.character = content; // Add character name to dataset
            }
            cell.dataset.row = row; // Add row and col as data attributes
            cell.dataset.col = col;
            cell.addEventListener('click', () => handleCellClick(row, col, content));
            board.appendChild(cell);
        }
    }
}

// Function to handle cell clicks
function handleCellClick(row, col, content) {
    console.log('Cell clicked:', { row, col, content });
    if (!selectedCharacter) {
        if (content && content.startsWith(currentPlayer)) { // Ensure that the clicked cell has content
            selectedCharacter = content;
            console.log('Character selected:', selectedCharacter);
            showMoveOptions();
        } else {
            alert('Select your own character!');
        }
    } else {
        const move = prompt('Enter move (L, R, F, B for Pawns and Hero1; FL, FR, BL, BR for Hero2):');
        if (move) {
            sendMove(selectedCharacter, move);
            selectedCharacter = null;
            hideMoveOptions();
        }
    }
}

// Function to display move options for selected character
function showMoveOptions() {
    const moveOptions = document.getElementById('move-options');
    moveOptions.innerHTML = '';
    const characterType = selectedCharacter.split('-')[1];
    let validMoves;
    if (characterType === 'P' || characterType === 'H1') {
        validMoves = ['L', 'R', 'F', 'B'];
    } else if (characterType === 'H2') {
        validMoves = ['FL', 'FR', 'BL', 'BR'];
    }
    validMoves.forEach(move => {
        const button = document.createElement('button');
        button.innerText = move;
        button.onclick = () => {
            sendMove(selectedCharacter, move);
            selectedCharacter = null;
            hideMoveOptions();
        };
        moveOptions.appendChild(button);
    });
}

// Function to send the selected move to the server
function sendMove(character, move) {
    if (currentPlayer !== character[0]) {
        alert('Not your turn!');
        return;
    }
    console.log(`Sending move: ${character} ${move}`);
    socket.send(JSON.stringify({
        type: 'move',
        player: currentPlayer,
        character: character,
        move: move
    }));
}

function hideMoveOptions() {
    const moveOptions = document.getElementById('move-options');
    moveOptions.innerHTML = '';
}
