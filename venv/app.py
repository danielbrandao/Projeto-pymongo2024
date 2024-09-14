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

@app.route("/produtos")
def lista_produtos():
    try:
        produtos = produtos_collection.find()

        produtos_serializado = []
        for produto in produtos:
            produto['_id'] = str(produto['_id'])
            produtos_serializado.append(produto)
        
        return jsonify(produtos_serializado), 200

    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao listar produtos.", 500

@app.route("/inserirProduto", methods=['POST'])
def set_produto():
    dados = request.get_json()

    novo_produto = Produtos(
        id_produto=dados['id_produto'],
        nome=dados['nome'],
        categoria=dados['categoria'],
        preco=dados['preco'],
        descricao=dados["descricao"]
    )

    resultado = produtos_collection.insert_one(novo_produto.serialize())

    if  resultado.inserted_id:
        novo_produto.id_produto = str(resultado.inserted_id)
        return jsonify(novo_produto.serialize()), 201
    else:
        return "Erro ao inserir produto.", 500

@app.route("/alteraProduto/<id_produto>", methods=["PUT"])
def update_produto(id_produto):
    try:
        dados = request.get_json()

        # Converter id_produto para inteiro (ajuste se necessário)
        id_produto = int(id_produto)

        # Buscar o documento utilizando o id_produto personalizado
        resultado_busca = produtos_collection.find_one({"id_produto": id_produto})

        if resultado_busca:
            _id = resultado_busca["_id"]

            # Atualiza o documento utilizando o _id
            resultado_atualizacao = produtos_collection.update_one(
                {"_id": _id},
                {"$set": dados}
            )

            if resultado_atualizacao.modified_count == 1:
                return f"produto {id_produto} atualizado com sucesso.", 200
            else:
                return f"Erro ao atualizar produto.", 500
        else:
            return f"produto com id {id_produto} não encontrado.", 404

    except Exception as e:
        return f"Erro ao atualizar produto: {e}", 500

@app.route("/excluiproduto/<id_produto>", methods=["DELETE"])
def delete_produto(id_produto):
    try:

        # Converter id_produto para inteiro (ajuste se necessário)
        id_produto = int(id_produto)

        # Buscar o documento utilizando o id_produto personalizado
        resultado_busca = produtos_collection.find_one({"id_produto": id_produto})

        if resultado_busca:
            _id = resultado_busca["_id"]

            resultado = produtos_collection.delete_one(
                {"_id": _id}
            )
            print(resultado)
            if resultado.deleted_count == 1:
                return f"produto {id_produto} excluido com sucesso.", 200
            else:
                return f"produto com id {id_produto} não encontrado.", 404

    except Exception as e:
        return f"Erro ao excluir produto: {e}", 500

@app.route("/pedidos", methods=['POST'])
def set_pedido():
    dados = request.get_json()
    id_cliente = dados['id_cliente']
    id_produto = dados['id_produto']

    # Verificar se o cliente existe
    cliente = clientes_collection.find_one({"id_cliente": id_cliente})
    if not cliente:
        return jsonify({"error": "Cliente não encontrado"}), 404

    # Verificar se o produto existe
    produto = produtos_collection.find_one({"id_produto": id_produto})
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404

    # Criar o novo pedido
    novo_pedido = {
        "id_cliente": id_cliente,
        "id_produto": id_produto,
        "data_pedido": id_pedido,
        "valor": valor
    }
    resultado = pedidos_collection.insert_one(novo_pedido)

    if resultado.inserted_id:
        return jsonify({"Pedido criado com sucesso"}), 201
    else:
        return jsonify({"Erro ao criar pedido"}), 500


if __name__ == "__main__":
    app.run(debug=True)