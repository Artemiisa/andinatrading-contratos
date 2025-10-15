# 🧩 Microservicio de Contratos - AndinaTrading

Microservicio encargado de la **gestión y formalización de contratos** entre inversionistas y comisionistas dentro del sistema **AndinaTrading**.  
Permite crear, aceptar o rechazar contratos antes de realizar transacciones bursátiles, y genera un **PDF automático** con los datos del acuerdo.



## 🚀 Características principales

- Creación de contratos entre **inversionistas** y **comisionistas**.  
- Estados de contrato: `PENDIENTE`, `ACEPTADO`, `RECHAZADO`, `VENCIDO`.  
- Generación automática de **PDFs** con información del contrato.  
- Registro en base de datos MySQL con integridad referencial.  
- API REST desarrollada con **FastAPI**.  
- Conexión con tablas:
  - `inversionista`
  - `comisionista`
  - `contrato`
  - `movimiento`

---

## 🧠 Arquitectura

```mermaid
flowchart TD
    A[Inversionista] -->|Crea orden y contrato| B[Microservicio Contratos]
    B -->|En espera| C[Comisionista]
    C -->|Acepta/Rechaza| B
    B -->|PDF generado| D[Base de datos MySQL]
    D --> E[Historial de movimientos]
