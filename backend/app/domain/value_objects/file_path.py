"""Value object para rutas de archivo."""
from dataclasses import dataclass
import os


MAX_PATH_LENGTH = 4096


@dataclass(frozen=True)
class FilePath:
    """Value object inmutable para representar rutas de archivo."""
    
    path: str
    
    def __post_init__(self):
        """Validaciones de la ruta."""
        if not self.path:
            raise ValueError("La ruta no puede estar vacía")
        if len(self.path) > MAX_PATH_LENGTH:
            raise ValueError(
                f"La ruta excede el máximo de {MAX_PATH_LENGTH} caracteres: {len(self.path)}"
            )
    
    @property
    def name(self) -> str:
        """Nombre del archivo."""
        return os.path.basename(self.path)
    
    @property
    def directory(self) -> str:
        """Directorio padre."""
        return os.path.dirname(self.path)
    
    @property
    def extension(self) -> str:
        """Extensión del archivo."""
        _, ext = os.path.splitext(self.path)
        return ext.lower()
    
    @property
    def is_mp4(self) -> bool:
        """Verifica si es un archivo MP4."""
        return self.extension == ".mp4"
    
    @property
    def is_avi(self) -> bool:
        """Verifica si es un archivo AVI."""
        return self.extension == ".avi"
    
    def with_extension(self, new_extension: str) -> "FilePath":
        """Retorna una nueva ruta con diferente extensión."""
        base, _ = os.path.splitext(self.path)
        ext = new_extension if new_extension.startswith(".") else f".{new_extension}"
        return FilePath(f"{base}{ext}")
    
    def __str__(self) -> str:
        return self.path
