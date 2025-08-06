# 🛒 Akıllı Ürün Öneri Sistemi

AI destekli ürün araştırması ve öneri platformu. Kullanıcılar doğal dilde istedikleri ürünleri tarif ederek, sistemden kapsamlı satın alma rehberi ve e-ticaret linklerini alabilirler.

## 🌟 Özellikler

- **Doğal Dil İşleme**: Kullanıcıların günlük dilde yaptıkları istekleri anlayabilir
- **Akıllı Ürün Analizi**: Google Gemini AI modeli ile ürün kategorilerini otomatik tespit eder
- **Kapsamlı Araştırma**: Google Search entegrasyonu ile güncel ürün bilgilerini toplar
- **Satın Alma Rehberi**: Her ürün kategorisi için detaylı satın alma önerileri sunar
- **E-ticaret Entegrasyonu**: Önerilen ürünler için direkt alışveriş linkleri oluşturur
- **Modern Arayüz**: React ve Tailwind CSS ile tasarlanmış kullanıcı dostu arayüz
- **API Tabanlı**: FastAPI ile geliştirilmiş RESTful API

## 🏗️ Sistem Mimarisi

### Backend (Python)
- **FastAPI**: Web API framework'ü
- **Google Gemini**: AI model entegrasyonu
- **LangGraph**: Workflow yönetimi
- **Pydantic**: Veri doğrulama

### Frontend (React)
- **React 19**: Modern UI framework'ü
- **TypeScript**: Tip güvenliği
- **Tailwind CSS**: Stil framework'ü
- **Vite**: Build tool

### Workflow
1. **Niyet Analizi**: Kullanıcı isteğini analiz eder ve ürün kategorisini belirler
2. **Satın Alma Rehberi**: Kategori için detaylı rehber oluşturur
3. **Ürün Araştırması**: Google Search ile güncel ürün bilgilerini toplar
4. **Öneri Oluşturma**: AI destekli kapsamlı öneri hazırlar
5. **E-ticaret Linkleri**: Popüler siteler için alışveriş linkleri ekler

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.10+
- Node.js 18+
- Docker (opsiyonel)
- Google Gemini API anahtarı

### 1. Projeyi İndirin
```bash
git clone <repository-url>
cd hackathon_final
```

### 2. Ortam Değişkenlerini Ayarlayın
Backend klasöründe `.env` dosyası oluşturun:
```env
GEMINI_API_KEY="sizin_api_anahtariniz"
```

### 3. Docker ile Çalıştırma (Önerilen)
```bash
docker-compose up --build
```

### 4. Manuel Kurulum

#### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Kullanım

1. **Web arayüzüne erişin**: http://localhost:3021
2. **Ürün isteğinizi yazın**: 
   - "Oyuncu bilgisayarı arıyorum"
   - "Bebekler için en iyi araba koltuğu"
   - "Kaliteli bir kahve makinesi"
3. **Sonuçları görüntüleyin**: AI destekli öneri ve e-ticaret linkleri

## 🔧 Geliştirme

### Backend Geliştirme
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app
```

### Frontend Geliştirme
```bash
cd frontend
npm run dev
```

## 📁 Proje Yapısı

```
hackathon_final/
├── backend/
│   ├── agent.py          # AI agent workflow
│   ├── api.py            # FastAPI uygulaması
│   ├── models.py         # Pydantic modeller
│   ├── config.py         # Konfigürasyon
│   ├── utils.py          # Yardımcı fonksiyonlar
│   └── requirements.txt  # Python bağımlılıkları
├── frontend/
│   ├── src/
│   │   ├── components/   # React bileşenleri
│   │   ├── types/        # TypeScript tipleri
│   │   └── App.tsx       # Ana uygulama
│   └── package.json      # Node.js bağımlılıkları
└── docker-compose.yml    # Docker konfigürasyonu
```

## 🛠️ Teknolojiler

**Backend:**
- FastAPI
- Google Gemini AI
- LangGraph
- Pydantic
- Uvicorn

**Frontend:**
- React 19
- TypeScript
- Tailwind CSS
- Vite
- Axios

**DevOps:**
- Docker
- Docker Compose

## 📄 Lisans

Bu proje hackathon projesi olarak geliştirilmiştir.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 İletişim

Sorularınız için issue oluşturabilirsiniz.

---

*Bu sistem AI destekli ürün araştırması yaparak kullanıcılara en iyi satın alma kararlarını vermelerine yardımcı olur.*
