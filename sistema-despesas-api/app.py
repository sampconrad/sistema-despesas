from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from model import Session, Despesa, TipoDespesa
from logger import logger
from schemas import *
from flask_cors import CORS
from datetime import datetime
import traceback

info = Info(
    title="API de Despesas Mensais",
    version="1.0.0",
    description="""
API PARA GERENCIAMENTO DE DESPESAS MENSAIS

Funcionalidades principais:
- Criar despesas com diferentes tipos (CRÉDITO FIXO, CRÉDITO PARCELADO, PIX, BOLETO)
- Listar todas as despesas cadastradas
- Buscar despesa específica por ID
- Atualizar despesas existentes
- Remover despesas da base de dados

Tipos de Despesa:
- CRÉDITO FIXO: Despesas recorrentes com valor fixo
- CRÉDITO PARCELADO: Despesas parceladas com controle de parcelas restantes
- PIX: Pagamentos via PIX
- BOLETO: Pagamentos via boleto bancário

Códigos de Status HTTP:
- 200: Sucesso - Operação realizada com sucesso
- 400: Bad Request - Dados inválidos ou malformados
- 404: Not Found - Recurso não encontrado
- 409: Conflict - Conflito de dados (ex: violação de integridade)
- 500: Internal Server Error - Erro interno do servidor

Formato de Dados:
- Entrada: FormData (multipart/form-data)
- Saída: JSON
- Valores monetários: Float com duas casas decimais
- Datas: Formato brasileiro (dd/mm/yyyy HH:MM)
"""
)
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
documentacao_tag = Tag(name="Documentação", description="Acesso à documentação interativa da API (Swagger, ReDoc, RapiDoc)")
despesa_tag = Tag(name="Despesa", description="Operações CRUD para gerenciamento de despesas mensais: criar, listar, buscar, atualizar e remover")

@app.get('/', tags=[documentacao_tag])
def home():
    """Redireciona para a documentação interativa da API.
    
    **Método HTTP:** GET
    
    **Retorna:** Redirecionamento para /openapi onde é possível escolher entre:
    - Swagger UI: Interface interativa para testar a API
    - ReDoc: Documentação em formato mais legível
    - RapiDoc: Interface alternativa para documentação
    """
    return redirect('/openapi')

# ==================== ROTAS DE DESPESAS ====================

