"""Enumeración de estados de conversión."""
from enum import Enum


class ConversionStatus(str, Enum):
    """Estados posibles de un trabajo de conversión."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
