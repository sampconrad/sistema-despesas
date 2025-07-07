from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum
from datetime import datetime
import enum

from model.base import Base

class TipoDespesa(enum.Enum):
    CREDITO_FIXO = "CRÉDITO FIXO"
    CREDITO_PARCELADO = "CRÉDITO PARCELADO"
    PIX = "PIX"
    BOLETO = "BOLETO"

class Despesa(Base):
    __tablename__ = 'despesa'

    id = Column(Integer, primary_key=True)
    tipo = Column(Enum(TipoDespesa), nullable=False)
    titulo = Column(String(100), nullable=False)
    valor = Column(Float, nullable=False)
    dia_vencimento = Column(Integer, nullable=False)  # Dia do mês (1-31)
    parcelas = Column(Integer, nullable=True)
    paga = Column(Boolean, default=False)
    data_insercao = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Despesa(id={self.id}, tipo='{self.tipo.value}', titulo='{self.titulo}', valor={self.valor}, dia_vencimento={self.dia_vencimento}, parcelas={self.parcelas}, paga={self.paga})>"

    def __init__(self, tipo: TipoDespesa, titulo: str, valor: float, 
                 dia_vencimento: int, parcelas: int = None, paga: bool = False, data_insercao: datetime = None):
        """
        Cria uma Despesa

        Arguments:
            tipo: tipo da despesa (CRÉDITO FIXO, CRÉDITO PARCELADO, PIX, BOLETO)
            titulo: título da despesa
            valor: valor da despesa
            dia_vencimento: dia do mês (1-31) de vencimento do pagamento
            parcelas: quantidade de parcelas (apenas para CRÉDITO PARCELADO)
            paga: se a despesa foi paga ou não
            data_insercao: data de inserção da despesa
        """
        self.tipo = tipo
        self.titulo = titulo
        self.valor = valor
        self.dia_vencimento = dia_vencimento
        self.parcelas = parcelas
        self.paga = paga
        if data_insercao:
            self.data_insercao = data_insercao 