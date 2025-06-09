import logging
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.api import ambiente
from app.schemas.ambiente import ambienteUpdate, ambientecreate
from core.security import get_hashed_password

# Crear ambiente_formacion
logger = logging.getLogger(__name__)

def create_ambiente(db: Session, ambiente: ambientecreate):
    try:
        pass_hashed=get_hashed_password(ambiente.pass_hash)
        ambiente_data=ambiente.model_dump()
        ambiente_data = {'pass_hash': pass_hashed}
        query = (
            """
            INSERT INTO ambiente_formacion (nombre_ambiente, num_max_aprendices, municipio, ubicacion, cod_centro, estado)
            VALUES (:nombre_ambiente, :num_max_aprendices, :municipio, :ubicacion, :cod_centro, :estado)
            """
        )
        db.commit(query,ambiente_data)
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {e}")
        raise Exception("Error de base de datos al crear el ambiente: " + str(e))

# Modificar ambiente_formacion

def update_ambiente(db: Session, user_id: int, ambiente_update: ambienteUpdate) -> bool:
    try:
        fields = ambiente_update.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["id_ambiente"] = ambiente

        query = text(f"UPDATE usuario SET {set_clause} WHERE id_usuario = :id_ambiente")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario: {e}")
        raise Exception("Error de base de datos al actualizar el usuario")

# Obtener por id ambiente_formacion

def get_ambiente_by_id(db: Session, id_ambiente: int):
    try:
        query = text(""" SELECT  id_ambiente, nombre_ambiente, num_max_aprendices, ,
                                municiPio, ubicacion,
                                cod_centro, estado,id_rol
                     FROM ambiente_formacion
                     WHERE id_ambiente = :id """)
        result = db.execute(query, {"id": id_ambiente}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario por id: {e}")
        raise Exception("Error de base de datos al obtener el usuario")
# Obtener los ambientes activos por centro de formación

def get_ambiente_activos_by_centro(db: Session, cod_centro: int):
    try:
        query = "SELECT * FROM ambiente_formacion WHERE cod_centro = :cod_centro AND estado = TRUE"
        result = db.execute(query, {"cod_centro": cod_centro}).mappings().all()
        return result
    except SQLAlchemyError as e:
        raise Exception("Error de base de datos al obtener ambientes activos: " + str(e))

# Modificar el estado de un ambiente de formación

def modify_status_ambiente(db: Session, id_ambiente: int):
    try:
        query = "UPDATE ambiente_formacion SET estado = IF(estado, FALSE, TRUE) WHERE id_ambiente = :id_ambiente"
        result = db.execute(query, {"id_ambiente": id_ambiente})
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception("Error de base de datos al modificar el estado del ambiente: " + str(e))
