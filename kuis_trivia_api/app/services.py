import json
import random
from typing import List, Optional
from uuid import UUID
from pathlib import Path
from app.models import Soal, SoalCreate

class SoalService:
    def __init__(self, data_file: str = "app/data/soal_data.json"):
        self.data_file = Path(data_file)
        self._load_data()
    
    def _load_data(self):
        """Memuat data soal dari file JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Convert string IDs back to UUID objects
                for item in data:
                    if isinstance(item['id'], str):
                        item['id'] = UUID(item['id'])
                self.soal_list = [Soal(**item) for item in data]
        except FileNotFoundError:
            self.soal_list = []
    
    def _save_data(self):
        """Menyimpan data soal ke file JSON"""
        data = [soal.dict() for soal in self.soal_list]
        # Convert UUID to string for JSON serialization
        for item in data:
            item['id'] = str(item['id'])
        
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    
    def get_all_soal(self, kategori: Optional[str] = None, jumlah: int = 10) -> List[Soal]:
        """Mengambil daftar soal dengan filter kategori dan jumlah"""
        if kategori:
            filtered_soal = [soal for soal in self.soal_list if soal.kategori.lower() == kategori.lower()]
        else:
            filtered_soal = self.soal_list
        
        # Randomize dan ambil sesuai jumlah yang diminta
        if len(filtered_soal) > jumlah:
            return random.sample(filtered_soal, jumlah)
        else:
            return filtered_soal
    
    def get_soal_by_id(self, soal_id: UUID) -> Optional[Soal]:
        """Mengambil soal berdasarkan ID"""
        for soal in self.soal_list:
            if soal.id == soal_id:
                return soal
        return None
    
    def create_soal(self, soal_data: SoalCreate) -> Soal:
        """Membuat soal baru"""
        # Validasi jawaban harus ada dalam pilihan
        if soal_data.jawaban not in soal_data.pilihan:
            raise ValueError("Jawaban harus merupakan salah satu dari pilihan yang tersedia")
        
        new_soal = Soal(**soal_data.dict())
        self.soal_list.append(new_soal)
        self._save_data()
        return new_soal
    
    def delete_soal(self, soal_id: UUID) -> bool:
        """Menghapus soal berdasarkan ID"""
        for i, soal in enumerate(self.soal_list):
            if soal.id == soal_id:
                del self.soal_list[i]
                self._save_data()
                return True
        return False
    
    def get_categories(self) -> List[str]:
        """Mengambil daftar kategori yang tersedia"""
        categories = list(set(soal.kategori for soal in self.soal_list))
        return sorted(categories)

# Singleton instance
soal_service = SoalService()
