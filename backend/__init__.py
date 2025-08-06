"""
Smart Product Recommendation Backend Package
"""

from .api import create_app
from .agent import SmartProductAgent
from .config import config
from .models import (
    RecommendationRequest,
    RecommendationResponse,
    HealthResponse,
    ProductRecommendationState
)

__version__ = "1.0.0"
__author__ = "Smart Product Recommendation Team"

__all__ = [
    "create_app",
    "SmartProductAgent", 
    "config",
    "RecommendationRequest",
    "RecommendationResponse", 
    "HealthResponse",
    "ProductRecommendationState"
]
