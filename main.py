from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

import os

app = FastAPI()

# Diretório de templates e saída
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configura Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template("contrato_template.html")

# Modelo de dados
class ContratoInput(BaseModel):
    contratante_nome: str
    contratante_cnpj: str
    contratante_endereco: str
    contratada_nome: str
    contratada_cnpj: str
    contratada_endereco: str
    valor: str
    datas: str

@app.post("/gerar-contrato")
async def gerar_contrato(dados: ContratoInput):
    html_content = template.render(dados.dict())
    output_path = os.path.join(OUTPUT_DIR, f"contrato_{dados.contratante_nome}.pdf")
    HTML(string=html_content).write_pdf(output_path)
    return FileResponse(output_path, media_type='application/pdf', filename="contrato_gerado.pdf")

@app.get("/")
async def root():
    return JSONResponse({"message": "API do Gerador de Contrato está online."})
