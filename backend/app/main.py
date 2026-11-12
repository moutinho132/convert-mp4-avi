"""
Punto de entrada de la aplicación FastAPI.
Sistema Conversor de MP4 a AVI.
"""
from fastapi import FastAPI


def create_app() -> FastAPI:
    """Factory function para crear la aplicación FastAPI."""
    app = FastAPI(
        title="MP4 to AVI Converter",
        description="API para conversión de archivos de video MP4 a AVI",
        version="1.0.0",
    )
    
    return app


app = create_app()


@app.get("/health")
async def health_check():
    """Endpoint de health check."""
    return {"status": "healthy"}
