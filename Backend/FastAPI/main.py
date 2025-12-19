#FastAPI tiene soporte para Docker
from dotenv import load_dotenv
load_dotenv() # Carga las variables de entorno del archivo .env

from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles


app = FastAPI() # Creamos una clase que se llama app

# Routers
app.include_router(products.router) # Se incluye el router products
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

# Primero se pone el nombre del directorio, luego se pone el tipo, que es static, y luego el nombre para sacarlo que es static
# Con esto puedo acceder a las imágenes, videos, etc desde la URL poniendo /static/images/python.webp
app.mount('/static', StaticFiles(directory = 'static'), name = 'static')


# Protocolo HTTP para hablar a través de la red
# get(): Es todo lo que hacemos cuando vamos a un navegador y llamamos una URL, se hace un get a la URL para obtener la página web
# La función root, cuando hacemos un get a algo que es /, nuestro server hace algo y retorna ¡Hola FastAPI!
@app.get('/') # Código de FastAPI, hacemos un get a un /
async def root(): # Siempre al llamar a un servidor, la operación que se ejecuta debe ser asíncrona, el servidor se puede tardar poco o mucho en responder, si es asíncrono, mi programa sigue funcionando
    return "Hola FastAPI!"

#-----INICIAR EL SERVIDOR-----#
# Ejecutar este comando en la terminal
# uvicorn main:app --reload
# main: Es el nombre del fichero raíz que nosotros queremos arrancar
# :app: Es la instancia que tenemos de FastAPI en el código
# --reload: Recarga el contexto del servidor cada vez que cambiemos algo en el fichero main, no detiene el servidor, se actualiza cada vez que guardo el archivo main

# El servidor tiene una URL que aparece en la línea:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# Esa dirección IP la tienen todos los ordenadores, fuera de cada PC no vale nada

@app.get('/url') # url es un endpoint http://127.0.0.1:8000/url
async def url(): # Poner nombre de l función dependiendo su función
    return {'url':'https://ayo-dev.com/python'}

# ----- DOCUMENTACIÓN DE LA API ----- # 
# Documentación con Swagger: endpoint /docs
# Documentación con Redocly; endpoint /redoc