"""Value object para opciones de conversión de video."""
from dataclasses import dataclass
from enum import Enum


class VideoCodec(str, Enum):
    """Codecs de video soportados para AVI."""
    MPEG4 = "mpeg4"
    XVID = "xvid"
    H264 = "h264"


class AudioCodec(str, Enum):
    """Codecs de audio soportados."""
    MP3 = "mp3"
    AAC = "aac"
    AC3 = "ac3"


@dataclass(frozen=True)
class ConversionOptions:
    """Value object inmutable para opciones de conversión."""
    
    video_codec: VideoCodec = VideoCodec.MPEG4
    audio_codec: AudioCodec = AudioCodec.MP3
    video_bitrate: str = "1500k"  # Bitrate de video por defecto
    audio_bitrate: str = "128k"   # Bitrate de audio por defecto
    quality: int = 23             # Calidad (menor = mejor, escala CRF)
    overwrite: bool = True        # Sobrescribir archivo destino si existe
    
    def __post_init__(self):
        """Validaciones de opciones."""
        if self.quality < 0 or self.quality > 51:
            raise ValueError("La calidad debe estar entre 0 y 51")
    
    def to_ffmpeg_args(self) -> list[str]:
        """Convierte las opciones a argumentos de FFmpeg."""
        args = [
            "-c:v", self.video_codec.value,
            "-b:v", self.video_bitrate,
            "-c:a", self.audio_codec.value,
            "-b:a", self.audio_bitrate,
        ]
        
        if self.video_codec == VideoCodec.H264:
            args.extend(["-crf", str(self.quality)])
        
        if self.overwrite:
            args.append("-y")
        
        return args
