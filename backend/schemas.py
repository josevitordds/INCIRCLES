from pydantic import BaseModel
from typing import List, Optional  

class AlternativaImport(BaseModel):
    letra: str
    texto: str
    is_correta: bool

class QuestaoImport(BaseModel):
    numero_questao: int
    enunciado: str
    tipo: str = "objetiva"
    alternativas: List[AlternativaImport]

class LoteImportacao(BaseModel):
    olimpiada_sigla: str
    ano: int
    fase: int
    nivel: int
    questoes: List[QuestaoImport]

class RespostaUsuario(BaseModel):
    alternativa_id: int

class UsuarioCreate(BaseModel):
    nome_completo: str
    email: str
    senha: str
    olimpiada_foco: Optional[str] = None

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome_completo: str
    email: str
    olimpiada_foco: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str