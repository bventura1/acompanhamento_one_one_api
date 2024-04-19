from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, jsonify, redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from model import Session, Atividades#, Colaboradores
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
atividades_tag = Tag(name="Atividades", description="Adição, visualização e remoção de tarefas à base")
#colaboradores_tag = Tag(name="Colaboradores", description="Adição, visualização e remoção de colaboradores à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/atividade', tags=[atividades_tag],
          responses={"200": AtividadesViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_atividade(form: AtividadesSchema):
    """Adiciona uma nova tarefa à base de dados.
    """
    atividades = Atividades(
        tarefa=form.tarefa,
        colaborador=form.colaborador,
        status=form.status)
    logger.debug(f"Adicionando atividades de nome: '{atividades.tarefa}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(atividades)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado atividades de nome: '{atividades.tarefa}'")
        return apresenta_atividades(atividades), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        #error_msg = "Produto de mesmo nome já salvo na base :/"
        #logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar produto '{atividades.tarefa}', {error_msg}")
        return {"mesage": error_msg}, 400





@app.get('/atividades_all', tags=[atividades_tag],
         responses={"200": ListagemAtividadesSchema, "404": ErrorSchema})
def get_atividades_all():
    session = Session()
    atividades = session.query(Atividades).all()
    
    # Convertendo as atividades para um formato JSON
    atividades_json = []
    for atividade in atividades:
        atividades_json.append({
            'id': atividade.id,
            'tarefa': atividade.tarefa,
            'colaborador': atividade.colaborador,
            'status': atividade.status,
            #'data_insercao': atividade.data_insercao.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify(atividades_json)




@app.get('/atividades', tags=[atividades_tag],
         responses={"200": ListagemAtividadesSchema, "404": ErrorSchema})
def get_atividades(query: AtividadesBuscaSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    colaborador = query.colaborador
    logger.debug(f"Coletando dados sobre produto #{colaborador}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    if colaborador:
        atividades = session.query(Atividades).filter_by(colaborador=colaborador).all()
    else:
        atividades = session.query(Atividades).all()
    
    session.close()
    
    # Convertendo as atividades para um formato JSON
    atividades_json = []
    for atividade in atividades:
        atividades_json.append({
            'id': atividade.id,
            'tarefa': atividade.tarefa,
            'colaborador': atividade.colaborador,
            'status': atividade.status,
            'data_insercao': atividade.data_insercao.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify(atividades_json)
    # else:
    #     # se o produto não foi encontrado
    #     error_msg = "Produto não encontrado na base :/"
    #     logger.warning(f"Erro ao buscar produto '{colaborador}', {error_msg}")
    #     return {"mesage": error_msg}, 404
 


@app.delete('/atividades', tags=[atividades_tag],
            responses={"200": AtividadesDelSchema, "404": ErrorSchema})
def del_atividades(query: AtividadesBuscaSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    atividades_tarefa = unquote(unquote(query.tarefa))
    print(atividades_tarefa)
    logger.debug(f"Deletando dados sobre produto #{atividades_tarefa}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Atividades).filter(Atividades.tarefa == atividades_tarefa).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{atividades_tarefa}")
        return {"mesage": "Produto removido", "id": atividades_tarefa}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{atividades_tarefa}', {error_msg}")
        return {"mesage": error_msg}, 404
    






# @app.post('/colaborador', tags=[colaboradores_tag],
#           responses={"200": ColaboradoresViewSchema, "409": ErrorSchema, "400": ErrorSchema})
# def add_colaborador(form: ColaboradoresSchema):
#      """Adiciona um novo Colaborador à base de dados
#      """
#      colaboradores = Colaboradores(
#          nome=form.nome,
#          cargo=form.cargo)
#      logger.debug(f"Adicionando atividades de nome: '{colaboradores.nome}'")
#      try:
#          # criando conexão com a base
#          session = Session()
#          # adicionando produto
#          session.add(colaboradores)
#          # efetivando o camando de adição de novo item na tabela
#          session.commit()
#          logger.debug(f"Adicionado atividades de nome: '{colaboradores.nome}'")
#          return apresenta_colaborador(colaboradores), 200
    
#     except IntegrityError as e:
#         # como a duplicidade do nome é a provável razão do IntegrityError
#         #error_msg = "Produto de mesmo nome já salvo na base :/"
#         #logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
#         return {"mesage": error_msg}, 409
    
#     except Exception as e:
#             # caso um erro fora do previsto
#             error_msg = "Não foi possível salvar novo colaborador :/"
#             logger.warning(f"Erro ao adicionar colaborador '{colaboradores.nome}', {error_msg}")
#             return {"mesage": error_msg}, 400

