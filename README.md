# Müşteri Segmentasyonu Analitiği

Bu depo, farklı müşteri verileri üzerinde denetimsiz öğrenme ile segmentasyon yapan iki bağımsız projeyi bir araya getirir. Her proje kendi FastAPI uygulamasına, gereksinim dosyasına, Jupyter not defterine ve web arayüzüne sahiptir.

## Projeler

### 1. Kredi Kartı Müşteri Segmentasyonu

`Credit-Cart-Unsupervised/` klasöründeki uygulama; müşterilerin kredi kartı bakiyesi, alışveriş, nakit avans ve kredi limiti gibi finansal özelliklerini kullanarak müşteri segmenti tahmin eder.

- Analiz ve modelleme: `credit_cart.ipynb`
- FastAPI uygulaması: `app.py`
- Web arayüzü: `templates/index.html`
- Beklenen model dosyası: `customer_segmentation_model.pkl`
- Beklenen veri dosyası: `CC GENERAL.csv`
- Segment profilleri: VIP / Premium, Riskli / Nakit Avansçı, Taksitli Alışverişçi ve Pasif / Uyuyan
- <img width="1565" height="782" alt="screenshot" src="https://github.com/user-attachments/assets/3f315ccd-e2ba-4012-a347-6bed11ea2143" />


### 2. E-Ticaret Müşteri Segmentasyonu

`E-Commerce-Unsupervised/` klasöründeki uygulama, e-ticaret alışveriş geçmişinden türetilen RFM metriklerini kullanır:

- **Recency:** Son alışverişten bu yana geçen gün sayısı
- **Frequency:** Alışveriş/fatura sıklığı
- **Monetary:** Toplam harcama

- Analiz ve modelleme: `e_com.ipynb`
- FastAPI uygulaması: `app.py`
- Web arayüzü: `templates/index.html`
- Beklenen model dosyası: `rfm_segmentasyon_modeli.pkl`
- Beklenen veri dosyası: `data.csv`
- Segment profilleri: VIP, Uyuyan, Seyrek ve Riskli Müşteriler
- <img width="893" height="721" alt="screenshot" src="https://github.com/user-attachments/assets/71ec8fee-4fcd-401d-8a78-5719b0aedfb0" />


## Gereksinimler

Python 3.10 veya üzeri önerilir. Her uygulamanın bağımlılıkları kendi `requirements.txt` dosyasında tanımlıdır.

## Uygulamaları çalıştırma

Her iki uygulama aynı `app.py` ve varsayılan portu kullandığından, ayrı klasörlerden ve aynı anda yalnızca farklı portlar belirleyerek çalıştırın.

### Kredi kartı projesi

PowerShell veya terminalde depo kök dizininden:

```powershell
cd Credit-Cart-Unsupervised
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload
```

Uygulamayı `http://127.0.0.1:8000` adresinde, API dokümantasyonunu `http://127.0.0.1:8000/docs` adresinde açın.

### E-ticaret projesi

Yeni bir terminalde depo kök dizininden:

```powershell
cd E-Commerce-Unsupervised
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload --port 8001
```

Uygulamayı `http://127.0.0.1:8001` adresinde, API dokümantasyonunu `http://127.0.0.1:8001/docs` adresinde açın.

> Sanal ortamı etkinleştirme komutu kullandığınız kabuğa ve işletim sistemine göre değişebilir. İkinci uygulama için ayrı bir sanal ortam oluşturmak, bağımlılıkları birbirinden bağımsız tutar.

## Model ve veri dosyaları

API uygulamaları başlatılırken ilgili `.pkl` model dosyasını kendi proje klasörlerinde arar. Bu dosyalar yoksa uygulama başlamaz. Analiz not defterlerini yeniden çalıştırmak için ilgili CSV veri dosyası da gerekir.

Not defterlerindeki `read_csv` satırları geliştiricinin bilgisayarına ait mutlak dosya yolları kullanıyor. Not defterlerini kendi ortamınızda çalıştırmadan önce bu yolları proje klasöründeki CSV dosyalarına göre güncelleyin (ör. `CC GENERAL.csv` veya `data.csv`).

Kredi kartı projesinin `.gitignore` dosyası CSV ve pickle dosyalarını Git dışında tutar. E-ticaret klasöründeki yoksayma kuralları bunları kapsamamaktadır. Depoyu GitHub'a yüklemeden önce dosyaların boyutunu, kullanım/lisans koşullarını ve verilerin kişisel ya da hassas bilgi içerip içermediğini kontrol edin. Büyük veya paylaşılmaması gereken dosyalar için depoya eklemek yerine güvenli bir indirme/kurulum yönergesi sağlayın. Pickle dosyalarını yalnızca güvendiğiniz kaynaklardan kullanın.

## Depo yapısı

```text
.
├── Credit-Cart-Unsupervised/
│   ├── app.py
│   ├── credit_cart.ipynb
│   ├── requirements.txt
│   └── templates/
└── E-Commerce-Unsupervised/
    ├── app.py
    ├── e_com.ipynb
    ├── requirements.txt
    └── templates/
```
