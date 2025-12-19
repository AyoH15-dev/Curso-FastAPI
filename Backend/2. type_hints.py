#TIPOS EN PYTHON
# -Python es un lenguaje de programación de tipo dinámico, significa que puedo estar variando el tipo de dato de una variable

# -FastAPI recomienda darle el tipo de dato a una variable, esto aumenta el rendimiendo de la API
# Al declarar el tipo de dato a una variable, podemos acceder a los métodos para un str, int, float, list, etc.

def get_full_name(first_name: str, last_name: str): # 
    
    # .title(): La primera letra de cada palabra del texto las convierte en mayúscula y las demás letras en minúscula
    full_name = first_name.title() + ' ' + last_name.title()
    return full_name

print(get_full_name('santiago', 'hernández'))

#--------------------------------------------------------------------------------------------------------#
my_typed_variable: int = 'My typed String variable' # Pide un entero pero no genera error si se le da otro tipo de dato
print(type(my_typed_variable))

my_typed_variable = 5
print(type(my_typed_variable))

#--------------------------------------------------------------------------------------------------------#
# Se pide 'name' como str y 'age' como int, para que no genere error, se convierte age en un str: str(age)
def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + str(age)
    return name_with_age

get_name_with_age('santiago', 40)

#---------- TIPOS GENÉRICOS ----------#
# Los tipos genéricos son los tipos que tienen tipos internos como los diccionarios, las listas, los conjuntos y las tuplas
# items: list[str] Esto indica que la variable items es una lista, y cada uno de los ítems en esta lista es un str
# item: Dentro del for, el editor sabe que item es un str porque es un elemento de la lista items
def process_items(items: list[str]):
    for item in items:
        print(item)

#--------------------------------------------------------------------------------------------------------#    
# La variable items_t es una tupla con 3 ítems, un int, otro int y un str
# La variable items_s es un conjunto, donde cada uno de sus items es de tipo bytes
def process_items(items_t: tuple[int, int, str], items_s: set[bytes]):
    return items_t, items_s

#--------------------------------------------------------------------------------------------------------#
# El primer parámetro del diccionario prices es de tipo str para las keys
# El segundo parámetro del diccionario prices es de tipo float para los values
def process_items(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)
        
#--------------------------------------------------------------------------------------------------------#
# '|': Indica que la variable item puede ser un int o un str        
def process_item(item: int | str):
    print(item)
    
#--------------------------------------------------------------------------------------------------------#
# La variable name puede ser un str o un None
# Si es str, muestra Hey {name}, si es None muestra Hello World
def say_hi(name: str | None = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")

say_hi()

#---------- CLASES COMO TIPOS ----------#
class Person:
    def __init__(self, name: str):
        self.name = name

# Declaro la variable one_person de tipo Person, esto me permite ver los métodos y propiedades de la clase Person
def get_person_name(one_person: Person):
    return one_person.name

#---------- MODELOS PYDANTIC ----------#
# SE RECOMIENDA PROFUNDIZAR EN PYDANTIC
# Pydantic es un paquete de Python para realizar la validación de datos
# Pydantic tiene la capacidad de convertir tipos a los que pide el desarrollador
from datetime import datetime
from pydantic import BaseModel

class User(BaseModel): # Clase con atributos, donde cada atributo tiene su tipo
    id: int
    name: str = "John Doe" # Valor por defecto es John Doe
    signup_ts: datetime | None = None # Puede ser fecha y hora o None, valor por defecto es None
    friends: list[int] = []

# Diccionario que simula datos que vienen de afuera (una API, del frontend, de una base de datos, de un .json, etc)
external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"], # pydantic convierte estos datos en enteros como se especifica en list[int]
}
#**external_data: Los ** hacen desempaquetado de diccionario, equivale a escribir todo el diccionario
user = User(**external_data)
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.signup_ts)
# > 123

#---------- ANOTACIONES DE TIPOS EN FASTAPI ----------#
# -Chequeo de tipos: FastAPI va a validar que mis datos son los correctos
# -Convertir datos
# -Documentar la API usando OpenAPI# -Validar datos