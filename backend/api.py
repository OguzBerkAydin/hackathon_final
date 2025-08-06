import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import RecommendationRequest, RecommendationResponse, HealthResponse
from agent import SmartProductAgent
from config import config


class APIApp:
    def __init__(self):
        self.app = FastAPI(
            title=config.APP_TITLE,
            description=config.APP_DESCRIPTION,
            version=config.APP_VERSION
        )
        
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=config.ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self.agent = None
        self.executor = ThreadPoolExecutor(max_workers=config.MAX_WORKERS)
        
        self.app.add_event_handler("startup", self.startup_event)
        
        self._register_routes()
    
    async def startup_event(self):
        try:
            self.agent = SmartProductAgent()
            print("✅ Smart Product Agent başlatıldı")
        except Exception as e:
            print(f"❌ Agent başlatılamadı: {e}")
            raise e
    
    def _register_routes(self):
        
        @self.app.get("/", response_model=HealthResponse)
        async def root():
            return HealthResponse(
                status="healthy",
                message="Smart Product Recommendation API çalışıyor"
            )
        
        @self.app.get("/health", response_model=HealthResponse)
        async def health_check():
            if self.agent is None:
                raise HTTPException(status_code=503, detail="Agent henüz başlatılmadı")
            
            return HealthResponse(
                status="healthy",
                message="Tüm sistemler çalışıyor"
            )
        
        @self.app.post("/recommend", response_model=RecommendationResponse)
        async def get_recommendation(request: RecommendationRequest):
            if self.agent is None:
                raise HTTPException(status_code=503, detail="Agent henüz başlatılmadı")
            
            if not request.user_input.strip():
                raise HTTPException(status_code=400, detail="Ürün isteği boş olamaz")
            
            try:
                
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self.executor, 
                    self.agent.get_recommendation, 
                    request.user_input
                )
                
                return RecommendationResponse(
                    recommendation=result["recommendation"],
                    product_category=result["product_category"],
                    recommended_products=result["recommended_products"],
                    ecommerce_links=result["ecommerce_links"],
                    sources=result["sources"]
                )
                
            except Exception as e:
                print(f"❌ Öneri hatası: {e}")
                raise HTTPException(status_code=500, detail=f"Öneri oluşturulamadı: {str(e)}")


def create_app() -> FastAPI:
    api_app = APIApp()
    return api_app.app
