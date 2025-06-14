# Kuis Trivia API

[![Deploy Status](https://img.shields.io/badge/Deploy-Live-success)](https://kuis-trivia-api-263444552508.asia-southeast2.run.app)
[![API Docs](https://img.shields.io/badge/API-Docs-blue)](https://kuis-trivia-api-263444552508.asia-southeast2.run.app/docs)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

API REST untuk menyediakan soal kuis trivia berbahasa Indonesia yang dapat diintegrasikan dengan aplikasi Flutter atau aplikasi mobile/web lainnya.

🌐 **Live API**: https://kuis-trivia-api-263444552508.asia-southeast2.run.app  
📖 **Dokumentasi Interaktif**: https://kuis-trivia-api-263444552508.asia-southeast2.run.app/docs

## 📋 Fitur

- ✅ Menyediakan soal kuis trivia berbahasa Indonesia
- ✅ 4 kategori soal: sejarah, geografi, sains, umum
- ✅ Support CORS untuk Flutter dan aplikasi web
- ✅ Dokumentasi Swagger/OpenAPI otomatis
- ✅ Data tersimpan dalam file JSON
- ✅ Docker ready untuk deployment
- ✅ Siap deploy ke Google Cloud Run
- ✅ Sudah live dan dapat diakses secara publik

## 🏗️ Teknologi yang Digunakan

- **Backend**: FastAPI (Python)
- **Database**: JSON file storage
- **Containerization**: Docker
- **Cloud Platform**: Google Cloud Run
- **CI/CD**: Google Cloud Build
- **Documentation**: Swagger/OpenAPI

## 🚀 Quick Start

### Menggunakan API Live (Recommended)

Langsung gunakan API yang sudah terdeploy:

```bash
# Test API
curl "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/"

# Ambil daftar kategori
curl "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/kategori"

# Ambil 5 soal acak
curl "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?jumlah=5"
```

### Menjalankan Lokal

1. **Clone repository**
   ```bash
   git clone https://github.com/your-username/kuis-trivia-api.git
   cd kuis-trivia-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan server**
   ```bash
   # Opsi 1: Menggunakan script bantuan
   python run_local.py
   
   # Opsi 2: Langsung dengan uvicorn
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Akses API**
   - API: http://localhost:8000
   - Dokumentasi: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Menjalankan dengan Docker

1. **Build dan run menggunakan script**
   ```bash
   python docker_build_run.py
   ```

2. **Atau manual dengan Docker commands**
   ```bash
   # Build image
   docker build -t kuis-trivia-api .
   
   # Run container
   docker run -d --name kuis-trivia-api -p 8000:8000 kuis-trivia-api
   ```

## 📖 API Endpoints

| Method | Endpoint | Deskripsi | Parameters |
|--------|----------|-----------|------------|
| `GET` | `/` | Informasi API | - |
| `GET` | `/health` | Health check | - |
| `GET` | `/kategori` | Ambil daftar kategori | - |
| `GET` | `/soal` | Ambil daftar soal | `kategori`, `jumlah` |
| `POST` | `/soal` | Tambah soal baru | JSON body |
| `GET` | `/soal/{id}` | Ambil detail soal | `id` (UUID) |
| `DELETE` | `/soal/{id}` | Hapus soal | `id` (UUID) |

### Query Parameters

#### GET /soal
- `kategori` (optional): Filter berdasarkan kategori (`geografi`, `sains`, `sejarah`, `umum`)
- `jumlah` (optional): Jumlah soal (default: 10, max: 50)

## 📝 Contoh Penggunaan

### Live API Examples

```bash
# Mengambil informasi API
curl "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/"

# Mengambil daftar kategori
curl "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/kategori"

# Mengambil 3 soal acak
curl "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?jumlah=3"

# Mengambil soal kategori geografi
curl "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?kategori=geografi&jumlah=5"

# Mengambil soal kategori sains
curl "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?kategori=sains&jumlah=2"
```

### Local Development Examples

```bash
# Mengambil 5 soal acak
curl "http://localhost:8000/soal?jumlah=5"

# Mengambil soal kategori sejarah
curl "http://localhost:8000/soal?kategori=sejarah&jumlah=3"

# Menambah soal baru
curl -X POST "http://localhost:8000/soal" \
  -H "Content-Type: application/json" \
  -d '{
    "pertanyaan": "Ibu kota Jawa Barat adalah?",
    "pilihan": ["Bandung", "Jakarta", "Surabaya", "Medan"],
    "jawaban": "Bandung",
    "kategori": "geografi"
  }'
```

### Response Format

#### GET /soal
```json
{
  "soal": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "pertanyaan": "Siapa presiden pertama Indonesia?",
      "pilihan": ["Soekarno", "Soeharto", "Habibie", "Megawati"],
      "jawaban": "Soekarno",
      "kategori": "sejarah"
    }
  ],
  "total": 1,
  "kategori": null,
  "jumlah": 10
}
```

#### GET /kategori
```json
{
  "kategori": ["geografi", "sains", "sejarah", "umum"]
}
```

#### GET /
```json
{
  "pesan": "Selamat datang di Kuis Trivia API",
  "versi": "1.0.0",
  "dokumentasi": "/docs",
  "status": "aktif"
}
```

## 🚀 Deploy ke Google Cloud Run

### Prerequisites
1. Install [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
2. Login dan setup project:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

### Opsi 1: Otomatis dengan Cloud Build (Recommended)

**Setup sekali:**
```bash
# 1. Setup Cloud Build trigger
python setup_cloud_build.py

# 2. Push ke GitHub repository
git add .
git commit -m "Initial commit"
git push origin main
```

**Deployment otomatis:**
- Push ke `main` branch → Production deployment
- Push ke `develop` branch → Staging deployment

📖 **Panduan lengkap:** [CLOUD_BUILD_SETUP.md](CLOUD_BUILD_SETUP.md)

### Opsi 2: Manual Deploy

1. **Build dan upload ke Container Registry**
   ```bash
   # Build dan tag image
   docker build -t gcr.io/YOUR_PROJECT_ID/kuis-trivia-api .
   
   # Push ke Google Container Registry
   docker push gcr.io/YOUR_PROJECT_ID/kuis-trivia-api
   ```

2. **Deploy ke Cloud Run**
   ```bash
   gcloud run deploy kuis-trivia-api \
     --image gcr.io/YOUR_PROJECT_ID/kuis-trivia-api \
     --platform managed \
     --region asia-southeast2 \
     --allow-unauthenticated \
     --port 8000 \
     --memory 512Mi \
     --cpu 1
   ```

3. **Alternatif: Deploy langsung dari source code**
   ```bash
   gcloud run deploy kuis-trivia-api \
     --source . \
     --platform managed \
     --region asia-southeast2 \
     --allow-unauthenticated \
     --port 8000
   ```

## 📱 Integrasi dengan Flutter

### HTTP Client Setup

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class KuisApiService {
  // Gunakan live API URL
  static const String baseUrl = 'https://kuis-trivia-api-263444552508.asia-southeast2.run.app';
  // Atau untuk development lokal: 'http://localhost:8000'
  
  Future<Map<String, dynamic>> getSoal({
    String? kategori,
    int jumlah = 10
  }) async {
    String url = '$baseUrl/soal?jumlah=$jumlah';
    if (kategori != null) {
      url += '&kategori=$kategori';
    }
    
    final response = await http.get(Uri.parse(url));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load soal');
    }
  }
  
  Future<List<String>> getKategori() async {
    final response = await http.get(Uri.parse('$baseUrl/kategori'));
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return List<String>.from(data['kategori']);
    } else {
      throw Exception('Failed to load kategori');
    }
  }

  Future<Map<String, dynamic>> getApiInfo() async {
    final response = await http.get(Uri.parse('$baseUrl/'));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load API info');
    }
  }
}
```

### Model Class Flutter

```dart
class Soal {
  final String id;
  final String pertanyaan;
  final List<String> pilihan;
  final String jawaban;
  final String kategori;

  Soal({
    required this.id,
    required this.pertanyaan,
    required this.pilihan,
    required this.jawaban,
    required this.kategori,
  });

  factory Soal.fromJson(Map<String, dynamic> json) {
    return Soal(
      id: json['id'],
      pertanyaan: json['pertanyaan'],
      pilihan: List<String>.from(json['pilihan']),
      jawaban: json['jawaban'],
      kategori: json['kategori'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'pertanyaan': pertanyaan,
      'pilihan': pilihan,
      'jawaban': jawaban,
      'kategori': kategori,
    };
  }
}

class KuisResponse {
  final List<Soal> soal;
  final int total;
  final String? kategori;
  final int jumlah;

  KuisResponse({
    required this.soal,
    required this.total,
    this.kategori,
    required this.jumlah,
  });

  factory KuisResponse.fromJson(Map<String, dynamic> json) {
    return KuisResponse(
      soal: (json['soal'] as List)
          .map((item) => Soal.fromJson(item))
          .toList(),
      total: json['total'],
      kategori: json['kategori'],
      jumlah: json['jumlah'],
    );
  }
}
```

### Contoh Penggunaan di Flutter

```dart
class QuizScreen extends StatefulWidget {
  @override
  _QuizScreenState createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  final KuisApiService _apiService = KuisApiService();
  List<Soal> _soalList = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadSoal();
  }

  Future<void> _loadSoal() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final response = await _apiService.getSoal(
        kategori: 'geografi',
        jumlah: 5
      );
      
      final kuisResponse = KuisResponse.fromJson(response);
      setState(() {
        _soalList = kuisResponse.soal;
        _isLoading = false;
      });
    } catch (e) {
      print('Error loading soal: $e');
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Kuis Trivia'),
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _soalList.length,
              itemBuilder: (context, index) {
                final soal = _soalList[index];
                return Card(
                  margin: EdgeInsets.all(8.0),
                  child: Padding(
                    padding: EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          soal.pertanyaan,
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        SizedBox(height: 12),
                        ...soal.pilihan.map((pilihan) => 
                          ListTile(
                            title: Text(pilihan),
                            leading: Radio(
                              value: pilihan,
                              groupValue: null, // Handle selection logic
                              onChanged: (value) {
                                // Handle answer selection
                              },
                            ),
                          ),
                        ).toList(),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
```

## 🗂️ Struktur Project

```
kuis-trivia-api/
├── main.py                     # Entry point aplikasi
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── run_local.py               # Script untuk menjalankan lokal
├── docker_build_run.py        # Script Docker helper
├── setup_cloud_build.py       # Setup Cloud Build
├── README.md                  # Dokumentasi
├── CLOUD_BUILD_SETUP.md       # Panduan Cloud Build
├── cloudbuild.yaml            # Cloud Build config (production)
├── cloudbuild-staging.yaml    # Cloud Build config (staging)
└── app/
    ├── __init__.py
    ├── services.py            # Business logic
    ├── data/
    │   └── soal_data.json     # Data soal kuis
    ├── models/
    │   ├── __init__.py
    │   └── soal.py            # Data models
    └── routers/
        ├── __init__.py
        ├── soal.py            # Soal endpoints
        └── kategori.py        # Kategori endpoints
```

## 🧪 Testing API

### Menggunakan curl

```bash
# Test dasar
curl -X GET "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/"

# Test dengan pretty print JSON
curl -X GET "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?jumlah=2" | python -m json.tool
```

### Menggunakan Python

```python
import requests

# Base URL
BASE_URL = "https://kuis-trivia-api-263444552508.asia-southeast2.run.app"

# Test API info
response = requests.get(f"{BASE_URL}/")
print("API Info:", response.json())

# Test kategori
response = requests.get(f"{BASE_URL}/kategori")
print("Kategori:", response.json())

# Test soal
response = requests.get(f"{BASE_URL}/soal", params={"kategori": "sains", "jumlah": 3})
print("Soal Sains:", response.json())
```

### Menggunakan JavaScript

```javascript
// Fetch API info
fetch('https://kuis-trivia-api-263444552508.asia-southeast2.run.app/')
  .then(response => response.json())
  .then(data => console.log('API Info:', data));

// Fetch soal
fetch('https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?kategori=geografi&jumlah=5')
  .then(response => response.json())
  .then(data => console.log('Soal Geografi:', data));
```

## ⚙️ Konfigurasi

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Port server |
| `HOST` | `0.0.0.0` | Host binding |
| `ENV` | `development` | Environment mode |

### CORS Settings

API sudah dikonfigurasi untuk menerima request dari semua origin untuk kemudahan development dan integrasi dengan aplikasi mobile.

## 🔧 Troubleshooting

### Common Issues

1. **CORS Error di Browser**
   - API sudah dikonfigurasi CORS untuk semua origin
   - Pastikan menggunakan HTTPS untuk live API

2. **Connection Timeout**
   - Live API mungkin cold start (tunggu beberapa detik)
   - Untuk production, consider using Cloud Run min instances

3. **Rate Limiting**
   - Saat ini tidak ada rate limiting
   - Gunakan dengan bijak untuk menghindari abuse

### Health Check

```bash
# Check status API
curl "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/health"
```

## 📄 License

MIT License - lihat file LICENSE untuk detail lengkap.

## 🤝 Contributing

1. Fork repository
2. Buat feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

Jika ada pertanyaan atau masalah:
- Buka issue di GitHub repository
- Check dokumentasi interaktif di `/docs`
- Review kode untuk memahami implementasi

---

**🎉 Selamat menggunakan Kuis Trivia API!**

**API sudah live dan siap digunakan untuk project Flutter Anda!** ✨

Dibuat dengan ❤️ menggunakan FastAPI dan Google Cloud Run.