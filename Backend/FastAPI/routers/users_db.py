from fastapi import APIRouter, HTTPException, status
from db.models.user import User # Importando el modelo User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId # Clase que representa el id de MongoDB

router = APIRouter(prefix = '/user_db',
                    tags = ['user_db'],
                    responses = {status.HTTP_404_NOT_FOUND: {'message': 'No encontrado'}})

# Iniciar el server: uvicorn users:app --reload

def search_user(id: int):
    return ""

def search_user(field: str, key):
    
    try:
        # find_one: Busca un solo registro que cumpla la condición
        user = user_schema(db_client.users.find_one({field: key}))
        return User(**user)
    except:
        return {'Error': 'No se ha encontrado el usuario'}


#----- PETICIÓN GET -----#
@router.get('/', response_model = list[User]) # Indica que la respuesta será una lista de usuarios
async def users():
    return users_schema(db_client.users.find()) # Devuelve todos los usuarios de la colección users

#----- PARÁMETROS POR EL PATH -----#
@router.get('/{id}')
async def user(id: str):
    return search_user('_id', ObjectId(id))
    
#----- PARÁMETROS DE QUERY -----#
@router.get('/')
async def user(id: str):
    return search_user('_id', ObjectId(id))


#----- PETICIÓN POST -----#
@router.post('/', response_model = User, status_code = status.HTTP_201_CREATED) 
async def user(user: User):
    if type(search_user('email', user.email)) == User:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'El usuario ya existe')
    
    user_dict = dict(user) # Se convierte el usuario a diccionario (JSON)s
    del user_dict['id']  # Se elimina el id para que MongoDB lo genere automáticamente
    
    # db_client: Accedemos al cliente de la base de datos
    # .local: Es el nombre de nuestra base de datos
    # .users: Es el nombre de nuestra colección
    # .insert_one: Inserta un solo registro
    # .insert_many: Inserta varios registros
    # .inserted_id: Devuelve el id del registro insertado
    id = db_client.users.insert_one(user_dict).inserted_id
    
    # Busca el usuario recién creado por su id y lo retorna como un JSON
    new_user = user_schema(db_client.users.find_one({'_id': id}))
    
    return User(**new_user)


#----- PETICIÓN PUT -----#  
@router.put('/', response_model = User)
async def user(user: User):
    
    try:
        user_dict = dict(user)
        del user_dict['id']  # Se elimina el id para que MongoDB lo genere
                
        # find_one_and_replace: Busca un registro y lo reemplaza completo
        db_client.users.find_one_and_replace({'_id': ObjectId(user.id)}, user_dict)
    except:
        return {'Error': 'No se ha actualizado el usuario'}

    return search_user('_id', ObjectId(user.id))


#----- PETICIÓN DELETE -----#
@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT) # Indica que no devuelve nada
async def user(id: str):

    # find_one_and_delete: Busca un registro y lo elimina completo
    found = db_client.users.find_one_and_delete({'_id': ObjectId(id)})

    if not found:
        return {'Error': 'No se ha eliminado el usuario'}

    return {'Confirmado': 'El usuario se eliminó correctamente'}