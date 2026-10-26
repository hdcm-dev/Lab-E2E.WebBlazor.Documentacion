"""Verificación de la documentación: enlaces internos y forma de la ia-db.

Falla si un enlace relativo a un archivo de este repositorio no resuelve, o si la ia-db
no tiene la forma del Profile Knowledge-Indexing (entrada única con manifiesto e índices
numerados con propósito, fuente primaria y vigencia). Los enlaces que salen del
repositorio (a Lab-E2E.WebBlazor o a Lab-Documentos) y los que empiezan con «/», que en este
workspace parten de su raíz, no se pueden comprobar acá: se cuentan y se informan, no fallan. El presupuesto de líneas por índice es orientativo: avisa.
"""
import pathlib
import re
import sys
from urllib.parse import unquote

RAIZ = pathlib.Path(__file__).resolve().parents[2]
ENLACE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CERCO = re.compile(r"^\s*(```|~~~)")
PRESUPUESTO = 500

errores, avisos, externos = [], [], 0


def lineas_fuera_de_cercos(texto):
    dentro = False
    for n, linea in enumerate(texto.splitlines(), 1):
        if CERCO.match(linea):
            dentro = not dentro
            continue
        if not dentro:
            yield n, re.sub(r"`[^`]*`", "", linea)


for md in sorted(RAIZ.rglob("*.md")):
    if ".git" in md.parts:
        continue
    for n, linea in lineas_fuera_de_cercos(md.read_text(encoding="utf-8")):
        for destino in ENLACE.findall(linea):
            if re.match(r"^[a-z][a-z0-9+.-]*:", destino, re.I) or destino.startswith("#"):
                continue
            ruta = unquote(destino.split("#", 1)[0])
            if not ruta:
                continue
            if ruta.startswith("/"):
                externos += 1
                continue
            objetivo = (md.parent / ruta).resolve()
            if RAIZ not in objetivo.parents and objetivo != RAIZ:
                externos += 1
                continue
            if not objetivo.exists():
                errores.append(f"{md.relative_to(RAIZ)}:{n}: enlace roto → {destino}")

ia_db = RAIZ / "ia-db"
if ia_db.exists():
    entrada = ia_db / "README.md"
    if not entrada.exists():
        errores.append("ia-db/README.md no existe: la ia-db no tiene punto de entrada")
    elif "## Manifiesto de generación" not in entrada.read_text(encoding="utf-8"):
        errores.append("ia-db/README.md no tiene la sección «## Manifiesto de generación»")
    indices = sorted((ia_db / "indexes").glob("*.md"))
    if not indices:
        errores.append("ia-db/indexes/ no tiene índices")
    for indice in indices:
        nombre = indice.relative_to(RAIZ)
        m = re.match(r"^(\d{2})_", indice.name)
        if not m:
            errores.append(f"{nombre}: el nombre no empieza con NN_")
            continue
        texto = indice.read_text(encoding="utf-8")
        cabecera = "\n".join(texto.splitlines()[:25])
        if not texto.startswith(f"# {m.group(1)} "):
            errores.append(f"{nombre}: el título no empieza con «# {m.group(1)} »")
        for campo in ("**Propósito**", "**Fuente primaria**", "**Vigencia**"):
            if campo not in cabecera:
                errores.append(f"{nombre}: falta {campo} en la cabecera")
        total = len(texto.splitlines())
        if total > PRESUPUESTO:
            avisos.append(f"{nombre}: {total} líneas, sobre el presupuesto orientativo de {PRESUPUESTO}")

for a in avisos:
    print(f"::warning::{a}")
for e in errores:
    print(f"::error::{e}")
print(f"Enlaces fuera del repositorio, no comprobables acá: {externos}")
print(f"Resultado: {len(errores)} errores, {len(avisos)} avisos")
sys.exit(1 if errores else 0)
