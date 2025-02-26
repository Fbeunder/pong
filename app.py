#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
import uuid

# Initialisatie van de Flask applicatie
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Voor het gebruik van sessies

# Tijdelijke opslag voor spel status (in een echte applicatie zou dit een database zijn)
games = {}

# Route voor de startpagina
@app.route('/', methods=['GET'])
def index():
    """Rendert de startpagina met het formulier voor de spelersnaam."""
    return render_template('index.html')

# Route voor de speelpagina
@app.route('/game', methods=['POST'])
def game():
    """
    Verwerkt het formulier van de startpagina en rendert de speelpagina.
    Initialiseert ook een nieuw spel voor de speler.
    """
    player_name = request.form.get('player_name', 'Speler')
    
    # Genereer een uniek game ID
    game_id = str(uuid.uuid4())
    
    # Initialiseer het spel
    games[game_id] = {
        'player_name': player_name,
        'score': 0,
        'lives': 3,
        'paddle_x': 250,  # Startpositie van de paddle
        'paddle_y': 380,
        'paddle_width': 100,
        'paddle_height': 10,
        'ball_x': 300,
        'ball_y': 200,
        'ball_radius': 10,
        'ball_dx': 3,  # Snelheid in x-richting
        'ball_dy': -3,  # Snelheid in y-richting
        'game_over': False
    }
    
    # Sla het game ID op in de sessie
    session['game_id'] = game_id
    
    return render_template('game.html', player_name=player_name, game_id=game_id)

# API endpoint voor het ophalen van de spelstatus
@app.route('/api/game_state', methods=['GET'])
def game_state():
    """Geeft de huidige spelstatus terug als JSON."""
    game_id = request.args.get('game_id')
    
    if not game_id or game_id not in games:
        return jsonify({'error': 'Ongeldig game ID'}), 400
    
    # Update de spelstatus (in een echte implementatie zou dit in modules.game_logic gebeuren)
    update_game_state(game_id)
    
    return jsonify(games[game_id])

# API endpoint voor het updaten van de paddle positie
@app.route('/api/update_paddle', methods=['POST'])
def update_paddle():
    """Werkt de positie van de paddle bij op basis van client input."""
    data = request.json
    game_id = data.get('game_id')
    paddle_position = data.get('paddle_position')
    
    if not game_id or game_id not in games:
        return jsonify({'error': 'Ongeldig game ID'}), 400
    
    # Update de paddle positie
    games[game_id]['paddle_x'] = paddle_position
    
    return jsonify({'success': True})

def update_game_state(game_id):
    """
    Werkt de spelstatus bij (beweegt de bal, controleert botsingen, etc.).
    In een echte implementatie zou dit in modules.game_logic zijn.
    """
    game = games.get(game_id)
    if not game or game['game_over']:
        return
    
    # Beweeg de bal
    game['ball_x'] += game['ball_dx']
    game['ball_y'] += game['ball_dy']
    
    # Controleer botsing met zijkanten
    if game['ball_x'] - game['ball_radius'] <= 0 or game['ball_x'] + game['ball_radius'] >= 600:
        game['ball_dx'] *= -1  # Keer de x-richting om
    
    # Controleer botsing met bovenkant
    if game['ball_y'] - game['ball_radius'] <= 0:
        game['ball_dy'] *= -1  # Keer de y-richting om
    
    # Controleer botsing met paddle
    if (game['ball_y'] + game['ball_radius'] >= game['paddle_y'] and
        game['ball_x'] >= game['paddle_x'] and 
        game['ball_x'] <= game['paddle_x'] + game['paddle_width']):
        game['ball_dy'] *= -1  # Keer de y-richting om
        game['score'] += 1  # Verhoog de score
    
    # Controleer of de bal de onderkant raakt (mis)
    if game['ball_y'] + game['ball_radius'] >= 400:
        game['lives'] -= 1  # Verminder het aantal levens
        
        # Reset de bal
        game['ball_x'] = 300
        game['ball_y'] = 200
        game['ball_dx'] = 3
        game['ball_dy'] = -3
        
        # Controleer of het spel voorbij is
        if game['lives'] <= 0:
            game['game_over'] = True

# Hoofdfunctie om de app te starten
def main():
    """Start de Flask applicatie."""
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
