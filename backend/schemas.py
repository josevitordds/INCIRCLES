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