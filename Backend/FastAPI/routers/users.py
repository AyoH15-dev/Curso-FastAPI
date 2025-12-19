from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list) # Obtiene el id que entra como parámetro de la lista users_list
    
    try: # Manejo de errores cuando no encuentra el usuario con un id inválido
        return list(users)[0]
    except:
        return {'Error': 'No se ha encontrado el usuario'}

router = APIRouter(tags = ['users'])

# Iniciar el server: uvicorn users:app --reload

# Objeto User()
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    
users_list = [User(id = 1, name = "Santiago", surname = "Hernandez", age = 28),
                User(id = 2, name = "Lisa", surname = "Frank", age = 33),
                User(id = 3, name = "Victor", surname = "Bonilla", age = 21)]


#----- PETICIÓN GET -----#
@router.get('/users_json')
async def users_json():
    return [{"name": "Santiago", "surname": "Hernandez", "age": 28},
            {"name": "Lisa", "surname": "Frank", "age": 33},
            {"name": "Victor", "surname": "Bonilla", "age": 21}]

@router.get('/users')
async def users():
    return users_list


#----- PARÁMETROS POR EL PATH -----#
# Van por la URL y se usa para parámetros fijos
@router.get('/user/{id}') # Parámetro id se pone entre llaves, el endpoint seria /user/1 para el id = 1
async def user(id: int): # Le pasamos el id como parámetro
    return search_user(id)
    
    
#----- PARÁMETROS DE QUERY -----#
# Podemos llamar casi lo que nosotros queramos
# Se usa para parámetros dinámicos, por ejemplo: Una red social envia las primeras 10 publicaciones y a medida que el usuario va bajando, la API va enviando las otras 10 publicaciones
@router.get('/user_query/') # En la URL se pone la query, /user_query/?id=1
async def user(id: int, name: str): # Le pasamos el id y el nombre, para dos parámetros se separa con &, ejemplo: /user_query/?id=1&name=santiago
    return search_user(id)


#----- PETICIÓN POST -----#
# status_code = 201: Manda un 201 que significa que todo ha salido bien y se ha creado algo, se pone un código de respuesta por defecto, si algo va mal, se cambia en otra parte de la función
# response_model = User: En el caso correcto, devolvemos una variable de tipo User, se usa para mejorar la documentación de la API
@router.post('/user/', response_model = User, status_code = 201) # Añadir nuevo usuario, para ello uso el mismo endpoint de user 
async def user(user: User): # Para añadir un usuario, tiene que ser del mismo tipo para poderla guardar
    if type(search_user(user.id)) == User:
        # raise: Se usa para manejar excepciones
        raise HTTPException(status_code = 404, detail = 'El usuario ya existe') # Al mandar una excepción, no se usa return, se usa raise
    
    users_list.append(user)
    return user


#----- PETICIÓN PUT -----#  
@router.put('/user/') # El put se usa para actualizar datos, se debe recibir como parámetro el usuario completo
async def user(user: User):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {'Error': 'No se ha actualizado el usuario'}

    return user


#----- PETICIÓN DELETE -----#
@router.delete('/user/{id}') # Eliminar un usuario con el id
async def user(id: int):

    found = False
    
    for index, delete_user in enumerate(users_list):
        if delete_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {'Error': 'No se ha eliminado el usuario'}

    return {'Confirmado': 'El usuario se eliminó correctamente'}