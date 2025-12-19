import os
from pymongo import MongoClient

# ---------- BASE DE DATOS LOCAL ---------- #

# Si no se le pasa nada por parámetro, se conecta al localhost por defecto
# Se agrega .local para seleccionar la base de datos llamada local
# db_client = MongoClient().local


# ---------- BASE DE DATOS REMOTA ---------- #

# La petición a la API sigue siendo http://127.0.0.1:8000#
# Pero la base de datos está en la nube, en MongoDB Atlas
# Para subir mi API a producción, debo cambiar la variable de entorno MONGO_URI para no exponer mi URI públicamente
MONGO_URI = os.getenv("MONGO_URI")

db_client = MongoClient(MONGO_URI).admin_test