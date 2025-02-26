// Game.js - Client-side spellogica voor Pong

// Globale variabelen
let canvas, ctx;
let paddlePosition = 0;
let gameId = null;
let gameLoop = null;

// Initialiseert het spel wanneer de pagina is geladen
window.onload = function() {
    initGame();
};

// Initialiseert het canvas en spelcomponenten
function initGame() {
    canvas = document.getElementById('gameCanvas');
    if (!canvas) {
        console.error('Canvas element niet gevonden!');
        return;
    }
    
    ctx = canvas.getContext('2d');
    
    // Reset canvas dimensies
    canvas.width = 600;
    canvas.height = 400;
    
    // Start met het verwerken van toetsenbordinvoer
    window.addEventListener('keydown', handleInput);
    
    // Start de game loop
    gameLoop = setInterval(updateGame, 16); // ~60 FPS
    
    // Haal het game ID op uit de URL (als het beschikbaar is)
    const urlParams = new URLSearchParams(window.location.search);
    gameId = urlParams.get('game_id');
    
    if (!gameId) {
        console.error('Game ID niet gevonden in URL!');
    }
}

// Updatet de spelstatus en rendert het spel
function updateGame() {
    if (!gameId) return;
    
    // Haal de huidige spelstatus op van de server
    fetch('/api/game_state?game_id=' + gameId)
        .then(response => response.json())
        .then(gameState => {
            renderGame(gameState);
            
            // Controleer of het spel voorbij is
            if (gameState.game_over) {
                clearInterval(gameLoop);
                alert('Game Over! Je score: ' + gameState.score);
                
                // Vraag of de speler opnieuw wil spelen
                if (confirm('Wil je opnieuw spelen?')) {
                    window.location.href = '/';
                }
            }
        })
        .catch(error => console.error('Fout bij het ophalen van de spelstatus:', error));
    
    // Stuur de huidige paddle positie naar de server
    sendPaddlePosition();
}

// Rendert het spel op basis van de spelstatus
function renderGame(gameState) {
    if (!ctx) return;
    
    // Wis het canvas
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Teken de paddle
    ctx.fillStyle = 'white';
    ctx.fillRect(gameState.paddle_x, gameState.paddle_y, gameState.paddle_width, gameState.paddle_height);
    
    // Teken de bal
    ctx.beginPath();
    ctx.arc(gameState.ball_x, gameState.ball_y, gameState.ball_radius, 0, Math.PI * 2);
    ctx.fillStyle = 'white';
    ctx.fill();
    ctx.closePath();
    
    // Teken de score
    ctx.font = '24px Arial';
    ctx.fillStyle = 'white';
    ctx.fillText('Score: ' + gameState.score, 20, 30);
    
    // Teken de levens
    ctx.fillText('Levens: ' + gameState.lives, canvas.width - 120, 30);
}

// Verwerkt toetsenbordinvoer
function handleInput(event) {
    // Pijl naar links
    if (event.key === 'ArrowLeft') {
        paddlePosition -= 20;
    }
    // Pijl naar rechts
    else if (event.key === 'ArrowRight') {
        paddlePosition += 20;
    }
    
    // Zorg ervoor dat de paddle niet buiten het canvas komt
    paddlePosition = Math.max(0, Math.min(canvas.width - 100, paddlePosition));
    
    // Stuur de bijgewerkte paddle positie naar de server
    sendPaddlePosition();
}

// Stuurt de huidige paddle positie naar de server
function sendPaddlePosition() {
    if (!gameId) return;
    
    fetch('/api/update_paddle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            game_id: gameId,
            paddle_position: paddlePosition
        })
    })
    .catch(error => console.error('Fout bij het versturen van de paddle positie:', error));
}
