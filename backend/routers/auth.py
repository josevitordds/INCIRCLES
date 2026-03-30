# backend/routers/auth.py
import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
import bcrypt 
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

import models, schemas
from database import get_session

load_dotenv()

router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticação"]
)

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("⚠️ ALERTA FATAL: A variável SECRET_KEY não foi encontrada no arquivo .env!")

ALGORITHM = "HS256"

@router.post("/cadastro", response_model=schemas.UsuarioResponse)
def cadastrar_usuario(usuario: schemas.UsuarioCreate, session: Session = Depends(get_session)):
    usuario_existente = session.exec(select(models.Usuario).where(models.Usuario.email == usuario.email)).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    salt = bcrypt.gensalt()
    senha_criptografada = bcrypt.hashpw(usuario.senha.encode('utf-8'), salt).decode('utf-8')

    novo_usuario = models.Usuario(
        nome_completo=usuario.nome_completo,
        email=usuario.email,
        senha_hash=senha_criptografada,
        olimpiada_foco=usuario.olimpiada_foco
    )
    
    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)
    
    return novo_usuario

@router.post("/login", response_model=schemas.Token)
def login(dados_login: schemas.UsuarioLogin, session: Session = Depends(get_session)):
    usuario = session.exec(select(models.Usuario).where(models.Usuario.email == dados_login.email)).first()
    
    if not usuario or not usuario.senha_hash:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
        
    senha_correta = bcrypt.checkpw(
        dados_login.senha.encode('utf-8'), 
        usuario.senha_hash.encode('utf-8')
    )
    
    if not senha_correta:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

    expiracao = datetime.utcnow() + timedelta(days=7)
    token_dados = {"sub": str(usuario.id), "exp": expiracao}
    token = jwt.encode(token_dados, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}