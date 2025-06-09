from pydantic import  BaseModel, Field
from typing import Optional

class ambienteBase(BaseModel):
    nombre_ambiente: str = Field(min_length=3, max_length=80)
    num_max_aprendices: int = Field(gt=0, le=100)
    municipio:str = Field(min_length=3, max_length=50)
    ubicacion: str = Field(min_length=3,max_length=100)
    cod_centro:int
    estado: bool
    id_rol: int 

class ambientecreate(ambienteBase):
    pass_hassed: str = Field(min_length=8, max_length=50)

class ambienteUpdate(ambienteBase):
    nombre_ambiente: Optional[str] = Field(default=None, min_length=3, max_length=80)
    num_max_aprendices: Optional[str] = Field(default=None, gt=0, le=100)
    municipio: Optional[str] = Field(min_length=3, max_length=50)
    ubicacion: Optional[str] = Field(min_length=3,max_length=100)

class ambienteOut(ambienteBase):
    id_ambiente: int