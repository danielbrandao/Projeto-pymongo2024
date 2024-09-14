from bson import ObjectId
from flask import Flask, jsonify, request
from config import bd, pedidos_collection, produtos_collection, clientes_collection

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World."

### Declarando Classes
class Clientes():
    def __init__(self,id_cliente,nome,email,cpf,data_nascimento):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    def serialize(self):
        return{
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento,
        }

class Produtos():
    def __init__(self,id_produto,nome,descricao,preco,categoria):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria

    def serialize(self):
        return{
            "id_produto": self.id_produto,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "categoria": self.categoria,
        }

class Pedidos():
    def __init__(self,id_produto,id_cliente,data_pedido,valor):
        self.id_produto = id_produto
        self.id_cliente = id_cliente
        self.data_pedido = data_pedido
        self.valor = valor

    def serialize(self):
        return {
            "id_cliente": self.id_cliente,
            "id_produto": self.id_produto,
            "data_pedido": self.data_pedido,
            "valor": self.valor,
        }   

### Criação das Rotas

@app.route("/clientes")
def lista_clientes():
    try:
        clientes = clientes_collection.find()

        clientes_serializado = []
        for cliente in clientes:
            cliente['_id'] = str(cliente['_id'])
            clientes_serializado.append(cliente)
        
        return jsonify(clientes_serializado), 200

    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao listas clientes.", 500

@app.route("/inserirCliente", methods=['POST'])
def set_cliente():
    dados = request.get_json()
    novo_cliente = Clientes(
        id_cliente=dados['id_cliente'],
        nome=dados['nome'],
        email=dados['email'],
        cpf=dados['cpf'],
        data_nascimento=dados["data_nascimento"]
    )

    resultado = clientes_collection.insert_one(novo_cliente.serialize())

    if  resultado.inserted_id:
        novo_cliente.id_cliente = str(resultado.inserted_id)
        return jsonify(novo_cliente.serialize()), 201
    else:
        return "Erro ao inserir cliente.", 500

@app.route("/alteraCliente/<id_cliente>", methods=["PUT"])
def update_cliente(id_cliente):
    try:
        dados = request.get_json()

        # Converter id_cliente para inteiro (ajuste se necessário)
        id_cliente = int(id_cliente)

        # Buscar o documento utilizando o id_cliente personalizado
        resultado_busca = clientes_collection.find_one({"id_cliente": id_cliente})

        if resultado_busca:
            _id = resultado_busca["_id"]

            # Atualiza o documento utilizando o _id
            resultado_atualizacao = clientes_collection.update_one(
                {"_id": _id},
                {"$set": dados}
            )

            if resultado_atualizacao.modified_count == 1:
                return f"Cliente {id_cliente} atualizado com sucesso.", 200
            else:
                return f"Erro ao atualizar cliente.", 500
        else:
            return f"Cliente com id {id_cliente} não encontrado.", 404

    except Exception as e:
        return f"Erro ao atualizar cliente: {e}", 500

@app.route("/excluiCliente/<id_cliente>", methods=["DELETE"])
def delete_cliente(id_cliente):
    try:

        # Converter id_cliente para inteiro (ajuste se necessário)
        id_cliente = int(id_cliente)

        # Buscar o documento utilizando o id_cliente personalizado
        resultado_busca = clientes_collection.find_one({"id_cliente": id_cliente})

        if resultado_busca:
            _id = resultado_busca["_id"]

            resultado = clientes_collection.delete_one(
                {"_id": _id}
            )

            if resultado.deleted_count == 1:
                return f"Cliente {id_cliente} excluido com sucesso.", 200
            else:
                return f"Cliente com id {id_cliente} não encontrado.", 404

    except Exception as e:
        return f"Erro ao excluir cliente: {e}", 500


if __name__ == "__main__":
    app.run(debug=True)