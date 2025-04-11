from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

app = FastAPI(
    title="Gerador de Contrato",
    version="1.0.0",
    description="API para gerar contrato em PDF a partir de dados enviados via JSON."
)

# Middleware para permitir requisições de qualquer origem (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretórios
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configuração do Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Modelo dos dados esperados no corpo da requisição
class ContratoData(BaseModel):
    tipo_contratante: str
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

# Rota principal para gerar o contrato em PDF
@app.post(
    "/gerar-contrato",
    response_model=None,  # Evita que o Swagger tente mostrar um modelo de resposta JSON
    summary="Gerar Contrato em PDF",
    description="Gera um contrato em PDF com base nos dados enviados e retorna o arquivo gerado."
)
def gerar_contrato(data: ContratoData):
    # Escolhe o template conforme o tipo do contratante
    template_file = (
        "contrato_template_juridico.html" if data.tipo_contratante == "juridica"
        else "contrato_template_fisico.html"
    )

    # Renderiza o HTML com os dados
    template = env.get_template(template_file)
    html_content = template.render(data=data)

    # Gera o PDF
    output_path = os.path.join(OUTPUT_DIR, "contrato.pdf")
    HTML(string=html_content).write_pdf(output_path)

    # Retorna o arquivo PDF
    return FileResponse(output_path, media_type="application/pdf", filename="contrato.pdf")
