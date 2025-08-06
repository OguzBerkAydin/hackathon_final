# Smart Product Recommendation Backend - Modular Architecture

## 📁 Dosya Yapısı

Kodunuz artık daha modüler ve bakımı kolay bir yapıya sahip:

```
backend/
├── __init__.py          # Package initialization
├── main.py              # Ana giriş noktası (basitleştirilmiş)
├── config.py            # Konfigürasyon ve ayarlar
├── models.py            # Pydantic modelleri ve TypedDict'ler
├── agent.py             # SmartProductAgent sınıfı ve mantığı
├── api.py               # FastAPI uygulama ve route'ları
├── utils.py             # Yardımcı fonksiyonlar ve araçlar
├── requirements.txt     # Bağımlılıklar
└── .env                 # Çevre değişkenleri
```

## 🔧 Modüler Yapının Faydaları

### 1. **Ayrılmış Sorumluluklar**
- **config.py**: Tüm konfigürasyon ve ayarlar
- **models.py**: Veri modelleri ve type tanımları
- **agent.py**: İş mantığı ve LangGraph workflow'u
- **api.py**: Web API ve HTTP route'ları
- **utils.py**: Ortak yardımcı fonksiyonlar

### 2. **Kolay Bakım**
- Her modül kendi sorumluluğuna odaklanır
- Değişiklikler izole edilir
- Test etmek daha kolay

### 3. **Yeniden Kullanılabilirlik**
- Utility fonksiyonları farklı modüllerde kullanılabilir
- Agent sınıfı bağımsız olarak test edilebilir
- API katmanı farklı backend'lerle çalışabilir

### 4. **Ölçeklenebilirlik**
- Yeni özellikler kolayca eklenebilir
- Kod organizasyonu net ve anlaşılır
- Ekip çalışması için uygun

## 📦 Modül Detayları

### `config.py`
- Çevre değişkenleri yönetimi
- Uygulama ayarları
- E-ticaret site listesi
- Konfigürasyon doğrulama

### `models.py`
- Pydantic modelleri (API için)
- TypedDict tanımları (LangGraph için)
- Veri doğrulama ve serileştirme

### `agent.py`
- SmartProductAgent sınıfı
- LangGraph workflow tanımı
- AI model entegrasyonu
- İş mantığı implementasyonu

### `api.py`
- FastAPI uygulama kurulumu
- HTTP route tanımları
- Middleware konfigürasyonu
- Hata yönetimi

### `utils.py`
- Metin işleme araçları
- URL oluşturma fonksiyonları
- Yanıt formatlama
- Prompt şablonları

## 🚀 Kullanım

### Geliştirme Ortamında Çalıştırma
```bash
cd backend
python main.py
```

### Production Ortamında
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8801
```

### Modülleri İçe Aktarma
```python
from backend import SmartProductAgent, config
from backend.models import RecommendationRequest
from backend.utils import TextProcessor
```

## 🔄 Migration Bilgileri

Önceki tek dosya yapısından bu modüler yapıya geçiş:

1. **Kod değişikliği yok**: Mevcut API ve fonksiyonalite aynı
2. **Import'lar otomatik**: `__init__.py` ile kolay erişim
3. **Geriye uyumluluk**: Eski kullanım şekilleri çalışmaya devam eder
4. **Performans**: Aynı performans, daha iyi organizasyon

## 📈 Gelecek İyileştirmeler

Bu modüler yapı sayesinde kolayca eklenebilecek özellikler:

- **Caching**: `utils.py`'da cache decorator'ları
- **Database**: Yeni bir `database.py` modülü
- **Authentication**: `auth.py` modülü
- **Logging**: `logging.py` modülü
- **Testing**: Modüler test dosyaları
- **Monitoring**: `monitoring.py` modülü

## 🛠️ Geliştirici Notları

- Her modül kendi import'larını yapar
- Circular import'ları önlemek için dikkatli olun
- Type hint'leri tutarlı şekilde kullanın
- Docstring'leri güncel tutun
- Utility fonksiyonları statik yapmayı tercih edin
