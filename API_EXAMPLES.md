# API Usage Examples

Contoh penggunaan praktis Kuis Trivia API untuk berbagai kebutuhan development.

🌐 **Base URL**: https://kuis-trivia-api-263444552508.asia-southeast2.run.app

## 📋 Quick Examples

- [Testing dengan curl](#testing-dengan-curl)
- [Integrasi Python](#integrasi-python)
- [Integrasi JavaScript](#integrasi-javascript)
- [Integrasi Flutter](#integrasi-flutter)

## 🔧 curl Examples

### Basic API Info
```bash
# Get API information
curl -X GET "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/" \
  -H "accept: application/json"
```

### Health Check
```bash
# Check API health status
curl -X GET "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/health" \
  -H "accept: application/json"
```

### Get Categories
```bash
# Get all available categories
curl -X GET "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/kategori" \
  -H "accept: application/json"
```

### Get Questions
```bash
# Get 5 random questions from all categories
curl -X GET "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?jumlah=5" \
  -H "accept: application/json"

# Get 3 geography questions
curl -X GET "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?kategori=geografi&jumlah=3" \
  -H "accept: application/json"

# Get 10 science questions (maximum)
curl -X GET "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?kategori=sains&jumlah=10" \
  -H "accept: application/json"

# Get 2 history questions
curl -X GET "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?kategori=sejarah&jumlah=2" \
  -H "accept: application/json"

# Get 5 general knowledge questions
curl -X GET "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?kategori=umum&jumlah=5" \
  -H "accept: application/json"
```

### Pretty Print JSON (Linux/Mac)
```bash
# Pretty print JSON response
curl -X GET "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?jumlah=2" | jq '.'
```

### Pretty Print JSON (Windows/PowerShell)
```powershell
# Pretty print JSON response
Invoke-RestMethod -Uri "https://kuis-trivia-api-263444552508.asia-southeast2.run.app/soal?jumlah=2" | ConvertTo-Json -Depth 10
```

## 🐍 Python Examples

### Basic Usage with requests
```python
import requests
import json
from typing import List, Dict, Optional

class KuisTriviaAPI:
    def __init__(self, base_url: str = "https://kuis-trivia-api-263444552508.asia-southeast2.run.app"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'KuisTriviaClient/1.0'
        })
    
    def get_api_info(self) -> Dict:
        """Get API information."""
        response = self.session.get(f"{self.base_url}/")
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict:
        """Check API health status."""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def get_categories(self) -> List[str]:
        """Get all available categories."""
        response = self.session.get(f"{self.base_url}/kategori")
        response.raise_for_status()
        return response.json()["kategori"]
    
    def get_questions(self, kategori: Optional[str] = None, jumlah: int = 10) -> Dict:
        """
        Get quiz questions.
        
        Args:
            kategori: Category filter (geografi, sains, sejarah, umum)
            jumlah: Number of questions (max 50)
        
        Returns:
            Dict containing questions and metadata
        """
        params = {"jumlah": jumlah}
        if kategori:
            params["kategori"] = kategori
        
        response = self.session.get(f"{self.base_url}/soal", params=params)
        response.raise_for_status()
        return response.json()

# Usage example
if __name__ == "__main__":
    api = KuisTriviaAPI()
    
    # Test API connection
    try:
        info = api.get_api_info()
        print("🎉 API Info:", json.dumps(info, indent=2, ensure_ascii=False))
        
        # Get categories
        categories = api.get_categories()
        print(f"\n📚 Available Categories: {categories}")
        
        # Get random questions
        questions = api.get_questions(jumlah=3)
        print(f"\n❓ Random Questions: {len(questions['soal'])} questions loaded")
        
        # Get category-specific questions
        geo_questions = api.get_questions(kategori="geografi", jumlah=2)
        print(f"\n🌍 Geography Questions: {len(geo_questions['soal'])} questions loaded")
        
        # Print first question
        if geo_questions['soal']:
            q = geo_questions['soal'][0]
            print(f"\n📝 Sample Question:")
            print(f"   Question: {q['pertanyaan']}")
            print(f"   Options: {q['pilihan']}")
            print(f"   Answer: {q['jawaban']}")
            print(f"   Category: {q['kategori']}")
            
    except requests.RequestException as e:
        print(f"❌ Error: {e}")
```

### Async Python with aiohttp
```python
import aiohttp
import asyncio
import json
from typing import List, Dict, Optional

class AsyncKuisTriviaAPI:
    def __init__(self, base_url: str = "https://kuis-trivia-api-263444552508.asia-southeast2.run.app"):
        self.base_url = base_url
    
    async def _request(self, session: aiohttp.ClientSession, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make async HTTP request."""
        async with session.get(f"{self.base_url}{endpoint}", params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get_questions(self, kategori: Optional[str] = None, jumlah: int = 10) -> Dict:
        """Get quiz questions asynchronously."""
        params = {"jumlah": jumlah}
        if kategori:
            params["kategori"] = kategori
        
        async with aiohttp.ClientSession() as session:
            return await self._request(session, "/soal", params)
    
    async def get_categories(self) -> List[str]:
        """Get categories asynchronously."""
        async with aiohttp.ClientSession() as session:
            data = await self._request(session, "/kategori")
            return data["kategori"]

# Usage example
async def main():
    api = AsyncKuisTriviaAPI()
    
    # Concurrent requests
    tasks = [
        api.get_questions(kategori="geografi", jumlah=2),
        api.get_questions(kategori="sains", jumlah=2),
        api.get_categories()
    ]
    
    geo_questions, science_questions, categories = await asyncio.gather(*tasks)
    
    print(f"📚 Categories: {categories}")
    print(f"🌍 Geography questions: {len(geo_questions['soal'])}")
    print(f"🔬 Science questions: {len(science_questions['soal'])}")

# Run async example
# asyncio.run(main())
```

## 🌐 JavaScript/Node.js Examples

### Using fetch (Modern JavaScript)
```javascript
class KuisTriviaAPI {
    constructor(baseUrl = 'https://kuis-trivia-api-263444552508.asia-southeast2.run.app') {
        this.baseUrl = baseUrl;
    }
    
    async request(endpoint, params = {}) {
        const url = new URL(endpoint, this.baseUrl);
        Object.keys(params).forEach(key => 
            params[key] && url.searchParams.append(key, params[key])
        );
        
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }
    
    async getApiInfo() {
        return await this.request('/');
    }
    
    async getCategories() {
        const data = await this.request('/kategori');
        return data.kategori;
    }
    
    async getQuestions(kategori = null, jumlah = 10) {
        return await this.request('/soal', { kategori, jumlah });
    }
}

// Usage example
(async () => {
    try {
        const api = new KuisTriviaAPI();
        
        // Get API info
        const info = await api.getApiInfo();
        console.log('🎉 API Info:', info);
        
        // Get categories
        const categories = await api.getCategories();
        console.log('📚 Categories:', categories);
        
        // Get random questions
        const questions = await api.getQuestions(null, 5);
        console.log(`❓ Got ${questions.soal.length} random questions`);
        
        // Get geography questions
        const geoQuestions = await api.getQuestions('geografi', 3);
        console.log(`🌍 Got ${geoQuestions.soal.length} geography questions`);
        
        // Display first question
        if (geoQuestions.soal.length > 0) {
            const q = geoQuestions.soal[0];
            console.log('\n📝 Sample Question:');
            console.log(`   Question: ${q.pertanyaan}`);
            console.log(`   Options: ${q.pilihan.join(', ')}`);
            console.log(`   Answer: ${q.jawaban}`);
            console.log(`   Category: ${q.kategori}`);
        }
        
    } catch (error) {
        console.error('❌ Error:', error.message);
    }
})();
```

### Using axios (Node.js)
```javascript
const axios = require('axios');

class KuisTriviaAPIClient {
    constructor(baseUrl = 'https://kuis-trivia-api-263444552508.asia-southeast2.run.app') {
        this.client = axios.create({
            baseURL: baseUrl,
            timeout: 10000,
            headers: {
                'Content-Type': 'application/json',
                'User-Agent': 'KuisTriviaClient/1.0'
            }
        });
    }
    
    async getQuestions(kategori = null, jumlah = 10) {
        try {
            const params = { jumlah };
            if (kategori) params.kategori = kategori;
            
            const response = await this.client.get('/soal', { params });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get questions: ${error.message}`);
        }
    }
    
    async getAllCategoryQuestions() {
        const categories = await this.getCategories();
        const promises = categories.map(kategori => 
            this.getQuestions(kategori, 2)
        );
        
        const results = await Promise.all(promises);
        
        return categories.reduce((acc, kategori, index) => {
            acc[kategori] = results[index];
            return acc;
        }, {});
    }
    
    async getCategories() {
        const response = await this.client.get('/kategori');
        return response.data.kategori;
    }
}

