from fastapi import APIRouter, UploadFile, File, Depends
import pandas as pd
from sqlalchemy.orm import Session
from io import BytesIO
from app.crud.cargar_archivo import insertar_datos_en_bd
from core.database import get_db

router = APIRouter()

@router.post("/upload-excel-pe04/")
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    df = pd.read_excel(
        BytesIO(contents),
        engine="openpyxl",
        skiprows=4,
        usecols=["IDENTIFICADOR_FICHA", "CODIGO_CENTRO", "CODIGO_PROGRAMA", "VERSION_PROGRAMA", "NOMBRE_PROGRAMA_FORMACION"],  # Nombres reales
        dtype=str
    )
    print(df.head())  # paréntesis
    print(df.columns)
    print(df.dtypes)

    # Renombrar columnas
    df = df.rename(columns={
        "IDENTIFICADOR_FICHA": "cod_ficha",
        "CODIGO_CENTRO": "cod_centro",
        "CODIGO_PROGRAMA": "cod_programa",
        "VERSION_PROGRAMA": "la_version",
        "ESTADO_CURSO": "estado_grupo",
        "NIVEL_FORMACION": "nombre_nivel",
        "NOMBRE_JORNADA": "jornada",
        "FECHA_INICIO_FICHA": "fecha_inicio",
        "FECHA_TERMINACION_FICHA": "fecha_fin",
        "ETAPA_FICHA": "etapa",
        "MODALIDAD_FORMACION": "modalidad",
        "NOMBRE_RESPONSABLE": "responsable",
        "NOMBRE_EMPRESA": "nombre_empresa",
        "NOMBRE_MUNICIPIO_CURSO": "nombre_municipio",
        "NOMBRE_PROGRAMA_ESPECIAL": "nombre_programa_especial",
        "NOMBRE_PROGRAMA_FORMACION": "nombre"
    })

    print(df.head())  # paréntesis

    #si quiere que funcione en todas las partes del pais
    #crear codigo para llenar regionales y centros y eliminar esta linea
    df = df[df["cod_centro"] == '9121']#filtrar por centro especifico
    print(df.head()) 

# # Eliminar filas con valores faltantes en campos obligatorios
    required_fields = [
        "cod_ficha", "cod_centro", "cod_programa", "la_version", "nombre"
        # "fecha_inicio", "fecha_fin", "etapa", "responsable", "nombre_municipio"
    ]
    # Solo dejar en required_fields las columnas que realmente existen en el DataFrame
    required_fields = [col for col in required_fields if col in df.columns]
    df = df.dropna(subset=required_fields)

    # Convertir columnas a tipo numérico
    for col in ["cod_ficha", "cod_programa", "la_version"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    
    print(df.head())  # paréntesis

    # # Convertir fechas solo si existen las columnas
    if "fecha_inicio" in df.columns:
        df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], errors="coerce").dt.date
    if "fecha_fin" in df.columns:
        df["fecha_fin"] = pd.to_datetime(df["fecha_fin"], errors="coerce").dt.date

    # # Asegurar columnas no proporcionadas
    df["hora_inicio"] = "00:00:00"
    df["hora_fin"] = "00:00:00"
    df["aula_actual"] = ""

    # Crear DataFrame de programas únicos
    df_programas = df[["cod_programa", "la_version", "nombre"]].drop_duplicates()
    df_programas["horas_lectivas"] = 0
    df_programas["horas_productivas"] = 0

    print(df_programas.head())
    
#eliminar la columna nombre del df
    df = df.drop('nombre',exis=1)
    print(df.head())

    resultados = insertar_datos_en_bd(db, df_programas, df)
    return resultados

