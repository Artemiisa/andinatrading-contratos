from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from ..database import SessionLocal
from ..models import Contrato, EstadoContrato
from ..schemas import ContratoBase
from ..services.pdf_service import generar_pdf_contrato_templatizado

import os

#  Un solo router
router = APIRouter(prefix="/contratos", tags=["Contratos"])

# Dependencia para manejar la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        


#  Crear contrato
@router.post("/")
def crear_contrato(contrato_data: ContratoBase, db: Session = Depends(get_db)):
    contrato = Contrato(**contrato_data.dict())
    db.add(contrato)
    db.commit()
    db.refresh(contrato)
    pdf_path = generar_pdf_contrato(contrato)
    return {"mensaje": "Contrato creado correctamente", "pdf": pdf_path}


#  Aceptar contrato
@router.put("/{contrato_id}/aceptar")
def aceptar_contrato(contrato_id: int, db: Session = Depends(get_db)):
    contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    if contrato.estado != EstadoContrato.PENDIENTE:
        raise HTTPException(status_code=400, detail="Solo se pueden aceptar contratos pendientes")

    contrato.estado = EstadoContrato.ACEPTADO
    db.commit()
    db.refresh(contrato)
    pdf_path = generar_pdf_contrato(contrato)
    return {"mensaje": "Contrato aceptado", "pdf": pdf_path}


#  Rechazar contrato
@router.put("/{contrato_id}/rechazar")
def rechazar_contrato(contrato_id: int, db: Session = Depends(get_db)):
    contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    if contrato.estado != EstadoContrato.PENDIENTE:
        raise HTTPException(status_code=400, detail="Solo se pueden rechazar contratos pendientes")

    contrato.estado = EstadoContrato.RECHAZADO
    db.commit()
    db.refresh(contrato)
    pdf_path = generar_pdf_contrato(contrato)
    return {"mensaje": "Contrato rechazado", "pdf": pdf_path}


#  Descargar PDF existente
@router.get("/{contrato_id}/pdf")
def descargar_pdf(contrato_id: int):
    pdf_path = f"pdfs/contrato_{contrato_id}.pdf"
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF no encontrado")
    return FileResponse(pdf_path, media_type='application/pdf', filename=f"contrato_{contrato_id}.pdf")


#  DEMO de prueba para el PDF
from datetime import datetime
import os
from fastapi.responses import FileResponse
from ..services.pdf_service import generar_pdf_contrato_templatizado

@router.get("/pdf/demo")
def generar_pdf_demo():
    """
    Genera un PDF de ejemplo con el estilo corporativo AndinaTrading.
    """
    pdf_path = generar_pdf_contrato_templatizado(
        contrato_id="C-2025-001",
        nombre_cliente="Juan Pérez",
        monto="5.000.000",
        fecha_emision=datetime.now().strftime("%d/%m/%Y %H:%M"),
        descripcion="Ejecución de órdenes bursátiles en la BVC conforme a autorización del cliente.",
        duracion_horas=24,
    )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path)
    )