// Usage
(async () => {
    const api = new KuisTriviaAPIClient();
    
    try {
        // Get all questions by category
        const allQuestions = await api.getAllCategoryQuestions();
        
        Object.entries(allQuestions).forEach(([kategori, data]) => {
            console.log(`\n📚 ${kategori.toUpperCase()} (${data.soal.length} questions):`);
            data.soal.forEach((q, i) => {
                console.log(`  ${i + 1}. ${q.pertanyaan}`);
            });
        });
        
    } catch (error) {
        console.error('❌ Error:', error.message);
    }
})();
```

## 📱 Flutter/Dart Examples

### Complete API Service
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiException implements Exception {
  final String message;
  final int? statusCode;
  
  ApiException(this.message, [this.statusCode]);
  
  @override
  String toString() => 'ApiException: $message (Status: $statusCode)';
}

class KuisTriviaApiService {
  static const String _baseUrl = 'https://kuis-trivia-api-263444552508.asia-southeast2.run.app';
  final http.Client _client;
  
  KuisTriviaApiService({http.Client? client}) : _client = client ?? http.Client();
  
  Future<Map<String, dynamic>> _request(
    String endpoint, {
    Map<String, String>? queryParams,
  }) async {
    final uri = Uri.parse('$_baseUrl$endpoint').replace(
      queryParameters: queryParams,
    );
    
    try {
      final response = await _client.get(
        uri,
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'KuisTriviaFlutterClient/1.0',
        },
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body) as Map<String, dynamic>;
      } else {
        throw ApiException(
          'Request failed with status ${response.statusCode}',
          response.statusCode,
        );
      }
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException('Network error: $e');
    }
  }
  
  Future<Map<String, dynamic>> getApiInfo() async {
    return await _request('/');
  }
  
  Future<List<String>> getCategories() async {
    final response = await _request('/kategori');
    return List<String>.from(response['kategori']);
  }
  
  Future<KuisResponse> getQuestions({
    String? kategori,
    int jumlah = 10,
  }) async {
    final queryParams = <String, String>{
      'jumlah': jumlah.toString(),
    };
    
    if (kategori != null) {
      queryParams['kategori'] = kategori;
    }
    
    final response = await _request('/soal', queryParams: queryParams);
    return KuisResponse.fromJson(response);
  }
  
  Future<Map<String, dynamic>> healthCheck() async {
    return await _request('/health');
  }
  
  void dispose() {
    _client.close();
  }
}

// Models
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
      id: json['id'] as String,
      pertanyaan: json['pertanyaan'] as String,
      pilihan: List<String>.from(json['pilihan']),
      jawaban: json['jawaban'] as String,
      kategori: json['kategori'] as String,
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
          .map((item) => Soal.fromJson(item as Map<String, dynamic>))
          .toList(),
      total: json['total'] as int,
      kategori: json['kategori'] as String?,
      jumlah: json['jumlah'] as int,
    );
  }
}

// Usage example in Flutter widget
class QuizService {
  final KuisTriviaApiService _apiService;
  
  QuizService() : _apiService = KuisTriviaApiService();
  
  Future<List<Soal>> loadQuiz(String kategori, int questionCount) async {
    try {
      final response = await _apiService.getQuestions(
        kategori: kategori,
        jumlah: questionCount,
      );
      return response.soal;
    } on ApiException catch (e) {
      print('API Error: $e');
      rethrow;
    } catch (e) {
      print('Unexpected error: $e');
      throw ApiException('Failed to load quiz questions');
    }
  }
  
  Future<List<String>> getAvailableCategories() async {
    return await _apiService.getCategories();
  }
  
  void dispose() {
    _apiService.dispose();
  }
}
```

