from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from uuid import UUID
from app.models import SoalResponse, SoalListResponse, SoalCreate, KategoriResponse, MessageResponse
from app.services import soal_service

router = APIRouter(prefix="/soal", tags=["Soal Kuis"])

@router.get("/", response_model=SoalListResponse, summary="Ambil Daftar Soal")
async def get_soal(
    kategori: Optional[str] = Query(None, description="Filter berdasarkan kategori"),
    jumlah: int = Query(10, ge=1, le=50, description="Jumlah soal yang diambil (1-50)")
):
    """
    Mengambil daftar soal kuis secara acak.
    
    - **kategori**: Filter soal berdasarkan kategori (opsional)
    - **jumlah**: Jumlah soal yang diinginkan (default: 10, maksimal: 50)
    """
    try:
        soal_list = soal_service.get_all_soal(kategori=kategori, jumlah=jumlah)
        
        soal_response = [
            SoalResponse(
                id=soal.id,
                pertanyaan=soal.pertanyaan,
                pilihan=soal.pilihan,
                jawaban=soal.jawaban,
                kategori=soal.kategori
            ) for soal in soal_list
        ]
        
        return SoalListResponse(
            soal=soal_response,
            total=len(soal_response),
            kategori=kategori,
            jumlah=jumlah
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")

@router.post("/", response_model=SoalResponse, summary="Tambah Soal Baru")
async def create_soal(soal_data: SoalCreate):
    """
    Menambahkan soal kuis baru.
    
    - **pertanyaan**: Pertanyaan kuis
    - **pilihan**: Array pilihan jawaban (minimal 3)
    - **jawaban**: Jawaban yang benar (harus ada dalam pilihan)
    - **kategori**: Kategori soal
    """
    try:
        new_soal = soal_service.create_soal(soal_data)
        return SoalResponse(
            id=new_soal.id,
            pertanyaan=new_soal.pertanyaan,
            pilihan=new_soal.pilihan,
            jawaban=new_soal.jawaban,
            kategori=new_soal.kategori
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")

@router.get("/{soal_id}", response_model=SoalResponse, summary="Ambil Detail Soal")
async def get_soal_by_id(soal_id: UUID):
    """
    Mengambil detail soal berdasarkan ID.
    
    - **soal_id**: ID unik soal
    """
    soal = soal_service.get_soal_by_id(soal_id)
    if not soal:
        raise HTTPException(status_code=404, detail="Soal tidak ditemukan")
    
    return SoalResponse(
        id=soal.id,
        pertanyaan=soal.pertanyaan,
        pilihan=soal.pilihan,
        jawaban=soal.jawaban,
        kategori=soal.kategori
    )

@router.delete("/{soal_id}", response_model=MessageResponse, summary="Hapus Soal")
async def delete_soal(soal_id: UUID):
    """
    Menghapus soal berdasarkan ID.
    
    - **soal_id**: ID unik soal yang akan dihapus
    """
    success = soal_service.delete_soal(soal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Soal tidak ditemukan")
    
    return MessageResponse(pesan="Soal berhasil dihapus")
