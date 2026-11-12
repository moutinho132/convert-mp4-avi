"""Entidad de dominio que representa un archivo MP4."""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class FileEntity:
    """Entidad de dominio que representa un archivo MP4."""
    
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    path: str = ""
    size: int = 0  # bytes
    last_modified: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validaciones de dominio."""
        if not self.name:
            raise ValueError("El nombre del archivo es requerido")
        if self.size < 0:
            raise ValueError("El tamaño del archivo no puede ser negativo")
    
    @property
    def extension(self) -> str:
        """Retorna la extensión del archivo."""
        return self.name.rsplit(".", 1)[-1].lower() if "." in self.name else ""
    
    @property
    def is_mp4(self) -> bool:
        """Verifica si el archivo es MP4."""
        return self.extension == "mp4"
    
    def to_dict(self) -> dict:
        """Serializa la entidad a diccionario."""
        return {
            "id": str(self.id),
            "name": self.name,
            "path": self.path,
            "size": self.size,
            "last_modified": self.last_modified.isoformat()
        }
