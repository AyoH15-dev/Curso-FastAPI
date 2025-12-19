from pymongo import MongoClient

# ---------- BASE DE DATOS LOCAL ---------- #

# Si no se le pasa nada por parámetro, se conecta al localhost por defecto
# Se agrega .local para seleccionar la base de datos llamada local
# db_client = MongoClient().local


# ---------- BASE DE DATOS REMOTA ---------- #

# La petición a la API sigue siendo http://127.0.0.1:8000#
# Pero la base de datos está en la nube, en MongoDB Atlas
db_client = MongoClient(
    'mongodb+srv://admin_test:admin_test@cluster0.xkvt1jj.mongodb.net/?appName=Cluster0').admin_test