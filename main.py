from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import ambiente, users
from app.api import auth
from app.api import cargar_archivo 

app = FastAPI()

# Incluir en el objeto app los routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router,prefix="/access",tags=["/login"])
app.include_router(ambiente.router, prefix="/ambiente", tags=["ambiente"])
app.include_router(cargar_archivo.router,prefix="/cargar_archivo",tags=["cargar_archivo"])

# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)

@app.get("/")
def read_root():
    return {
                "message": "ok",
                "autor": "ADSO 2847248"
            }

