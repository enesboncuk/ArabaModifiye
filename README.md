# Araba Modifiye MVP

Araç modifiye denemeleri için 2D görsel işleme uygulaması. Kullanıcılar araç fotoğrafları üzerinde renk değişimi, jant ekleme ve segmentasyon işlemleri yapabilir.

## Özellikler

### MVP (Mevcut)
- ✅ Kullanıcı kaydı ve girişi (JWT authentication)
- ✅ Proje yönetimi (oluşturma, listeleme, düzenleme)
- ✅ Fotoğraf yükleme ve yönetimi
- ✅ Araç gövdesi segmentasyonu (OpenCV GrabCut)
- ✅ HSV renk uzayında renk değişimi
- ✅ Jant overlay (homography transform)
- ✅ Jant kataloğu ve araç uyumluluğu
- ✅ Proje paylaşımı

### V1 (Planlanan)
- 🔄 OEM uyum verisi entegrasyonu
- 🔄 Yarı-otomatik jant hizalama
- 🔄 Işık/gölge uyumu iyileştirmeleri
- 🔄 Gelişmiş parça kataloğu

### V2 (Gelecek)
- 🔮 3D araç model desteği
- 🔮 Three.js ile 3D görüntüleme
- 🔮 PBR materyal sistemi

## Teknoloji Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM ve veritabanı yönetimi
- **PostgreSQL** - Ana veritabanı
- **OpenCV** - Görsel işleme
- **NumPy** - Sayısal işlemler
- **JWT** - Authentication
- **Pydantic** - Veri validasyonu

### Frontend
- **React 18** - UI framework
- **TypeScript** - Tip güvenliği
- **Vite** - Build tool
- **Modern CSS** - Responsive tasarım

## Kurulum

### Gereksinimler
- Python 3.11+
- Node.js 18+
- PostgreSQL 13+
- OpenCV

### Backend Kurulumu

1. **Repository'yi klonlayın:**
```bash
git clone <repository-url>
cd ArabaModifiye/backend
```

2. **Virtual environment oluşturun:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

3. **Dependencies'leri yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Environment dosyası oluşturun:**
```bash
cp .env.example .env
# .env dosyasını düzenleyin
```

5. **Veritabanını kurun:**
```bash
# PostgreSQL'de veritabanı oluşturun
createdb arabamodifiye

# Tabloları oluşturun (uygulama ilk çalıştığında otomatik)
```

6. **Uygulamayı çalıştırın:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Kurulumu

1. **Frontend dizinine gidin:**
```bash
cd ../frontend
```

2. **Dependencies'leri yükleyin:**
```bash
npm install
```

3. **Environment dosyası oluşturun:**
```bash
# .env.local dosyası oluşturun
echo "VITE_API_BASE=http://localhost:8000" > .env.local
```

4. **Uygulamayı çalıştırın:**
```bash
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Kullanıcı kaydı
- `POST /api/v1/auth/login` - Kullanıcı girişi
- `GET /api/v1/auth/me` - Mevcut kullanıcı bilgisi

### Projects
- `POST /api/v1/projects` - Yeni proje oluşturma
- `GET /api/v1/projects` - Proje listesi
- `GET /api/v1/projects/{id}` - Proje detayı
- `PUT /api/v1/projects/{id}` - Proje güncelleme
- `DELETE /api/v1/projects/{id}` - Proje silme

### Images
- `POST /api/v1/images` - Fotoğraf yükleme
- `GET /api/v1/images/{id}` - Fotoğraf bilgisi
- `DELETE /api/v1/images/{id}` - Fotoğraf silme

### Operations
- `POST /api/v1/ops/segment` - Segmentasyon
- `POST /api/v1/ops/recolor` - Renk değişimi
- `POST /api/v1/ops/overlay/wheel` - Jant overlay

### Catalog
- `GET /api/v1/catalog/wheels` - Jant listesi
- `GET /api/v1/catalog/vehicles` - Araç özellikleri
- `GET /api/v1/catalog/wheels/compatible` - Uyumlu jantlar

### Share
- `POST /api/v1/share/projects` - Proje paylaşımı
- `GET /api/v1/share/{slug}` - Paylaşılan proje

## Kullanım

1. **Kayıt olun veya giriş yapın**
2. **Yeni proje oluşturun**
3. **Araç fotoğrafı yükleyin**
4. **Segmentasyon yapın** (gövde maskesi oluşturur)
5. **Renk değişimi yapın** (HSV sliders ile)
6. **Jant ekleyin** (katalogdan seçip overlay)
7. **Projeyi kaydedin ve paylaşın**

## Geliştirme

### Backend Geliştirme
```bash
cd backend
# Code formatting
black app/
# Linting
flake8 app/
# Type checking
mypy app/
```

### Frontend Geliştirme
```bash
cd frontend
# Code formatting
npm run format
# Linting
npm run lint
# Type checking
npm run type-check
```

### Test
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Veritabanı Şeması

### Ana Tablolar
- `users` - Kullanıcı bilgileri
- `projects` - Proje bilgileri
- `images` - Yüklenen fotoğraflar
- `masks` - Segmentasyon maskeleri
- `variants` - İşlenmiş görseller
- `assets` - Jant/spoiler vb. parçalar
- `vehicle_specs` - Araç özellikleri

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## İletişim

Proje hakkında sorularınız için issue açabilir veya pull request gönderebilirsiniz.

## Roadmap

- [x] MVP temel özellikleri
- [ ] OEM veri entegrasyonu
- [ ] Gelişmiş segmentasyon (AI tabanlı)
- [ ] 3D model desteği
- [ ] Mobil uygulama
- [ ] Sosyal özellikler (beğeni, yorum)
- [ ] Parça satış entegrasyonu
