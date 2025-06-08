from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import soal_router, kategori_router

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="Kuis Trivia API",
    description="API untuk menyediakan soal kuis trivia berbahasa Indonesia",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Konfigurasi CORS untuk Flutter dan aplikasi web lainnya
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Untuk production, ganti dengan domain spesifik
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrasi router
app.include_router(soal_router)
app.include_router(kategori_router)

@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint root untuk memeriksa status API
    """
    return {
        "pesan": "Selamat datang di Kuis Trivia API",
        "versi": "1.0.0",
        "dokumentasi": "/docs",
        "status": "aktif"
    }

@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Endpoint untuk health check
    """
    return {"status": "sehat", "pesan": "API berjalan dengan baik"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
