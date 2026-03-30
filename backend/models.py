from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class QuestaoAssunto(SQLModel, table=True):
    questao_id: Optional[int]= Field(
        default=None, foreign_key="questao.id", primary_key=True
    )
    assunto_id: Optional[int] = Field(
        default=None, foreign_key="assunto.id", primary_key=True
    )

class Assunto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True)

    questoes: List["Questao"] = Relationship(
        back_populates="assuntos", link_model=QuestaoAssunto
    )

class Olimpiada(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sigla: str = Field(index=True)
    nome_completo: str

    provas: List["Prova"] = Relationship(back_populates="olimpiada")

class Prova(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ano: int
    fase: int
    nivel: int

    olimpiada_id: Optional[int] = Field(default=None, foreign_key="olimpiada.id")
    olimpiada: Optional[Olimpiada] = Relationship(back_populates="provas")
    questoes: List["Questao"] = Relationship(back_populates="prova")

class Questao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    numero_questao: int
    enunciado: str
    imagem_url: Optional[str] = None
    tipo: str
    gabarito_comentado: Optional[str] = None

    prova_id: Optional[int] = Field(default=None, foreign_key="prova.id")
    prova: Optional[Prova] = Relationship(back_populates="questoes")
    alternativas: List["Alternativa"] = Relationship(back_populates="questao")

    assuntos: List[Assunto] = Relationship(
        back_populates="questoes", link_model=QuestaoAssunto
    )

class Alternativa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    letra: str
    texto: str
    is_correta: bool = Field(default=False)

    questao_id: Optional[int] = Field(default=None, foreign_key="questao.id")
    questao: Optional[Questao] = Relationship(back_populates="alternativas")

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome_completo: str
    email: str = Field(unique=True, index=True)
    senha_hash: Optional[str] = None 
    olimpiada_foco: Optional[str] = None
    is_google_auth: bool = Field(default=False) 