### Flutter Widget Example
```dart
import 'package:flutter/material.dart';

class QuizScreen extends StatefulWidget {
  final String kategori;
  
  const QuizScreen({Key? key, required this.kategori}) : super(key: key);

  @override
  _QuizScreenState createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  final QuizService _quizService = QuizService();
  List<Soal> _questions = [];
  bool _isLoading = true;
  String? _error;
  int _currentQuestionIndex = 0;
  String? _selectedAnswer;
  int _score = 0;

  @override
  void initState() {
    super.initState();
    _loadQuestions();
  }

  Future<void> _loadQuestions() async {
    try {
      setState(() {
        _isLoading = true;
        _error = null;
      });

      final questions = await _quizService.loadQuiz(widget.kategori, 10);
      
      setState(() {
        _questions = questions;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  void _selectAnswer(String answer) {
    setState(() {
      _selectedAnswer = answer;
    });
  }

  void _nextQuestion() {
    if (_selectedAnswer == _questions[_currentQuestionIndex].jawaban) {
      _score++;
    }

    if (_currentQuestionIndex < _questions.length - 1) {
      setState(() {
        _currentQuestionIndex++;
        _selectedAnswer = null;
      });
    } else {
      _showResults();
    }
  }

  void _showResults() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        title: Text('Quiz Completed! 🎉'),
        content: Text(
          'Your Score: $_score/${_questions.length}\n'
          'Accuracy: ${((_score / _questions.length) * 100).toStringAsFixed(1)}%'
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              Navigator.of(context).pop();
            },
            child: Text('Back to Menu'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              _restartQuiz();
            },
            child: Text('Play Again'),
          ),
        ],
      ),
    );
  }

  void _restartQuiz() {
    setState(() {
      _currentQuestionIndex = 0;
      _selectedAnswer = null;
      _score = 0;
    });
    _loadQuestions();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Quiz ${widget.kategori.toUpperCase()}'),
        backgroundColor: Colors.blue,
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(),
            SizedBox(height: 16),
            Text('Loading questions...'),
          ],
        ),
      );
    }

    if (_error != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.error, size: 64, color: Colors.red),
            SizedBox(height: 16),
            Text('Error: $_error'),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: _loadQuestions,
              child: Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (_questions.isEmpty) {
      return Center(
        child: Text('No questions available for this category.'),
      );
    }

    final currentQuestion = _questions[_currentQuestionIndex];

    return Padding(
      padding: EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Progress indicator
          LinearProgressIndicator(
            value: (_currentQuestionIndex + 1) / _questions.length,
            backgroundColor: Colors.grey[300],
            valueColor: AlwaysStoppedAnimation<Color>(Colors.blue),
          ),
          SizedBox(height: 16),
          
          // Question counter
          Text(
            'Question ${_currentQuestionIndex + 1} of ${_questions.length}',
            style: TextStyle(fontSize: 16, color: Colors.grey[600]),
          ),
          SizedBox(height: 24),
          
          // Question
          Card(
            child: Padding(
              padding: EdgeInsets.all(16.0),
              child: Text(
                currentQuestion.pertanyaan,
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ),
          ),
          SizedBox(height: 24),
          
          // Answer options
          Expanded(
            child: ListView.builder(
              itemCount: currentQuestion.pilihan.length,
              itemBuilder: (context, index) {
                final option = currentQuestion.pilihan[index];
                final isSelected = option == _selectedAnswer;
                
                return Padding(
                  padding: EdgeInsets.only(bottom: 12.0),
                  child: ElevatedButton(
                    onPressed: () => _selectAnswer(option),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: isSelected ? Colors.blue : Colors.grey[200],
                      foregroundColor: isSelected ? Colors.white : Colors.black,
                      padding: EdgeInsets.all(16.0),
                    ),
                    child: Text(
                      option,
                      style: TextStyle(fontSize: 16),
                    ),
                  ),
                );
              },
            ),
          ),
          
          // Next button
          ElevatedButton(
            onPressed: _selectedAnswer != null ? _nextQuestion : null,
            style: ElevatedButton.styleFrom(
              padding: EdgeInsets.all(16.0),
              backgroundColor: Colors.green,
            ),
            child: Text(
              _currentQuestionIndex == _questions.length - 1 ? 'Finish' : 'Next',
              style: TextStyle(fontSize: 18),
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _quizService.dispose();
    super.dispose();
  }
}
```

