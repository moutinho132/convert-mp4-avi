"""
Configuración de la aplicación usando Pydantic Settings.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación."""
    
    app_name: str = "MP4 to AVI Converter"
    debug: bool = False
    
    # Paths por defecto
    default_source_path: str = "/source"
    default_destination_path: str = "/dest"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"


settings = Settings()
