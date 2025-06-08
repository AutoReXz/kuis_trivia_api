from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

class SoalBase(BaseModel):
    pertanyaan: str = Field(..., description="Pertanyaan kuis")
    pilihan: List[str] = Field(..., min_items=3, description="Pilihan jawaban (minimal 3)")
    jawaban: str = Field(..., description="Jawaban benar")
    kategori: str = Field(..., description="Kategori soal")

class SoalCreate(SoalBase):
    pass

class Soal(SoalBase):
    id: UUID = Field(default_factory=uuid4, description="ID unik soal")
    
    class Config:
        from_attributes = True

class SoalResponse(BaseModel):
    id: UUID
    pertanyaan: str
    pilihan: List[str]
    jawaban: str
    kategori: str

class SoalListResponse(BaseModel):
    soal: List[SoalResponse]
    total: int
    kategori: Optional[str] = None
    jumlah: int

class KategoriResponse(BaseModel):
    kategori: List[str]

class MessageResponse(BaseModel):
    pesan: str
