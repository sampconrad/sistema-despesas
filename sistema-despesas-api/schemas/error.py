from pydantic import BaseModel, Field


class ErrorSchema(BaseModel):
    """ Define como uma mensagem de erro será representada
    
    **Códigos de Status:**
    - 400: Bad Request - Dados inválidos ou malformados
    - 404: Not Found - Recurso não encontrado
    - 409: Conflict - Conflito de dados (ex: violação de integridade)
    - 500: Internal Server Error - Erro interno do servidor
    """
    message: str = Field(..., example="Erro ao processar a requisição", description="Mensagem descritiva do erro")
