from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
import models
import schemas 

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"mensagem": "API do Sistema de Questões rodando!"}

@app.post("/api/admin/questoes/importar")
def importar_questoes(lote: schemas.LoteImportacao, session: Session = Depends(get_session)):
    
    olimpiada = session.exec(select(models.Olimpiada).where(models.Olimpiada.sigla == lote.olimpiada_sigla)).first()
    if not olimpiada:
        olimpiada = models.Olimpiada(sigla=lote.olimpiada_sigla, nome_completo=f"Olimpíada {lote.olimpiada_sigla}")
        session.add(olimpiada)
        session.commit()
        session.refresh(olimpiada)

    prova = session.exec(select(models.Prova).where(
        models.Prova.olimpiada_id == olimpiada.id,
        models.Prova.ano == lote.ano,
        models.Prova.fase == lote.fase,
        models.Prova.nivel == lote.nivel
    )).first()
    
    if not prova:
        prova = models.Prova(olimpiada_id=olimpiada.id, ano=lote.ano, fase=lote.fase, nivel=lote.nivel)
        session.add(prova)
        session.commit()
        session.refresh(prova)

    qtd_inseridas = 0
    for q_data in lote.questoes:
        questao_existente = session.exec(select(models.Questao).where(
            models.Questao.prova_id == prova.id, 
            models.Questao.numero_questao == q_data.numero_questao
        )).first()
        
        if questao_existente:
            continue

        nova_questao = models.Questao(
            prova_id=prova.id,
            numero_questao=q_data.numero_questao,
            enunciado=q_data.enunciado,
            tipo=q_data.tipo
        )
        session.add(nova_questao)
        session.commit()
        session.refresh(nova_questao)

        for alt_data in q_data.alternativas:
            nova_alt = models.Alternativa(
                questao_id=nova_questao.id,
                letra=alt_data.letra,
                texto=alt_data.texto,
                is_correta=alt_data.is_correta
            )
            session.add(nova_alt)
        
        qtd_inseridas += 1

    session.commit()
    return {"status": "sucesso", "mensagem": f"{qtd_inseridas} questões salvas no banco de dados!"}