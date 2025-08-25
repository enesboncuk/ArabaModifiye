## Araba Modifiye Uygulaması – PRD (Product Requirements Document)

### 1) Ürün Vizyonu
Kullanıcıların kendi araç fotoğrafları üzerinde gerçekçi 2D modifiye denemeleri (jant, jant boyutu, spoiler, renk değişimi vb.) yapabilmesini, ilerleyen aşamada gerçek 3D araç modelleri (.glb/.obj) üzerinden konfigürasyon yapabilmesini sağlayan, OEM uyumlu parça verilerini kullanan bir web/mobil uygulaması.

### 2) Kapsam ve Fazlar
- MVP (2D Temel):
  - Fotoğraf yükleme (jpg/png/webp)
  - Basit araç segmentasyonu (OpenCV/GrabCut veya hazır DL model)
  - Gövde rengi değiştirme (ton/koyuluk/doygunluk)
  - Jant yerleştirme (2D overlay, kullanıcıdan 4 nokta referans/homography)
  - Proje kaydetme/yeniden düzenleme

- V1 (2D İyileştirme + Veri):
  - OEM uyum verisi (araç marka/model/yıl → uyumlu jant çapı/ofset/genişlik)
  - Yarı-otomatik jant hizalama (teker merkez/hub tahmini)
  - Işık/gölge uyumu ve yansıma iyileştirmeleri
  - Basit parça katalogu (spoiler, body kit silüetleri)
  - Hesaplar, favoriler, paylaşım linki

- V2 (3D Destek):
  - 3D araç modeli (.glb önerilir) görüntüleme ve boyama
  - 3D jant yerleştirme ve ölçülendirme
  - Basit ışıklandırma (IBL) ve materyal varyasyonları (metal/pearlescent)
  - Web’de three.js, mobilde Flutter 3D (SceneKit/ARCore köprüleri) değerlendirme

### 3) Hedef Kitle ve Kullanım Senaryoları
- Araç sahipleri: Modifiyeyi satın almadan önce görsel deneme
- Modifiye dükkanları: Müşteriyle opsiyonları hızla gösterme
- Jant üreticileri/dağıtıcılar: Ürün pazarlama görselleştirmesi

### 4) Başlıca Kullanıcı Hikayeleri
- Bir kullanıcı olarak, araç fotoğrafımı yükleyip gövde rengini farklı renklerde görmek istiyorum.
- Bir kullanıcı olarak, OEM uyumlu jantları filtreleyip fotoğrafımda denemek istiyorum.
- Bir kullanıcı olarak, jantı fotoğraf üzerinde seçtiğim 4 noktaya oturtarak perspektifini ayarlamak istiyorum.
- Bir kullanıcı olarak, çalışmamı kaydedip paylaşılabilir bir link almak istiyorum.

### 5) Fonksiyonel Gereksinimler
- Görsel yükleme, önizleme, kaydetme (orijinal + maskeler + katmanlar)
- Segmentasyon: araç gövdesi maskesi (MVP’de tek sınıf; sonraki aşamada lastik/cam/arka plan ayrımı)
- Renk değişimi: HSV/LAB uzayında ton/doygunluk/aydınlık ayarı; gölgelere saygı
- Jant yerleştirme: ölçek/perspektif, opaklık ve gölge blend
- OEM uyum verisi: marka/model/yıl/trim bazında jant/lastik ölçüleri ve bolt pattern
- Projeler: kullanıcı → projeler → sahneler → katmanlar

### 6) Performans ve Diğer Gereksinimler
- API < 500 ms (cache yokken basit işlemler), uzun işlemler için background job
- Görseller için CDN/S3 benzeri saklama, imza ile erişim
- GDPR/KVKK uyumu: açık rıza, silme isteği, loglama
- Mobil ve masaüstü web’e uygun responsive UI

### 7) Mimari Genel Bakış
- Frontend (MVP): React (Vite) web. Alternatif: Flutter (V1’de eklenebilir)
- Backend: FastAPI (Python), Uvicorn, Pydantic; Celery/RQ ile arka plan işler
- Depolama: PostgreSQL (kullanıcı/proje/meta), S3 uyumlu obje (MinIO/AWS S3) görseller
- Kimlik: JWT (short-lived) + refresh; OAuth (Google/Apple) sonra
- 3D (V2): three.js + glTF (.glb), HDRI tabanlı aydınlatma

### 8) API Taslağı
- POST `/api/v1/auth/signup`, `/login`, `/logout`
- GET `/api/v1/catalog/wheels?make=&model=&year=` → OEM uyum listesi
- POST `/api/v1/projects` → yeni proje
- GET `/api/v1/projects/{id}` → proje detay
- POST `/api/v1/images` → fotoğraf yükle (presigned URL opsiyonu)
- POST `/api/v1/ops/segment` → {image_id} → {mask_id}
- POST `/api/v1/ops/recolor` → {image_id, mask_id, hue, sat, light}` → {image_variant_id}
- POST `/api/v1/ops/overlay/wheel` → {image_id, wheel_asset_id, points[4]}` → {image_variant_id}
- GET `/api/v1/assets/wheels` → jant görselleri/3D’leri/katalog meta
- GET `/api/v1/share/{slug}` → public read-only sahne

