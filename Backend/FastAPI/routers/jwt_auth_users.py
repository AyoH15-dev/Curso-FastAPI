# ---------- 1️⃣ IMPORTS (librerías) ---------- #
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

# ---------- 2️⃣ CONFIGURACIÓN GLOBAL ---------- #

ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION = 1   # Minutos

#SECRET_KEY = Creado con el comando openssl rand -hex 32 en la terminal
SECRET_KEY = '21c472043d74fc6d11f32b83edd5b8ca0725ec27c6af7962c48bca1fb8049c4b' # Clave secreta para firmar el token (debe ser larga y compleja)

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl = 'login')
password_hash = PasswordHash.recommended()

# ---------- 3️⃣ CONSTANTES / VARIABLES GLOBALES ---------- #

users_db = {
    'ayoh15': {
        'username' : 'ayoh15', 
        'full_name': 'Santiago Hernández Rodríguez',
        'email' : 'example@example.com',
        'disabled': False,
        'password' : '$argon2id$v=19$m=16,t=2,p=1$YTlGM2tRMlo$twJCfb+8HxXYQbU2CSueVA'
    },
    'ayoh18': {
        'username' : 'ayoh18', 
        'full_name': 'Santiago Hernández Rodríguez 2',
        'email' : 'example2@example.com',
        'disabled': True,
        'password' : '$argon2id$v=19$m=16,t=2,p=1$YTlGM2tRMlo$KNAQumSJwtqVJ41GPa0iEw'
    },
}

# ---------- 4️⃣ MODELOS (Pydantic) ---------- #

class User(BaseModel): # Usuario en el cliente sin contraseña (por seguridad)
    username: str
    full_name: str
    email: str
    disabled: bool
    
class User_db(User): # Usuario dentro de la base de datos con contraseña (por seguridad)
    password: str
    

# ---------- 5️⃣ FUNCIONES AUXILIARES (lógica) ---------- #

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

def search_user_db(username: str):
    if username in users_db:
        return User_db(**users_db[username])

# ---------- 6️⃣ DEPENDENCIAS (Depends) ---------- #

async def auth_user(token: str = Depends(oauth2)):
    exception_401 = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Credenciales de autenticación inválidas',
            headers = {'WWW-Authenticate': 'Bearer'})
    
    try:
        user_name = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM]).get('sub')
        if user_name is None: # Si es usuario está vación
            raise exception_401
            
    except PyJWTError:
        raise exception_401
    
    return search_user(user_name)

async def current_user(user: User = Depends(auth_user)): # El token se busca dentro del sistema de autentificación creado, osea oauth2 
    if user.disabled:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = 'Usuario inactivo')
        
    return user

# ---------- 7️⃣ ENDPOINTS / RUTAS ---------- #

@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()): # Entra como parámetro form de tipo OAuth2PasswordRequestForm
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
                        status_code = status.HTTP_400_BAD_REQUEST,
                        detail = 'El usuario no es correcto') # 400: Porque no ha encontrado el dato
    
    user = search_user_db(form.username)
    
    if not password_hash.verify(form.password, user.password):
        raise HTTPException(
                        status_code = status.HTTP_400_BAD_REQUEST,
                        detail = 'La contraseña no es correcta') # 400: Porque no ha encontrado el dato
    
    # datetime.now(timezone.utc): Fecha y hora actual en UTC, ejemplo: 2024-06-12 14:30:00+00:00
    # timedelta(minutes = ACCESS_TOKEN_DURATION): Da n minutos más al token de acceso
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_DURATION)
    access_token = {
        'sub': user.username,
        'exp': expire
    }
    enconded_jwt = jwt.encode(access_token, SECRET_KEY, algorithm = ALGORITHM)
    
    return {'access_token': enconded_jwt, 'token_type': 'bearer'} # Bearer: Tipo de token que se usa en OAuth2

@router.get('/users/me') # Una vez autenticados, muestra cual es el usuario
async def me(user: User = Depends(current_user)):
    return user