@app.post('/despesa', tags=[despesa_tag],
          responses={"200": DespesaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_despesa(form: DespesaSchema):
    """Adiciona uma nova despesa mensal à base de dados.
    
    **Método HTTP:** POST
    
    **Parâmetros obrigatórios:**
    - tipo: Tipo da despesa (CRÉDITO FIXO, CRÉDITO PARCELADO, PIX, BOLETO)
    - titulo: Título/descrição da despesa
    - valor: Valor da despesa (deve ser maior que zero)
    - dia_vencimento: Dia do mês de vencimento (1-31)
    
    **Parâmetros opcionais:**
    - parcelas: Quantidade de parcelas restantes (apenas para CRÉDITO PARCELADO)
    - paga: Status de pagamento (padrão: False)
    
    **Retorna:** Despesa criada com ID e data de inserção
    """
    try:
        # Converter string para enum
        tipo_enum = TipoDespesa(form.tipo)
        
        despesa = Despesa(
            tipo=tipo_enum,
            titulo=form.titulo,
            valor=form.valor,
            dia_vencimento=form.dia_vencimento,
            parcelas=form.parcelas,
            paga=form.paga
        )
        logger.debug(f"Adicionando despesa: '{despesa.titulo}'")
        
        session = Session()
        session.add(despesa)
        session.commit()
        logger.debug(f"Adicionada despesa: '{despesa.titulo}'")
        return apresenta_despesa(despesa), 200
        
    except IntegrityError as e:
        error_msg = "Erro de integridade ao adicionar despesa"
        logger.warning(f"Erro ao adicionar despesa, {error_msg}: {str(e)}")
        return {"message": error_msg}, 409
        
    except Exception as e:
        error_msg = "Não foi possível salvar nova despesa"
        logger.error(f"Erro ao adicionar despesa: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"message": error_msg}, 400

@app.get('/despesas', tags=[despesa_tag],
         responses={"200": ListagemDespesasSchema, "500": ErrorSchema})
def get_despesas():
    """Lista todas as despesas mensais cadastradas.
    
    **Método HTTP:** GET
    
    **Parâmetros:** Nenhum
    
    **Retorna:** Lista de todas as despesas com seus detalhes completos
    """
    try:
        logger.debug(f"Coletando despesas")
        session = Session()
        despesas = session.query(Despesa).all()
        if not despesas:
            return {"despesas": []}, 200
        else:
            logger.debug(f"%d despesas encontradas" % len(despesas))
            return apresenta_despesas(despesas), 200
    except Exception as e:
        logger.error(f"Erro ao listar despesas: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"message": "Erro interno do servidor"}, 500

@app.get('/despesa', tags=[despesa_tag],
         responses={"200": DespesaViewSchema, "404": ErrorSchema, "500": ErrorSchema})
def get_despesa(query: DespesaBuscaSchema):
    """Busca uma despesa específica pelo ID.
    
    **Método HTTP:** GET
    
    **Parâmetros de consulta:**
    - id: ID único da despesa (obrigatório)
    
    **Retorna:** Detalhes completos da despesa encontrada
    """
    try:
        despesa_id = query.id
        logger.debug(f"Coletando dados sobre despesa #{despesa_id}")
        session = Session()
        despesa = session.query(Despesa).filter(Despesa.id == despesa_id).first()
        if not despesa:
            error_msg = "Despesa não encontrada na base"
            logger.warning(f"Erro ao buscar despesa #{despesa_id}, {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(f"Despesa encontrada: '{despesa.titulo}'")
            return apresenta_despesa(despesa), 200
    except Exception as e:
        logger.error(f"Erro ao buscar despesa: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"message": "Erro interno do servidor"}, 500

@app.put('/despesa', tags=[despesa_tag],
         responses={"200": DespesaViewSchema, "404": ErrorSchema, "400": ErrorSchema, "500": ErrorSchema})
def update_despesa(form: DespesaAtualizaSchema):
    """Atualiza uma despesa existente na base de dados.
    
    **Método HTTP:** PUT
    
    **Parâmetros obrigatórios:**
    - id: ID da despesa a ser atualizada
    
    **Parâmetros opcionais (pelo menos um deve ser fornecido):**
    - tipo: Novo tipo da despesa
    - titulo: Novo título da despesa
    - valor: Novo valor da despesa
    - dia_vencimento: Novo dia de vencimento
    - parcelas: Nova quantidade de parcelas (apenas para CRÉDITO PARCELADO)
    - paga: Novo status de pagamento
    
    **Regras de Negócio:**
    - Se o tipo for alterado para algo diferente de CRÉDITO PARCELADO, parcelas será zerado
    - Para despesas do tipo CRÉDITO PARCELADO: quando marcada como paga, o número de parcelas é reduzido em 1
    
    **Retorna:** Despesa atualizada com todos os dados
    """
    try:
        despesa_id = form.id
        logger.debug(f"Atualizando despesa #{despesa_id}")
        session = Session()
        despesa = session.query(Despesa).filter(Despesa.id == despesa_id).first()
        if not despesa:
            error_msg = "Despesa não encontrada na base"
            logger.warning(f"Erro ao atualizar despesa #{despesa_id}, {error_msg}")
            return {"message": error_msg}, 404
        
        if form.tipo is not None:
            despesa.tipo = TipoDespesa(form.tipo)
            # Se o tipo não for CRÉDITO PARCELADO, zera parcelas
            if form.tipo != 'CRÉDITO PARCELADO':
                despesa.parcelas = None
        if form.titulo is not None:
            despesa.titulo = form.titulo
        if form.valor is not None:
            despesa.valor = form.valor
        if form.dia_vencimento is not None:
            despesa.dia_vencimento = form.dia_vencimento
        if form.parcelas is not None and (form.tipo == 'CRÉDITO PARCELADO' or despesa.tipo.value == 'CRÉDITO PARCELADO'):
            despesa.parcelas = form.parcelas
        if form.paga is not None:
            # Reduzindo número de parcelas quando despesa do tipo CRÉDITO PARCELADO é marcada como paga
            if form.paga and not despesa.paga and despesa.tipo.value == 'CRÉDITO PARCELADO' and despesa.parcelas is not None and despesa.parcelas > 0:
                despesa.parcelas = despesa.parcelas - 1
                logger.debug(f"Parcela paga para despesa #{despesa_id}. Parcelas restantes: {despesa.parcelas}")
            
            despesa.paga = form.paga
        
        session.commit()
        logger.debug(f"Despesa #{despesa_id} atualizada com sucesso")
        return apresenta_despesa(despesa), 200
        
    except Exception as e:
        error_msg = "Não foi possível atualizar a despesa"
        logger.error(f"Erro ao atualizar despesa: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"message": error_msg}, 400

@app.delete('/despesa', tags=[despesa_tag],
            responses={"200": DespesaDelSchema, "404": ErrorSchema, "500": ErrorSchema})
def del_despesa(query: DespesaBuscaSchema):
    """Remove uma despesa da base de dados.
    
    **Método HTTP:** DELETE
    
    **Parâmetros de consulta:**
    - id: ID da despesa a ser removida (obrigatório)
    
    **Retorna:** Confirmação da remoção com ID da despesa removida
    """
    try:
        despesa_id = query.id
        logger.debug(f"Deletando dados sobre despesa #{despesa_id}")
        session = Session()
        count = session.query(Despesa).filter(Despesa.id == despesa_id).delete()
        session.commit()
        if count:
            logger.debug(f"Deletada despesa #{despesa_id}")
            return {"message": "Despesa removida", "id": despesa_id}
        else:
            error_msg = "Despesa não encontrada na base"
            logger.warning(f"Erro ao deletar despesa #{despesa_id}, {error_msg}")
            return {"message": error_msg}, 404
    except Exception as e:
        logger.error(f"Erro ao deletar despesa: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"message": "Erro interno do servidor"}, 500
