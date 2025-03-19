"""

Conexion a Mongo DB Atlas

"""





"""
 En este paso vamos a configurar la conexión a Mongo Atlas desde nuestro código usando Motor, el driver asíncrono para MongoDB.
"""

import motor .motor_asyncio
import os
from dotenv import load_dotenv



#!Cargamos las variables de entorno desde .env
load_dotenv()

#!Obtenemos la connection String desde la variable de entorno en .env
MONGO = os.getenv("MONGO_CONNECTION_STRING")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO)

database = client.Chat_app

usuarios_collection = database.get_collection("Usuarios")


#!Si en el futuro deseas agregar más colecciones (por ejemplo, para mensajes), puedes definirlas aquí:
#!mensajes_collection = database.get_collection("mensajes")