## 📮 Postman Collection

### Collection JSON
```json
{
  "info": {
    "name": "Kuis Trivia API",
    "description": "Complete collection for Kuis Trivia API endpoints",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "baseUrl",
      "value": "https://kuis-trivia-api-263444552508.asia-southeast2.run.app",
      "type": "string"
    }
  ],
  "item": [
    {
      "name": "API Info",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{baseUrl}}/",
          "host": ["{{baseUrl}}"],
          "path": [""]
        }
      }
    },
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{baseUrl}}/health",
          "host": ["{{baseUrl}}"],
          "path": ["health"]
        }
      }
    },
    {
      "name": "Get Categories",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{baseUrl}}/kategori",
          "host": ["{{baseUrl}}"],
          "path": ["kategori"]
        }
      }
    },
    {
      "name": "Get Random Questions",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{baseUrl}}/soal?jumlah=5",
          "host": ["{{baseUrl}}"],
          "path": ["soal"],
          "query": [
            {
              "key": "jumlah",
              "value": "5"
            }
          ]
        }
      }
    },
    {
      "name": "Get Geography Questions",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{baseUrl}}/soal?kategori=geografi&jumlah=3",
          "host": ["{{baseUrl}}"],
          "path": ["soal"],
          "query": [
            {
              "key": "kategori",
              "value": "geografi"
            },
            {
              "key": "jumlah",
              "value": "3"
            }
          ]
        }
      }
    }
  ]
}
```

