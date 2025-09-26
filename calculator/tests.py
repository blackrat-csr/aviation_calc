from django.test import TestCase, Client
from django.urls import reverse
import json
import math

class AviationCalculatorTests(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_wind_triangle_calculation(self):
        """Test wind triangle calculation with known values"""
        data = {
            'true_airspeed': 100,
            'true_course': 90,
            'wind_direction': 45,
            'wind_speed': 20
        }
        
        response = self.client.post(
            reverse('calculator:wind_triangle'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        self.assertIn('drift_angle', result['results'])
        self.assertIn('magnetic_heading', result['results'])
        self.assertIn('ground_speed', result['results'])
    
    def test_great_circle_calculation(self):
        """Test great circle calculation between two known points"""
        # Test calculation between New York and London (approximate coordinates)
        data = {
            'lat1': 40.7128,
            'lon1': -74.0060,
            'lat2': 51.5074,
            'lon2': -0.1278
        }
        
        response = self.client.post(
            reverse('calculator:great_circle'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        self.assertIn('distance', result['results'])
        self.assertIn('initial_bearing', result['results'])
        
        # Distance should be approximately 3000+ nautical miles
        self.assertGreater(result['results']['distance'], 3000)
        self.assertLess(result['results']['distance'], 4000)
    
    def test_rhumb_line_calculation(self):
        """Test rhumb line calculation"""
        data = {
            'lat1': 40.0,
            'lon1': -74.0,
            'lat2': 41.0,
            'lon2': -73.0
        }
        
        response = self.client.post(
            reverse('calculator:rhumb_line'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        self.assertIn('distance', result['results'])
        self.assertIn('bearing', result['results'])
    
    def test_home_page_loads(self):
        """Test that home page loads correctly"""
        response = self.client.get(reverse('calculator:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aviation Calculator')
    
    def test_calculator_pages_load(self):
        """Test that all calculator pages load correctly"""
        pages = ['wind_triangle', 'great_circle', 'rhumb_line', 'history']
        
        for page in pages:
            response = self.client.get(reverse(f'calculator:{page}'))
            self.assertEqual(response.status_code, 200)
    
    def test_invalid_wind_triangle_input(self):
        """Test wind triangle with invalid input"""
        data = {
            'true_airspeed': 0,  # Invalid - would cause division by zero
            'true_course': 90,
            'wind_direction': 45,
            'wind_speed': 100
        }
        
        response = self.client.post(
            reverse('calculator:wind_triangle'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertFalse(result['success'])
