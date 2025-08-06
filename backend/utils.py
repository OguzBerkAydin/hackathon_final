import re
import json
from typing import Dict, List, Optional, Any
from urllib.parse import quote_plus

class TextProcessor:
    
    @staticmethod
    def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:

        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            pass
        return None
    
    @staticmethod
    def clean_product_name(name: str) -> str:

        cleaned = re.sub(r'^[-•]\s*', '', name.strip())
        return cleaned if len(cleaned) > 3 else name
    
    @staticmethod
    def parse_product_list(text: str) -> List[str]:

        products = []
        if text:
            for line in text.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('*'):
                    cleaned = TextProcessor.clean_product_name(line)
                    if cleaned:
                        products.append(cleaned)
        return products


class URLGenerator:
    
    @staticmethod
    def create_ecommerce_links(product_name: str, sites: Dict[str, str]) -> Dict[str, str]:
        """
        Create e-commerce links for a product
        
        Args:
            product_name: Name of the product
            sites: Dictionary of site names and base URLs
            
        Returns:
            Dictionary of site names and search URLs
        """
        links = {}
        search_query = quote_plus(product_name)
        
        for site_name, base_url in sites.items():
            try:
                links[site_name] = base_url + search_query
            except Exception as e:
                print(f"Error creating link for {site_name}: {e}")
                continue
                
        return links


class ResponseFormatter:
    
    @staticmethod
    def add_sources_to_text(text: str, sources: List[Dict[str, str]]) -> str:
        """
        Add sources section to recommendation text
        
        Args:
            text: Original recommendation text
            sources: List of source dictionaries
            
        Returns:
            Text with sources appended
        """
        if not sources:
            return text
            
        text += "\n\n---\n\n## 📚 Kaynaklar:\n\n"
        for i, source in enumerate(sources, 1):
            title = source.get('title', 'Başlık Yok')
            url = source.get('url', '')
            
            if '.' in title and len(title.split('.')) > 1:
                title = title.split('.')[0]
            
            text += f"{i}. [{title}]({url})\n"
            
        return text
    
    @staticmethod
    def add_ecommerce_links_to_text(text: str, ecommerce_links: Dict[str, Dict[str, str]]) -> str:
        """
        Add e-commerce links section to recommendation text
        
        Args:
            text: Original recommendation text
            ecommerce_links: Dictionary of products and their e-commerce links
            
        Returns:
            Text with e-commerce links appended
        """
        if not ecommerce_links:
            return text
            
        text += "\n\n---\n\n## 🛒 E-Ticaret Siteleri:\n\n"
        text += "*Önerilen ürünleri aşağıdaki sitelerde bulabilirsiniz:*\n\n"
        
        for product, links in ecommerce_links.items():
            text += f"### 📦 {product}\n\n"
            for site_name, link in links.items():
                text += f"- **[{site_name}]({link})**\n"
            text += "\n"
        
        return text


class PromptTemplates:
    
    INTENT_ANALYSIS_TEMPLATE = """
    Kullanıcının mesajını analiz et ve şu bilgileri çıkar:

    Kullanıcı Mesajı: "{user_message}"

    Görevler:
    1. Kullanıcının satın almak istediği ürün kategorisini belirle
    2. Kullanıcının niyetinin özetini çıkar

    Cevabını şu JSON formatında ver:
    {{
        "product_category": "belirlenen ürün kategorisi (örn: telefon, televizyon, halı)",
        "user_intent": "kullanıcının niyetinin özeti"
    }}
    """
    
    BUYING_GUIDE_TEMPLATE = """
    {product_category} satın almak isteyen kullanıcılar için kısa ve pratik bir satın alma rehberi oluştur.

    Kullanıcı İsteği: {user_intent}
    Ürün Kategorisi: {product_category}

    Rehber şu bölümleri içermeli:
    1. **Dikkat Edilmesi Gereken Ana Özellikler** (3-4 madde)
    2. **Yaygın Hatalar** (1-2 madde)
    3. **Satın Alma İpuçları** (1-2 madde)

    Kısa, öz ve anlaşılır ol. Türkçe yaz.
    """
    
    PRODUCT_SEARCH_TEMPLATE = """
    {product_category} kategorisinde güncel ürün önerilerini araştır.
    
    Arama kriterleri:
    - Türkiye'deki mevcut fiyatlar
    - Farklı bütçe seviyelerinde seçenekler
    - Kullanıcı yorumları ve değerlendirmeleri
    - Teknik özellikler ve performans karşılaştırmaları
    
    Kullanıcı isteği: {user_intent}
    
    En az 3-4 farklı ürün seçeneği bul (bütçe dostu, orta segment, premium).
    """
    
    PRODUCT_EXTRACTION_TEMPLATE = """
    Aşağıdaki ürün araştırma sonuçlarından önerilen ürünlerin listesini çıkar:
    
    Araştırma Sonuçları:
    {search_results}
    
    Sadece ürün isimlerini ver, her satırda bir ürün ismi olacak şekilde.
    Örnek format:
    iPhone 15 Pro
    Samsung Galaxy S24
    Google Pixel 8
    
    Sadece ürün isimleri, başka açıklama yazma.
    """
    
    FINAL_RECOMMENDATION_TEMPLATE = """
    Kapsamlı bir ürün satın alma önerisi hazırla.
    
    Ürün Kategorisi: {product_category}
    
    Satın Alma Rehberi:
    {buying_guide}
    
    Ürün Araştırma Sonuçları:
    {search_results}
    
    Görevler:
    1. Satın alma rehberini özet olarak sun
    2. En iyi 3-4 ürün önerisini farklı bütçe seviyelerinde ver
    3. "En İyi Değer" seçimini belirle ve nedenini açıkla
    4. Kullanıcı yorumlarından önemli noktaları özetle
    5. Final satın alma tavsiyesi ver
    
    Format:
    # 🛍️ {product_category_title} Satın Alma Rehberi
    
    ## 📋 Dikkat Edilmesi Gerekenler
    [rehber özeti]
    
    ## 🏆 Önerilen Ürünler
    [ürün önerileri - fiyat, özellik, artı/eksi]
    
    ## ⭐ En İyi Değer Seçimi
    [bir ürünü öne çıkar ve nedenini açıkla]
    
    ## 💬 Kullanıcı Yorumları Özeti
    [önemli yorumlar]
    
    ## 🎯 Final Tavsiye
    [kısa ve net satın alma tavsiyesi]
    
    Türkçe, net ve kullanışlı bir öneri hazırla.
    """