### 9) Veri Modeli (Basitleştirilmiş)
- users(id, email, hash, created_at)
- projects(id, user_id, title, created_at)
- images(id, project_id, url, width, height, exif)
- masks(id, image_id, kind, url)
- variants(id, image_id, description, url, layers_json)
- assets(id, kind[wheel/spoiler/paint], brand, model, meta_json, thumb_url, file_url)
- vehicle_specs(id, make, model, year, trim, bolt_pattern, rim_diameter, rim_width, offset, center_bore)

### 10) Görüntü İşleme Boru Hattı (MVP → V1)
1) Yükleme → EXIF yön düzeltme, webp’e çevirme, uzun kenarı 2048 px’e sınırlama
2) Segmentasyon:
   - MVP: OpenCV GrabCut/Watershed (kullanıcıdan kaba dikdörtgen) veya hazır U2Net/DeepLabv3
   - V1: Araç sınıfı için hazır model (U2Net/HQ, Segment Anything ile prompts)
3) Renk Değişimi: Maskeli HSV/LAB uzayında ayar; highlight/şadov koruma için dodge/burn haritaları
4) Jant Overlay: Kullanıcıdan 4 nokta → homography → perspektif transform; blend (multiply/soft light)
5) Gölge/Uyum: 
   - Basit: jant grayscale + Gaussian shadow mask; 
   - V1: tahmini yerdeki gölge yönü, ambient occlusion taklidi

### 11) 3D Yol Haritası (V2)
- glTF 2.0 (.glb) standart; PBR materyaller (baseColor, metallicRoughness)
- three.js ile viewer; `model-viewer` fallback
- Jantlar ayrı mesh, teker koordinatlarına instance placement
- IBL/HDRI ile aydınlatma; basit post-processing (ACES tonemap)

### 12) OEM/Orijinal Veri Kaynağı Stratejisi
- Üretici katalogları ve lisanslı veri sağlayıcıları (hukuki izin şart)
- Açık kaynak/Topluluk siteleri: doğruluk/lisans denetimi (örn. wheel-size veri şemasına benzer)
- Veri normalize edilecek: bolt pattern, rim_width (inch), offset (mm), center bore (mm)

### 13) Test Planı
- Birim: segment, recolor, homography fonksiyonları
- Entegrasyon: `/ops/*` uçları için golden image karşılaştırmaları (SSIM/PSNR eşikleri)
- E2E: yükle→segment→recolor→overlay akışı (Playwright/Cypress)
- Performans: büyük görseller, batch işleme

### 14) Güvenlik
- Dosya türü/doğrulama, antivirüs taraması (opsiyonel)
- Presigned URL ile sınırlı süreli erişim
- Rate limit, audit log, PII minimizasyonu

### 15) Dağıtım
- Backend: Docker + Uvicorn/Gunicorn; Render/Fly.io/AWS ECS
- Frontend: Vercel/Netlify, çevre değişkenleri ile API URL
- Medya: S3/CloudFront veya Backblaze B2/Cloudflare R2
- DB: Postgres (Railway/Supabase/RDS)

### 16) Ölçümleme
- Olaylar: upload, segment, recolor, overlay, share
- Dönüşüm hunisi: upload→ilk modifikasyon→kaydet→paylaş

### 17) Riskler ve Azaltmalar
- OEM veri lisansı: Erken hukuk/iş geliştirme, dummy veriyle MVP
- Segmentasyon doğruluğu: kullanıcı yardımlı işaretleme, geri bildirim döngüsü
- Performans maliyeti: önbellek, arka plan işler, downscale/tiling

### 18) Yol Haritası ve Görev Listeleri

#### Yapılacaklar (Backlog)
- [ ] FastAPI iskeleti, temel `/health`, `/images`, `/ops/*`
- [ ] Yerel dosya/S3 saklama modülü
- [ ] Basit GrabCut segmentasyonu uç noktası
- [ ] HSV/LAB renk değişimi fonksiyonu ve uç noktası
- [ ] Jant overlay için homography + blend
- [ ] React web (Vite) upload + mask/overlay UI
- [ ] Postgres şeması ve migrasyonlar
- [ ] Oturum/JWT
- [ ] OEM veri şeması + seed (örnek/dummy)
- [ ] E2E test (Playwright)

#### Yapılanlar
- [x] PRD oluşturuldu (bu dosya)
- [x] FastAPI iskeleti, temel `/health`, `/images`, `/ops/*`
- [x] Yerel dosya/S3 saklama modülü
- [x] Basit GrabCut segmentasyonu uç noktası
- [x] HSV/LAB renk değişimi fonksiyonu ve uç noktası
- [x] Jant overlay için homography + blend
- [x] React web (Vite) upload + mask/overlay UI
- [x] Postgres şeması ve migrasyonlar
- [x] Oturum/JWT authentication sistemi
- [x] Proje yönetimi (CRUD)
- [x] Jant kataloğu ve araç uyumluluğu
- [x] Proje paylaşım sistemi
- [x] Kullanıcı arayüzü (authentication, proje yönetimi, sidebar)

#### Geliştirme Önerileri
- [ ] Segment Anything entegrasyonu ile tıklama tabanlı maskeler
- [ ] Işık/gölge uyumu için gölge yön tahmini (basit edge/gradient analizi)
- [ ] 3D glTF pipeline, araç başına teker koordinat katalogu

---

### Ek: Teknik Kararlar
- Python 3.11+, FastAPI + Pydantic v2
- OpenCV, NumPy, Pillow; DL opsiyon: Torch + U2Net/DeepLabv3
- three.js + glTF; mobilde Flutter ek modül olarak ileride


