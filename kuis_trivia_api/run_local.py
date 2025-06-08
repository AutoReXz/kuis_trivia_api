#!/usr/bin/env python3
"""
Script untuk menjalankan Kuis Trivia API secara lokal
"""

import uvicorn
import sys
import os

def main():
    # Pastikan working directory benar
    if not os.path.exists('main.py'):
        print("❌ Error: File main.py tidak ditemukan!")
        print("   Pastikan Anda menjalankan script ini dari folder root project.")
        sys.exit(1)
    
    print("🚀 Memulai Kuis Trivia API...")
    print("📍 URL API: http://localhost:8000")
    print("📚 Dokumentasi: http://localhost:8000/docs")
    print("🔄 Auto-reload: Aktif")
    print("⏹️  Tekan Ctrl+C untuk menghentikan server")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server dihentikan. Terima kasih!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
