# Kuis Trivia API

API REST untuk menyediakan soal kuis trivia berbahasa Indonesia yang dapat diintegrasikan dengan aplikasi Flutter atau aplikasi mobile/web lainnya.

## 📋 Fitur

- ✅ Menyediakan soal kuis trivia berbahasa Indonesia
- ✅ 4 kategori soal: sejarah, geografi, sains, umum
- ✅ Support CORS untuk Flutter dan aplikasi web
- ✅ Dokumentasi Swagger/OpenAPI otomatis
- ✅ Data tersimpan dalam file JSON
- ✅ Docker ready untuk deployment
- ✅ Siap deploy ke Google Cloud Run

## 🚀 Quick Start

### Menjalankan Lokal

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd kuis_trivia_api
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

### Root & Health
- `GET /` - Informasi API
- `GET /health` - Health check

### Soal Kuis
- `GET /soal` - Ambil daftar soal
  - Query params:
    - `kategori` (optional): Filter berdasarkan kategori
    - `jumlah` (optional): Jumlah soal (default: 10, max: 50)
- `POST /soal` - Tambah soal baru
- `GET /soal/{id}` - Ambil detail soal berdasarkan ID
- `DELETE /soal/{id}` - Hapus soal

### Kategori
- `GET /kategori` - Ambil daftar kategori yang tersedia

## 📝 Contoh Penggunaan

### Mengambil 5 soal acak
```bash
curl "http://localhost:8000/soal?jumlah=5"
```

### Mengambil soal kategori sejarah
```bash
curl "http://localhost:8000/soal?kategori=sejarah&jumlah=3"
```

### Menambah soal baru
```bash
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
  static const String baseUrl = 'https://your-cloud-run-url';
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
}
```

---

**Selamat menggunakan Kuis Trivia API!** 🎉

**Project sudah siap digunakan!** Clone, build Docker, dan deploy ke Cloud Run! 🚀
