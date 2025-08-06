"""
Configuration settings for Smart Product Recommendation API
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    APP_TITLE = "Smart Product Recommendation API"
    APP_DESCRIPTION = "LangGraph tabanlı akıllı ürün öneri sistemi"
    APP_VERSION = "1.0.0"
    
    HOST = "0.0.0.0"
    PORT = 8801
    
    ALLOWED_ORIGINS = ["*"]
    
    MAX_WORKERS = 1
    
    ECOMMERCE_SITES = {
        "Hepsiburada": "https://www.hepsiburada.com/ara?q=",
        "Trendyol": "https://www.trendyol.com/sr?q=",
        "Amazon": "https://www.amazon.com.tr/s?k=",
        "N11": "https://www.n11.com/arama?q=",
        "Çiçeksepeti": "https://www.ciceksepeti.com/arama?query="
    }
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable gerekli")
        return True

config = Config()
