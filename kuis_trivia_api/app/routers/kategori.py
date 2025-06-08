from fastapi import APIRouter
from app.models import KategoriResponse
from app.services import soal_service

router = APIRouter(prefix="/kategori", tags=["Kategori"])

@router.get("/", response_model=KategoriResponse, summary="Ambil Daftar Kategori")
async def get_kategori():
    """
    Mengambil daftar semua kategori soal yang tersedia.
    
    Returns:
        List kategori soal yang ada dalam database
    """
    categories = soal_service.get_categories()
    return KategoriResponse(kategori=categories)
