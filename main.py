from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class ContratoData(BaseModel):
    tipo_contratante: str  # "juridica" ou "fisica"
    contratante_nome: str
    contratante_cnpj: str | None = None
    contratante_endereco: str
    contratada_nome: str
    contratada_cnpj: str
    contratada_endereco: str
    descricao_servico: str
    valor_servico: str
    tem_gastos_extras: bool
    gastos_detalhados: str | None = None
    valor_total: str
    data_contrato: str
    nome_testemunha_contratante: str
    nome_testemunha_contratada: str

@app.get("/")
def status():
    return {"message": "API do Gerador de Contrato está online."}

@app.post("/gerar-contrato")
def gerar_contrato(data: ContratoData):
    template_file = (
        "contrato_template_juridico.html"
        if data.tipo_contratante == "juridica"
        else "contrato_template_fisico.html"
    )
    template = env.get_template(template_file)
    html_content = template.render(data=data)

    output_path = os.path.join(OUTPUT_DIR, "contrato.pdf")
    HTML(string=html_content).write_pdf(output_path)

    return FileResponse(output_path, media_type="application/pdf", filename="contrato.pdf")
