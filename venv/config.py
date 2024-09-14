from pymongo import MongoClient

# Conexao com Mongodb
cliente = MongoClient('mongodb://localhost:27017')
bd = cliente['banco_web']
pedidos_collection = bd['pedidos']
clientes_collection = bd['clientes']
produtos_collection = bd['produtos']
