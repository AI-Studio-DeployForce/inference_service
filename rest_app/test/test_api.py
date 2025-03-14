"""
Test module for the REST API endpoints.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class ModelInferenceAPITest(TestCase):
    """Test class for model inference API endpoints."""
    
    def setUp(self):
        """Set up test client and other test variables."""
        self.client = APIClient()
        
    def test_api_health(self):
        """Test the API health endpoint."""
        url = reverse('health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'status': 'healthy'})
        
    def test_model_inference(self):
        """Test the model inference endpoint."""
        # This is a placeholder test that should be updated with actual test data
        url = reverse('predict')
        test_data = {'input': 'test data'}
        response = self.client.post(url, test_data, format='json')
        self.assertEqual(response.status_code, 200) 