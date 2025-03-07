from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Variables de conexión
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# Escapar caracteres especiales en la contraseña
escaped_password = quote_plus(DB_PASSWORD)

# Crear la cadena de conexión
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{escaped_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Verificar que DATABASE_URL esté correctamente formada
if not DATABASE_URL:
    raise ValueError("La cadena de conexión no está bien formada")

# Configurar el engine con pool_pre_ping=True para reconectar conexiones inactivas
engine = create_engine(
    DATABASE_URL,
    pool_size=10,         # Mantiene hasta 10 conexiones abiertas
    max_overflow=5,       # Permite hasta 5 conexiones adicionales si hay demanda
    pool_timeout=30,      # Espera hasta 30 segundos antes de descartar una conexión
    pool_recycle=1800,    # Recicla conexiones después de 30 minutos (1800 segundos)
    pool_pre_ping=True    # Verifica si la conexión sigue activa antes de usarla
)

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()  # Asegura que la conexión se cierre correctamente


