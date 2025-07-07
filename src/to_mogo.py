import json
from pymongo import MongoClient

# Conectar ao MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client["olist_ecommerce"]
collection = db["orders"]

#Limpar coleção antes de inserir para evitar duplicação
collection.drop()

# Carregar os dados do JSON
with open("data/olist/json/orders.json", encoding="utf-8") as f:
    orders_json = json.load(f)

# Inserir no MongoDB
result = collection.insert_many(orders_json)
print(f"Inseridos {len(result.inserted_ids)} documentos no MongoDB com sucesso!")