## 📊 Response Examples

### GET / (API Info)
```json
{
  "pesan": "Selamat datang di Kuis Trivia API",
  "versi": "1.0.0",
  "dokumentasi": "/docs",
  "status": "aktif"
}
```

### GET /kategori (Categories)
```json
{
  "kategori": ["geografi", "sains", "sejarah", "umum"]
}
```

### GET /soal (Questions)
```json
{
  "soal": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "pertanyaan": "Ibu kota Indonesia adalah?",
      "pilihan": ["Jakarta", "Surabaya", "Bandung", "Medan"],
      "jawaban": "Jakarta",
      "kategori": "geografi"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "pertanyaan": "Planet terdekat dengan matahari adalah?",
      "pilihan": ["Venus", "Merkurius", "Mars", "Bumi"],
      "jawaban": "Merkurius",
      "kategori": "sains"
    }
  ],
  "total": 2,
  "kategori": null,
  "jumlah": 2
}
```

### Error Response Example
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["query", "jumlah"],
      "msg": "ensure this value is less than or equal to 50",
      "input": "100",
      "ctx": {"limit_value": 50}
    }
  ]
}
```

---

**💡 Tips:**
- Semua endpoint mendukung CORS untuk integrasi web/mobile
- Parameter `jumlah` maksimal adalah 50
- API menggunakan cold start di Google Cloud Run, jadi request pertama mungkin lambat
- Gunakan connection pooling untuk performa yang lebih baik
- API rate limiting belum diimplementasi, gunakan dengan bijak

**🔗 Links:**
- [API Documentation](https://kuis-trivia-api-263444552508.asia-southeast2.run.app/docs)
- [GitHub Repository](https://github.com/your-username/kuis-trivia-api)
- [Report Issues](https://github.com/your-username/kuis-trivia-api/issues)
