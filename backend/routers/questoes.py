# backend/routers/questoes.py
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from typing import Optional
import models
import schemas
from database import get_session
from fastapi import HTTPException

router = APIRouter(
    prefix="/api/questoes",
    tags=["Questões"]
)

@router.post("/admin/importar")
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

@router.get("/")
def listar_questoes(
    pagina: int = Query(1, description="Número da página (começa em 1)"),
    limite: int = Query(10, description="Quantidade de questões por página"),
    ano: Optional[int] = Query(None, description="Filtrar por ano da prova"),
    fase: Optional[int] = Query(None, description="Filtrar por fase (1 ou 2)"),
    nivel: Optional[int] = Query(None, description="Filtrar por nível (1, 2 ou 3)"),
    session: Session = Depends(get_session)
):
    statement = select(models.Questao).join(models.Prova)

    if ano:
        statement = statement.where(models.Prova.ano == ano)
    if fase:
        statement = statement.where(models.Prova.fase == fase)
    if nivel:
        statement = statement.where(models.Prova.nivel == nivel)

    total_questoes = len(session.exec(statement).all())

    saltar = (pagina - 1) * limite
    statement = statement.offset(saltar).limit(limite)
    
    questoes = session.exec(statement).all()
    
    resultado_questoes = []
    for q in questoes:
        resultado_questoes.append({
            "id": q.id,
            "numero": q.numero_questao,
            "enunciado": q.enunciado,
            "imagem_url": q.imagem_url, 
            "alternativas": [
                {"id": alt.id, "letra": alt.letra, "texto": alt.texto} 
                for alt in q.alternativas
            ]
        })
    
    return {
        "total": total_questoes,
        "pagina_atual": pagina,
        "total_paginas": (total_questoes + limite - 1) // limite,
        "questoes": resultado_questoes
    }

@router.post("/{questao_id}/responder")
def responder_questao(
    questao_id: int, 
    resposta: schemas.RespostaUsuario, 
    session: Session = Depends(get_session)
):
    questao = session.exec(select(models.Questao).where(models.Questao.id == questao_id)).first()
    if not questao:
        raise HTTPException(status_code=404, detail="Questão não encontrada")

    alt_correta = session.exec(
        select(models.Alternativa).where(
            models.Alternativa.questao_id == questao_id,
            models.Alternativa.is_correta == True
        )
    ).first()

    if not alt_correta:
        raise HTTPException(status_code=500, detail="Gabarito não cadastrado para esta questão")

    acertou = (resposta.alternativa_id == alt_correta.id)

    return {
        "acertou": acertou,
        "alternativa_correta_id": alt_correta.id,
        "letra_correta": alt_correta.letra,
        "mensagem": "Resposta correta!" if acertou else "Resposta incorreta."
    }