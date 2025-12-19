# Creación de routers, se configura todo desde el main y se importa APIRouter
# La idea es tener un solo router para /user, /users, /products, etc
from fastapi import APIRouter

# prefix = '/products': Por defecto, es /products y todas las peticiones que haga, tiene /products al inicio
# tags = ['products']: En la documentación, va a dividir todas las peticiones de products con un título, el cual es products
router = APIRouter(prefix = '/products',
                tags = ['products'],
                responses = {404: {'message': 'No encontrado'}})

products_list = ['Producto 1', 'Producto 2', 'Producto 3', 'Producto 4', 'Producto 5']


@router.get('/')
async def products():
    return products_list

@router.get('/{id}')
async def products(id: int):
    return products_list[id]