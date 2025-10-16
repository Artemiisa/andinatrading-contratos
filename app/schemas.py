from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class EstadoContrato(str, Enum):
    PENDIENTE = "PENDIENTE"
    ACEPTADO = "ACEPTADO"
    RECHAZADO = "RECHAZADO"
    VENCIDO = "VENCIDO"

class ContratoBase(BaseModel):
    inversionista_id: int
    comisionista_id: int
    porcentaje_comision: float = 1.5
    duracion_horas: int = 24
    observaciones: Optional[str] = None

class ContratoResponse(ContratoBase):
    id: int
    fecha_creacion: datetime
    estado: EstadoContrato

    class Config:
        orm_mode = True