from sqlalchemy import Column, Integer, Float, DateTime, Enum, Text, ForeignKey
from datetime import datetime
from .database import Base
import enum

class EstadoContrato(enum.Enum):
    PENDIENTE = "PENDIENTE"
    ACEPTADO = "ACEPTADO"
    RECHAZADO = "RECHAZADO"
    VENCIDO = "VENCIDO"

class Contrato(Base):
    __tablename__ = "contrato"

    id = Column(Integer, primary_key=True, index=True)
    inversionista_id = Column(Integer, ForeignKey("inversionista.id"))
    comisionista_id = Column(Integer, ForeignKey("comisionista.id"))
    porcentaje_comision = Column(Float, default=1.5)
    duracion_horas = Column(Integer, default=24)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(Enum(EstadoContrato), default=EstadoContrato.PENDIENTE)
    observaciones = Column(Text, nullable=True)