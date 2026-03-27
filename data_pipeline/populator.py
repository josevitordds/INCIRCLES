import os
import json
import time
import requests
from dotenv import load_dotenv
from google import genai
import cloudinary
import cloudinary.uploader
from pdf2image import convert_from_path
from PIL import Image

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
BACKEND_URL = "http://localhost:8000/api/questoes/admin/importar"

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

client = genai.Client(api_key=GOOGLE_API_KEY)
DADOS_PROVA ={
    "olimpiada_sigla": "OBMEP",
    "ano": 2019,
    "fase": 1,
    "nivel": 3,
    "pdf_path": "provas/pf1n3-2019.pdf" 
}

DPI_CONVERSAO_PDF = 300

PROMPT_SISTEMA= """ Você é um sistema especialista em extração rigorosa de provas da OBMEP.
Analise a imagem desta página de prova e retorne ESTRITAMENTE um objeto JSON.

DIRETRIZES CRÍTICAS (Siga sob pena de falha sistêmica):
1. NÃO PULE NENHUMA QUESTÃO: Extraia absolutamente todas as questões visíveis na página. Verifique a numeração para garantir que a sequência está correta.
2. MATEMÁTICA EM LATEX: Qualquer símbolo matemático ($ \sqrt{x} $, frações, graus) deve ser convertido para LaTeX delimitado por '$'.
3. PRECISÃO CIRÚRGICA NAS IMAGENS:
   - Se a questão tiver figuras, gráficos ou tabelas, você DEVE detectá-las.
   - Forneça as coordenadas 'box_2d' [ymin, xmin, ymax, xmax] normalizadas de 0 a 1000.
   - Seja extremamente preciso para incluir a figura inteira, sem cortar as bordas.
   - Insira '{{URL_IMAGEM_AQUI}}' no enunciado exato onde a figura se aplica.
4. GABARITO: Marque 'is_correta' da alternativa 'A' como true como padrão de segurança.

Formato do JSON de saída esperado:
{
  "questoes": [
    {
      "numero_questao": 1,
      "enunciado": "Texto com LaTeX e tag {{URL_IMAGEM_AQUI}}.",
      "tipo": "objetiva",
      "alternativas": [
        {"letra": "A", "texto": "texto", "is_correta": true}
      ]
    }
  ],
  "imagens_detectadas": [
    {
      "associada_a_questao": 1,
      "box_2d": [150, 200, 400, 800] 
    }
  ]
}

Retorne APENAS o JSON puro, sem markdown ou explicações adicionais."""

def preparar_pastas_trabalho(dados_prova):
    nome_prova = f"{dados_prova['olimpiada_sigla']}_{dados_prova['ano']}_fase{dados_prova['fase']}_nivel{dados_prova['nivel']}"
    pasta_imagens = os.path.join("processadas", nome_prova, "recortes")
    os.makedirs(pasta_imagens, exist_ok=True)
    return pasta_imagens

def recortar_e_upar_imagem(imagem_pil, coords, num_questao, pasta_recortes):
    width, height = imagem_pil.size
    ymin, xmin, ymax, xmax = coords

    margem = 20 
    left = max(0, (xmin*width/1000) - margem)
    top = max(0, (ymin*height/1000) - margem)
    right = min(width, (xmax*width/1000) + margem)
    bottom = min(height, (ymax*height/1000) + margem)

    img_recortada = imagem_pil.crop((left, top, right, bottom))
    caminho_local= os.path.join(pasta_recortes, f"questao_{num_questao}.png")
    img_recortada.save(caminho_local)

    print(f"✂️ Recorte da Q{num_questao} salvo. Iniciando upload para Cloudinary...")
    try:
        res = cloudinary.uploader.upload(
            caminho_local,
            folder=f"olimpiadas/{DADOS_PROVA['olimpiada_sigla']}/{DADOS_PROVA['ano']}/fase{DADOS_PROVA['fase']}/nivel{DADOS_PROVA['nivel']}",
            public_id=f"questao_{num_questao}",
        )
        return res['secure_url']
    except Exception as e:
        print(f"❌ Erro no Cloudinary para a Q{num_questao}: {e}")
        return None 
    
def analisar_pagina(imagem_pil, num_pag):
    print(f"🧠 IA (Gemini 2.5 Pro) analisando página {num_pag}...")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[PROMPT_SISTEMA, imagem_pil]
        )
        texto = response.text.strip()
        
        if texto.startswith("```"): 
            texto = texto.strip("```json").strip("```")
            
        return json.loads(texto)
    except Exception as e:
        print(f"❌ Erro na IA ao analisar página {num_pag}: {e}")
        return {"questoes": [], "imagens_detectadas": []}

def executar_pipeline():
    if not os.path.exists(DADOS_PROVA["pdf_path"]):
        print(f"❌ Erro: PDF não encontrado em: {DADOS_PROVA['pdf_path']}")
        return

    pasta_recortes = preparar_pastas_trabalho(DADOS_PROVA)
    print("🔄 Convertendo PDF para imagens em alta resolução...")
    
    caminho_do_poppler = r"C:\Users\josev\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin" 
    imagens_paginas = convert_from_path(DADOS_PROVA["pdf_path"], dpi=DPI_CONVERSAO_PDF, poppler_path=caminho_do_poppler)
    
    questoes_finais = []

    for i, img_pagina in enumerate(imagens_paginas): 
        num_pag = i + 1 
        time.sleep(4) 
        
        dados = analisar_pagina(img_pagina, num_pag)
        questoes = dados.get("questoes", [])
        imagens = dados.get("imagens_detectadas", [])

        mapa_urls = {}
        for img_info in imagens:
            q_num = img_info["associada_a_questao"]
            url = recortar_e_upar_imagem(img_pagina, img_info["box_2d"], q_num, pasta_recortes)
            if url: 
                mapa_urls[q_num] = url

        for q in questoes:
            if q["numero_questao"] in mapa_urls:
                q["enunciado"] = q["enunciado"].replace("{{URL_IMAGEM_AQUI}}", mapa_urls[q["numero_questao"]])
            else:
                q["enunciado"] = q["enunciado"].replace("{{URL_IMAGEM_AQUI}}", "")
            questoes_finais.append(q)

    if questoes_finais:
        pacote = DADOS_PROVA.copy()
        del pacote["pdf_path"]
        pacote["questoes"] = questoes_finais

        with open("backup_nova_prova.json", "w", encoding="utf-8") as f:
            json.dump(pacote, f, indent=4, ensure_ascii=False)
            
        resposta = input(f"\n✅ {len(questoes_finais)} questões geradas. Enviar ao Banco de Dados (FastAPI) agora? (s/n): ")
        if resposta.lower() == 's':
            print("🚀 Enviando pacote para o backend...")
            res = requests.post(BACKEND_URL, json=pacote)
            if res.status_code == 200:
                print("🎉 Sucesso! Resposta do Servidor:", res.json())
            else:
                print(f"❌ Erro no servidor ({res.status_code}):", res.text)
    else:
        print("⚠ Nenhuma questão extraída.")

if __name__ == "__main__":
    executar_pipeline()