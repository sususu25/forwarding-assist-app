from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

BASE_DIR     = Path(__file__).parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
OUTPUT_DIR   = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def generate_pdf(data: dict) -> str:
    """data(dict) => PDF 경로(str)"""
    tpl_name = "ci.html" if data["doc_type"] == "CI" else "pl.html"   # <<<
    html_str = env.get_template(tpl_name).render(**data)

    file_name  = f'{data["doc_type"]}_{datetime.utcnow():%Y%m%d_%H%M%S}.pdf'
    final_path = OUTPUT_DIR / file_name
    HTML(string=html_str).write_pdf(str(final_path))
    return str(final_path)
