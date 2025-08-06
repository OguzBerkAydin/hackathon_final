import time
from typing import Dict

from google.genai import Client
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage

from models import ProductRecommendationState
from config import config
from utils import (
    TextProcessor, 
    URLGenerator, 
    ResponseFormatter, 
    PromptTemplates
)


class SmartProductAgent:
    def __init__(self):
        config.validate_config()
        
        self.client = Client(api_key=config.GEMINI_API_KEY)
        self.graph = self._build_graph()
        self.ecommerce_sites = config.ECOMMERCE_SITES
    
    def _build_graph(self) -> StateGraph:
        """LangGraph workflow'u"""
        workflow = StateGraph(ProductRecommendationState)
        
        workflow.add_node("analyze_intent", self._analyze_intent_node)
        workflow.add_node("generate_buying_guide", self._generate_buying_guide_node)
        workflow.add_node("search_products", self._search_products_node)
        workflow.add_node("generate_recommendation", self._generate_recommendation_node)
        workflow.add_node("search_ecommerce_links", self._search_ecommerce_links_node)
        
        workflow.add_edge(START, "analyze_intent")
        workflow.add_edge("analyze_intent", "generate_buying_guide")
        workflow.add_edge("generate_buying_guide", "search_products")
        workflow.add_edge("search_products", "generate_recommendation")
        workflow.add_edge("generate_recommendation", "search_ecommerce_links")
        workflow.add_edge("search_ecommerce_links", END)
        
        return workflow.compile()
    
    def _analyze_intent_node(self, state: ProductRecommendationState) -> ProductRecommendationState:
        """NODE 1: Kullanıcı niyetini analiz et ve ürün kategorisini belirle"""
        user_message = state["messages"][-1].content
        
        print(f"🎯 Kullanıcı niyeti analiz ediliyor: {user_message}")
        
        prompt = PromptTemplates.INTENT_ANALYSIS_TEMPLATE.format(
            user_message=user_message
        )
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config={"temperature": 0.3}
            )
            
            result = TextProcessor.extract_json_from_text(response.text.strip())
            
            if result:
                print(f"📋 Ürün kategorisi: {result['product_category']}")
                return {
                    "product_category": result["product_category"],
                    "user_intent": result["user_intent"]
                }
            else:
                raise ValueError("JSON parse edilemedi")
            
        except Exception as e:
            print(f"Intent analizi başarısız: {e}")
            return {
                "product_category": "genel ürün",
                "user_intent": user_message
            }
    
    def _generate_buying_guide_node(self, state: ProductRecommendationState) -> ProductRecommendationState:
        """NODE 2: Satın alma rehberi oluştur"""
        product_category = state["product_category"]
        user_intent = state["user_intent"]
        
        print(f"📖 {product_category} için satın alma rehberi oluşturuluyor...")
        
        prompt = PromptTemplates.BUYING_GUIDE_TEMPLATE.format(
            product_category=product_category,
            user_intent=user_intent
        )
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"temperature": 0.3}
            )
            
            buying_guide = response.text.strip()
            print(f"✅ Satın alma rehberi hazır")
            
            return {
                "buying_guide": buying_guide
            }
            
        except Exception as e:
            print(f"Rehber oluşturulamadı: {e}")
            return {
                "buying_guide": f"{product_category} için genel satın alma önerileri araştırılıyor..."
            }
    
    def _search_products_node(self, state: ProductRecommendationState) -> ProductRecommendationState:
        """NODE 3: Ürün arama ve analiz"""
        product_category = state["product_category"]
        user_intent = state["user_intent"]
        
        print(f"🔍 {product_category} ürünleri araştırılıyor...")
        
        search_prompt = PromptTemplates.PRODUCT_SEARCH_TEMPLATE.format(
            product_category=product_category,
            user_intent=user_intent
        )
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=search_prompt,
                config={
                    "tools": [{"google_search": {}}],
                    "temperature": 0
                }
            )
            
            search_results = response.text
            
            sources = []
            if (hasattr(response, 'candidates') and 
                response.candidates and 
                hasattr(response.candidates[0], 'grounding_metadata') and
                response.candidates[0].grounding_metadata and
                hasattr(response.candidates[0].grounding_metadata, 'grounding_chunks')):
                
                for chunk in response.candidates[0].grounding_metadata.grounding_chunks:
                    if hasattr(chunk, 'web') and chunk.web:
                        source = {
                            'title': chunk.web.title if hasattr(chunk.web, 'title') else 'Başlık Yok',
                            'url': chunk.web.uri if hasattr(chunk.web, 'uri') else '',
                        }
                        sources.append(source)
            
            print(f"✅ Ürün araştırması tamamlandı - {len(sources)} kaynak")
            
            return {
                "search_results": search_results,
                "sources": sources
            }
            
        except Exception as e:
            print(f"Ürün araması başarısız: {e}")
            return {
                "search_results": f"{product_category} için ürün bilgileri bulunamadı.",
                "sources": []
            }
    
    def _generate_recommendation_node(self, state: ProductRecommendationState) -> ProductRecommendationState:
        """NODE 4: Final öneri oluştur ve ürün listesi çıkar"""
        product_category = state["product_category"]
        buying_guide = state["buying_guide"]
        search_results = state["search_results"]
        sources = state.get("sources", [])
        
        print(f"🎯 Final öneri hazırlanıyor...")
        
        product_extraction_prompt = PromptTemplates.PRODUCT_EXTRACTION_TEMPLATE.format(
            search_results=search_results
        )
        
        try:
            product_response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=product_extraction_prompt,
                config={"temperature": 0.1}
            )
            
            recommended_products = TextProcessor.parse_product_list(product_response.text)
            
            print(f"📦 {len(recommended_products)} ürün tespit edildi")
            
        except Exception as e:
            print(f"Ürün listesi çıkarma hatası: {e}")
            recommended_products = []
        
        prompt = PromptTemplates.FINAL_RECOMMENDATION_TEMPLATE.format(
            product_category=product_category,
            product_category_title=product_category.title(),
            buying_guide=buying_guide,
            search_results=search_results
        )
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"temperature": 0.2}
            )
            
            final_recommendation = response.text
            
            final_recommendation = ResponseFormatter.add_sources_to_text(
                final_recommendation, sources
            )
            
            print(f"🎉 Final öneri hazır!")
            
            return {
                "final_recommendation": final_recommendation,
                "recommended_products": recommended_products,
                "messages": [AIMessage(content=final_recommendation)]
            }
            
        except Exception as e:
            print(f"Final öneri oluşturulamadı: {e}")
            error_message = "Öneri oluşturulamadı."
            return {
                "final_recommendation": error_message,
                "recommended_products": [],
                "messages": [AIMessage(content=error_message)]
            }
    
    def _search_ecommerce_links_node(self, state: ProductRecommendationState) -> ProductRecommendationState:
        """NODE 5: E-ticaret sitelerinde ürün linkleri ara"""
        recommended_products = state.get("recommended_products", [])
        final_recommendation = state.get("final_recommendation", "")
        
        print(f"🛒 E-ticaret linkleri aranıyor...")
        
        if not recommended_products:
            print("⚠️ Önerilen ürün bulunamadı, e-ticaret araması yapılamıyor")
            return {"ecommerce_links": {}}
        
        ecommerce_links = {}
        
        for product in recommended_products[:4]:
            print(f"   🔍 Aranan ürün: {product}")
            
            product_links = URLGenerator.create_ecommerce_links(product, self.ecommerce_sites)
            
            if product_links:
                ecommerce_links[product] = product_links
                print(f"      ✅ {len(product_links)} site linki oluşturuldu")
            
            time.sleep(0.1)
        
        final_recommendation = ResponseFormatter.add_ecommerce_links_to_text(
            final_recommendation, ecommerce_links
        )
        
        print(f"🎉 E-ticaret linkleri hazır! {len(ecommerce_links)} ürün için linkler oluşturuldu")
        
        return {
            "ecommerce_links": ecommerce_links,
            "final_recommendation": final_recommendation,
            "messages": [AIMessage(content=final_recommendation)]
        }
    
    def get_recommendation(self, user_input: str) -> Dict:
        """Kullanıcı isteğine göre ürün önerisi al"""
        print("\n" + "="*60)
        print("🛒 Akıllı Ürün Öneri Ajanı Başlatılıyor...")
        print("="*60)
        
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "user_intent": "",
            "product_category": "",
            "buying_guide": "",
            "search_results": "",
            "final_recommendation": "",
            "recommended_products": [],
            "ecommerce_links": {},
            "sources": []
        }
        
        result = self.graph.invoke(initial_state)
        
        return {
            "recommendation": result["final_recommendation"],
            "product_category": result["product_category"],
            "recommended_products": result["recommended_products"],
            "ecommerce_links": result["ecommerce_links"],
            "sources": result["sources"]
        }
