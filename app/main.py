from fastapi import FastAPI
from .database import Base, engine
from .routers import contratos

# Crear las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Microservicio de Contratos - AndinaTrading")

app.include_router(contratos.router)

@app.get("/")
def root():
    return {"mensaje": "Microservicio de contratos funcionando correctamente"}