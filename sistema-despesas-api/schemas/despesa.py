from pydantic import BaseModel, validator, Field
from typing import Optional, List, Union
from datetime import datetime
from model.despesa import Despesa, TipoDespesa


class DespesaSchema(BaseModel):
    """ Define como uma nova despesa a ser inserida deve ser representada
    
    **Validações:**
    - tipo: Deve ser um dos valores válidos (CRÉDITO FIXO, CRÉDITO PARCELADO, PIX, BOLETO)
    - valor: Deve ser maior que zero
    - dia_vencimento: Deve estar entre 1 e 31
    - parcelas: Deve ser positivo (apenas para CRÉDITO PARCELADO)
    """
    tipo: str = Field(..., example="CRÉDITO FIXO", description="Tipo da despesa")
    titulo: str = Field(..., example="Cartão de Crédito Nubank", description="Título da despesa")
    valor: float = Field(..., example=1500.75, description="Valor da despesa")
    dia_vencimento: int = Field(..., example=15, description="Dia do mês de vencimento (1-31)")
    parcelas: Optional[int] = Field(None, example=12, description="Quantidade de parcelas restantes (apenas para CRÉDITO PARCELADO)")
    paga: bool = Field(False, example=False, description="Se a despesa foi paga")

    @validator('tipo')
    def validate_tipo(cls, v):
        tipos_validos = ["CRÉDITO FIXO", "CRÉDITO PARCELADO", "PIX", "BOLETO"]
        if v not in tipos_validos:
            raise ValueError(f'Tipo deve ser um dos seguintes: {tipos_validos}')
        return v

    @validator('parcelas', pre=True)
    def validate_parcelas(cls, v):
        if v is None or v == "null" or v == "":
            return None
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                raise ValueError('Parcelas deve ser um número inteiro')
        if isinstance(v, int):
            if v <= 0:
                raise ValueError('Parcelas deve ser um número positivo')
            return v
        return v

    @validator('valor')
    def validate_valor(cls, v):
        if v <= 0:
            raise ValueError('Valor deve ser maior que zero')
        return v

    @validator('dia_vencimento')
    def validate_dia_vencimento(cls, v):
        if v < 1 or v > 31:
            raise ValueError('Dia de vencimento deve ser entre 1 e 31')
        return v


class DespesaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por ID
    """
    id: int = Field(..., example=1, description="ID da despesa")


class DespesaAtualizaSchema(BaseModel):
    """ Define como uma despesa deve ser atualizada
    
    **Validações:**
    - id: ID obrigatório da despesa a ser atualizada
    - tipo: Deve ser um dos valores válidos (se fornecido)
    - valor: Deve ser maior que zero (se fornecido)
    - dia_vencimento: Deve estar entre 1 e 31 (se fornecido)
    - parcelas: Deve ser positivo (apenas para CRÉDITO PARCELADO, se fornecido)
    
    **Regras de Negócio:**
    - Se o tipo for alterado para algo diferente de CRÉDITO PARCELADO, parcelas será zerado
    - Pelo menos um campo opcional deve ser fornecido para atualização
    """
    id: int = Field(..., example=1, description="ID da despesa")
    tipo: Optional[str] = Field(None, example="CRÉDITO PARCELADO", description="Tipo da despesa")
    titulo: Optional[str] = Field(None, example="Cartão de Crédito Itaú", description="Título da despesa")
    valor: Optional[float] = Field(None, example=2000.50, description="Valor da despesa")
    dia_vencimento: Optional[int] = Field(None, example=20, description="Dia do mês de vencimento (1-31)")
    parcelas: Optional[int] = Field(None, example=6, description="Quantidade de parcelas restantes")
    paga: Optional[bool] = Field(None, example=True, description="Se a despesa foi paga")

    @validator('tipo')
    def validate_tipo(cls, v):
        if v is not None:
            tipos_validos = ["CRÉDITO FIXO", "CRÉDITO PARCELADO", "PIX", "BOLETO"]
            if v not in tipos_validos:
                raise ValueError(f'Tipo deve ser um dos seguintes: {tipos_validos}')
        return v

    @validator('parcelas', pre=True)
    def validate_parcelas(cls, v):
        if v is None or v == "null" or v == "":
            return None
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                raise ValueError('Parcelas deve ser um número inteiro')
        if isinstance(v, int):
            if v <= 0:
                raise ValueError('Parcelas deve ser um número positivo')
            return v
        return v

    @validator('valor')
    def validate_valor(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Valor deve ser maior que zero')
        return v

    @validator('dia_vencimento')
    def validate_dia_vencimento(cls, v):
        if v is not None and (v < 1 or v > 31):
            raise ValueError('Dia de vencimento deve ser entre 1 e 31')
        return v


class ListagemDespesasSchema(BaseModel):
    """ Define como uma listagem de despesas será retornada.
    """
    despesas: List[dict] = Field(..., example=[
        {
            "id": 1,
            "tipo": "CRÉDITO FIXO",
            "titulo": "Cartão de Crédito Nubank",
            "valor": 1500.75,
            "parcelas": None,
            "dia_vencimento": 15,
            "paga": False,
            "data_insercao": "05/07/2025 19:17"
        },
        {
            "id": 2,
            "tipo": "CRÉDITO PARCELADO",
            "titulo": "Financiamento Carro",
            "valor": 2500.00,
            "parcelas": 12,
            "dia_vencimento": 10,
            "paga": False,
            "data_insercao": "05/07/2025 19:20"
        }
    ], description="Lista de despesas")


def apresenta_despesas(despesas: List[Despesa]):
    """ Retorna uma representação das despesas seguindo o schema definido.
    """
    result = []
    for despesa in despesas:
        result.append({
            "id": despesa.id,
            "tipo": despesa.tipo.value,
            "titulo": despesa.titulo,
            "valor": despesa.valor,
            "parcelas": despesa.parcelas,
            "dia_vencimento": despesa.dia_vencimento,
            "paga": despesa.paga,
            "data_insercao": despesa.data_insercao.strftime("%d/%m/%Y %H:%M")
        })

    return {"despesas": result}


class DespesaViewSchema(BaseModel):
    """ Define como uma despesa será retornada.
    """
    id: int = Field(..., example=1, description="ID da despesa")
    tipo: str = Field(..., example="CRÉDITO FIXO", description="Tipo da despesa")
    titulo: str = Field(..., example="Cartão de Crédito Nubank", description="Título da despesa")
    valor: float = Field(..., example=1500.75, description="Valor da despesa")
    parcelas: Optional[int] = Field(None, example=None, description="Quantidade de parcelas restantes")
    dia_vencimento: int = Field(..., example=15, description="Dia do mês de vencimento")
    paga: bool = Field(..., example=False, description="Se a despesa foi paga")
    data_insercao: str = Field(..., example="05/07/2025 19:17", description="Data de inserção da despesa")


class DespesaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str = Field(..., example="Despesa removida", description="Mensagem de confirmação")
    id: int = Field(..., example=1, description="ID da despesa removida")


def apresenta_despesa(despesa: Despesa):
    """ Retorna uma representação da despesa seguindo o schema definido em
        DespesaViewSchema.
    """
    return {
        "id": despesa.id,
        "tipo": despesa.tipo.value,
        "titulo": despesa.titulo,
        "valor": despesa.valor,
        "parcelas": despesa.parcelas,
        "dia_vencimento": despesa.dia_vencimento,
        "paga": despesa.paga,
        "data_insercao": despesa.data_insercao.strftime("%d/%m/%Y %H:%M")
    } 