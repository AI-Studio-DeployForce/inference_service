"""
API views for the ML model serving endpoints.
"""
import logging
from typing import Any, Dict

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from rest_app.model.model_loader import model_loader

logger = logging.getLogger(__name__)


@api_view(['GET'])
def health_check(request: Request) -> Response:
    """
    Health check endpoint to verify the API is running.
    
    Args:
        request: The HTTP request.
        
    Returns:
        Response with health status.
    """
    return Response({'status': 'healthy'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def predict(request: Request) -> Response:
    """
    Endpoint for making predictions using the ML model.
    
    Args:
        request: The HTTP request containing input data.
        
    Returns:
        Response with prediction results.
    """
    try:
        input_data = request.data
        
        # Validate input data
        if not input_data:
            return Response(
                {'error': 'No input data provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Make prediction
        result = model_loader.predict(input_data)
        
        if result.get('status') == 'error':
            return Response(
                {'error': result.get('message', 'Prediction failed')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response(result, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.exception(f"Error in predict endpoint: {str(e)}")
        return Response(
            {'error': f'Prediction failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def model_info(request: Request) -> Response:
    """
    Endpoint to get information about the loaded model.
    
    Args:
        request: The HTTP request.
        
    Returns:
        Response with model information.
    """
    try:
        # Ensure model is loaded
        if model_loader.model is None:
            model_loader.load_model()
        
        # Get model information
        # This should be customized based on your model
        model_info = {
            'model_path': model_loader.model_path,
            'model_type': type(model_loader.model).__name__,
            'is_loaded': model_loader.model is not None,
        }
        
        return Response(model_info, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.exception(f"Error in model_info endpoint: {str(e)}")
        return Response(
            {'error': f'Failed to get model info: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 