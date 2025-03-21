"""
Borra todos los registros de la colección @mensajes de la BBDD de ATLAS


"""
"""
Borra todos los registros de la colección @mensajes de la BBDD de ATLAS
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MONGO_URL = os.getenv("MONGO_CONNECTION_STRING")
DB_NAME = os.getenv("DB_NAME", "chat_db")  

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
mensajes_collection = db["mensajes"]

confirm = input("Seguro men? (s/n): ")
if confirm.lower() != "s":
    print("❌ Operación cancelada.")
    exit()

# Eliminar todos los mensajes
result = mensajes_collection.delete_many({})
print(f"✅ {result.deleted_count} mensajes eliminados correctamente.")
