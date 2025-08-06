from pydantic import BaseModel
from typing import List, Optional, TypedDict, Annotated
from langgraph.graph import add_messages

class RecommendationRequest(BaseModel):
    user_input: str

class RecommendationResponse(BaseModel):
    recommendation: str
    product_category: str
    recommended_products: List[str]
    ecommerce_links: dict
    sources: List[dict]

class HealthResponse(BaseModel):
    status: str
    message: str

class ProductRecommendationState(TypedDict):
    messages: Annotated[list, add_messages]
    user_intent: str
    product_category: str
    buying_guide: str
    search_results: str
    final_recommendation: str
    recommended_products: list
    ecommerce_links: dict
    sources: list
