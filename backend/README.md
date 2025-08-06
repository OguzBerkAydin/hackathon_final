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

