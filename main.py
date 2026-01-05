from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

API_KEY = "minha_chave_secreta"

class Lead(BaseModel):
    nome: str
    telefone: str
    cidade: str
    interesse: str
    origem: str
    consentimento: bool

leads = []

@app.post("/leads")
def criar_lead(lead: Lead, x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Chave inválida")
    if not lead.consentimento:
        raise HTTPException(status_code=400, detail="Sem consentimento")

    leads.append({
        **lead.dict(),
        "score": 70,
        "criado_em": datetime.now()
    })
    return {"status": "ok"}

@app.get("/leads")
def listar_leads(score_min: int = 0, x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Chave inválida")
    return leads
