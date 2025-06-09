from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException, status
from core.database import get_db
from core.dependencies import get_current_user
from app.schemas.ambiente import ambienteBase, ambienteOut, ambientecreate, ambienteUpdate
from app.crud import ambiente as crud_ambiente

router = APIRouter()

# Crear ambiente_formacion (solo superadmin y admin)
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_ambiente(
    ambiente: ambientecreate,
    db: Session = Depends(get_db),
    current_user: ambienteOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    try:
        ambiente_db = crud_ambiente.create_ambiente(db, ambiente)
        return {"message": "Ambiente creado correctamente", "ambiente": ambiente_db}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Modificar ambiente_formacion (solo superadmin y admin)
@router.put("/update/{id_ambiente}")
def update_ambiente(
    id_ambiente: int,
    ambiente: ambienteUpdate,
    db: Session = Depends(get_db),
    current_user: ambienteOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    try:
        updated = crud_ambiente.update_ambiente(db, id_ambiente, ambiente)
        if not updated:
            raise HTTPException(status_code=404, detail="Ambiente no encontrado")
        return {"message": "Ambiente actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener por id ambiente_formacion
@router.get("/get-by-id/{id_ambiente}", response_model=ambienteOut)
def get_ambiente_by_id(
    id_ambiente: int,
    db: Session = Depends(get_db),
    current_user: ambienteOut = Depends(get_current_user)
):
    try:
        ambiente = crud_ambiente.get_ambiente_by_id(db, id_ambiente)
        if not ambiente:
            raise HTTPException(status_code=404, detail="Ambiente no encontrado")
        return ambiente
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener los ambientes activos por centro de formación
@router.get("/activos-by-centro/{cod_centro}", response_model=list[ambienteOut])
def get_ambientes_activos_by_centro(
    cod_centro: int,
    db: Session = Depends(get_db),
    current_user: ambienteOut = Depends(get_current_user)
):
    try:
        ambientes = crud_ambiente.get_ambientes_activos_by_centro(db, cod_centro)
        if not ambientes:
            raise HTTPException(status_code=404, detail="No se encontraron ambientes activos para este centro")
        return ambientes
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Modificar el estado de un ambiente de formación (solo superadmin y admin)
@router.put("/modify-status/{id_ambiente}")
def modify_status_ambiente(
    id_ambiente: int,
    db: Session = Depends(get_db),
    current_user: ambienteOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    try:
        updated = crud_ambiente.modify_status_ambiente(db, id_ambiente)
        if not updated:
            raise HTTPException(status_code=404, detail="Ambiente no encontrado")
        return {"message": "Estado del ambiente modificado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))