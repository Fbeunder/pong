#!/usr/bin/env python3

import unittest
import sys
import os

# Voeg de root directory toe aan sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestApp(unittest.TestCase):
    """Test cases voor de Pong app."""
    
    def setUp(self):
        """Voorbereiden van de test client."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_index_route(self):
        """Test of de index route correct werkt."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welkom bij Pong', response.data)
    
    def test_game_route(self):
        """Test of de game route correct werkt."""
        response = self.app.post('/game', data={'player_name': 'TestSpeler'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TestSpeler', response.data)
        self.assertIn(b'gameCanvas', response.data)
    
    def test_api_game_state_invalid(self):
        """Test of de API een foutmelding geeft bij een ongeldig game ID."""
        response = self.app.get('/api/game_state?game_id=invalid')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Ongeldig game ID', response.data)
    
    def test_api_update_paddle_invalid(self):
        """Test of de API een foutmelding geeft bij een ongeldig game ID."""
        response = self.app.post('/api/update_paddle', 
                                json={'game_id': 'invalid', 'paddle_position': 100})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Ongeldig game ID', response.data)

if __name__ == '__main__':
    unittest.main()
