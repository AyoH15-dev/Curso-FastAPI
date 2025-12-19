# Hay estándares para autentificar a una persona para poder entrar a su cuenta como oauth
# status: Tiene todos los códigos HTTP para mayor legibilidad
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel

# OAuth2PasswordBearer: Es la clase que se va a encargar de gestionar la autenticación, el usuario y la contraseña
# OAuth2PasswordRequestForm: Es la forma en la que el Backend va a obtener y enviar el usuario y la contraseña
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  


router = APIRouter()


oauth2 = OAuth2PasswordBearer(tokenUrl = 'login')


users_db = {
    'ayoh15': {
        'username' : 'ayoh15', 
        'full_name': 'Santiago Hernández Rodríguez',
        'email' : 'example@example.com',
        'disabled': False,
        'password' : '123456'
    },
    'ayoh18': {
        'username' : 'ayoh18', 
        'full_name': 'Santiago Hernández Rodríguez 2',
        'email' : 'example2@example.com',
        'disabled': True,
        'password' : '654321'
    },
}

class User(BaseModel): # Usuario en el cliente sin contraseña (por seguridad)
    username: str
    full_name: str
    email: str
    disabled: bool
    
class User_db(User): # Usuario dentro de la base de datos con contraseña (por seguridad)
    password: str


def search_user_db(username: str):
    if username in users_db:
        return User_db(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Criterio de dependencia
async def current_user(token: str = Depends(oauth2)): # El token se busca dentro del sistema de autentificación creado, osea oauth2
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Credenciales de autenticación inválidas',
            headers = {'WWW-Authenticate': 'Bearer'})
        
    if user.disabled:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = 'Usuario inactivo')
        
    return user

# ---------- AUTÉNTICACIÓN ---------- #
@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()): # Entra como parámetro form de tipo OAuth2PasswordRequestForm
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
                        status_code = status.HTTP_400_BAD_REQUEST,
                        detail = 'El usuario no es correcto') # 400: Porque no ha encontrado el dato
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
                        status_code = status.HTTP_400_BAD_REQUEST,
                        detail = 'La contraseña no es correcta') # 400: Porque no ha encontrado el dato
    
    return {'access_token': user.username, 'token_type': 'bearer'}

@router.get('/users/me') # Una vez autenticados, muestra cual es el usuario
async def me(user: User = Depends(current_user)):
    return user