"""Entidades de dominio para trabajos de conversión."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class ConversionStatus(str, Enum):
    """Estados posibles de un trabajo de conversión."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class FileJob:
    """Representa un archivo individual dentro de un trabajo de conversión."""
    
    file_id: UUID
    file_name: str
    source_path: str
    destination_path: str
    status: ConversionStatus = ConversionStatus.PENDING
    progress: int = 0  # 0-100
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def start(self) -> None:
        """Inicia la conversión del archivo."""
        self.status = ConversionStatus.IN_PROGRESS
        self.started_at = datetime.now()
    
    def complete(self) -> None:
        """Marca la conversión como completada."""
        self.status = ConversionStatus.COMPLETED
        self.progress = 100
        self.completed_at = datetime.now()
    
    def fail(self, error: str) -> None:
        """Marca la conversión como fallida."""
        self.status = ConversionStatus.FAILED
        self.error_message = error
        self.completed_at = datetime.now()
    
    def cancel(self) -> None:
        """Marca la conversión como cancelada."""
        self.status = ConversionStatus.CANCELLED
        self.completed_at = datetime.now()


@dataclass
class ConversionJob:
    """Entidad de dominio que representa un trabajo de conversión por lotes."""
    
    id: UUID = field(default_factory=uuid4)
    files: list[FileJob] = field(default_factory=list)
    status: ConversionStatus = ConversionStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    @property
    def total_files(self) -> int:
        """Total de archivos en el trabajo."""
        return len(self.files)
    
    @property
    def completed_count(self) -> int:
        """Cantidad de archivos completados."""
        return sum(1 for f in self.files if f.status == ConversionStatus.COMPLETED)
    
    @property
    def failed_count(self) -> int:
        """Cantidad de archivos fallidos."""
        return sum(1 for f in self.files if f.status == ConversionStatus.FAILED)
    
    @property
    def remaining_count(self) -> int:
        """Cantidad de archivos pendientes."""
        return sum(
            1 for f in self.files 
            if f.status in [ConversionStatus.PENDING, ConversionStatus.IN_PROGRESS]
        )
    
    @property
    def current_file(self) -> Optional[FileJob]:
        """Archivo actualmente en conversión."""
        for file_job in self.files:
            if file_job.status == ConversionStatus.IN_PROGRESS:
                return file_job
        return None
    
    @property
    def overall_progress(self) -> int:
        """Progreso general del trabajo (0-100)."""
        if not self.files:
            return 0
        total_progress = sum(f.progress for f in self.files)
        return total_progress // len(self.files)
    
    def add_file(self, file_job: FileJob) -> None:
        """Agrega un archivo al trabajo."""
        if len(self.files) >= 100:
            raise ValueError("Máximo 100 archivos por trabajo de conversión")
        self.files.append(file_job)
    
    def start(self) -> None:
        """Inicia el trabajo de conversión."""
        self.status = ConversionStatus.IN_PROGRESS
        self.started_at = datetime.now()
    
    def complete(self) -> None:
        """Marca el trabajo como completado."""
        self.status = ConversionStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def cancel(self) -> None:
        """Cancela el trabajo."""
        self.status = ConversionStatus.CANCELLED
        self.completed_at = datetime.now()
        # Cancelar todos los archivos pendientes
        for file_job in self.files:
            if file_job.status in [ConversionStatus.PENDING, ConversionStatus.IN_PROGRESS]:
                file_job.cancel()
