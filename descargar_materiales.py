#!/usr/bin/env python3
"""
descargar_materiales.py
=======================
Descarga las presentaciones (PDF) del aula virtual y copia los notebooks
del repo del profesor (mattbarreto/ifts24-lab-pdi-2026) a las carpetas LAB.

Requisitos:
    pip install requests gdown

Uso:
    cd C:\\Users\\Cristian\\Desktop\\repo\\greco-cristian-pdi-1c-2026
    python descargar_materiales.py
"""

import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

import requests

try:
    import gdown
except ImportError:
    print("Instalando gdown...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown", "-q"])
    import gdown

# ─── Raíz del repo ───────────────────────────────────────────────────────────
REPO = Path(__file__).parent.resolve()

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0"})


# ─── Helpers ─────────────────────────────────────────────────────────────────

def ensure(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def download_slides_pdf(slides_id: str, dest: Path, label: str):
    """Google Slides → PDF"""
    url = f"https://docs.google.com/presentation/d/{slides_id}/export/pdf"
    _download_url(url, dest, label)


def download_doc_pdf(doc_id: str, dest: Path, label: str):
    """Google Docs → PDF"""
    url = f"https://docs.google.com/document/d/{doc_id}/export?format=pdf"
    _download_url(url, dest, label)


def _download_url(url: str, dest: Path, label: str):
    if dest.exists():
        print(f"  [OK] ya existe: {dest.name}")
        return
    print(f"  Descargando {label} …")
    try:
        r = SESSION.get(url, timeout=30, stream=True)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  [OK] {dest.name}")
    except Exception as e:
        print(f"  [ERROR] {label}: {e}")


def download_drive_zip(file_id: str, dest: Path, label: str):
    """Google Drive → cualquier archivo"""
    if dest.exists():
        print(f"  [OK] ya existe: {dest.name}")
        return
    print(f"  Descargando {label} …")
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        gdown.download(url, str(dest), quiet=False, fuzzy=True)
        print(f"  [OK] {dest.name}")
    except Exception as e:
        print(f"  [ERROR] {label}: {e}")


# ─── Semana 1 ────────────────────────────────────────────────────────────────
def semana_01():
    print("\n── Semana 01 ──")
    teo = REPO / "001" / "001 - TEO"
    ensure(teo)
    download_slides_pdf(
        "1ls5u25Pyt6WNhWYQsIvQT51f-TilbD2iHFcjBN9iOq8",
        teo / "Semana01_TEO_Presentacion.pdf",
        "Semana 1 TEO – Presentación"
    )
    pra = REPO / "001" / "001 - PRA"
    ensure(pra)
    download_slides_pdf(
        "1GjL2TIsERrSeffuv0bDA3VlFfRsabs0a3CjdyLFLxNQ",
        pra / "Semana01_PRA_Presentacion.pdf",
        "Semana 1 PRA – Presentación"
    )


# ─── Semana 2 ────────────────────────────────────────────────────────────────
def semana_02():
    print("\n── Semana 02 ──")
    teo = REPO / "002" / "002 - TEO"
    ensure(teo)
    download_slides_pdf(
        "1W6jqIFq-q1e5Ew42B_GOsZWjfrQ8QC3W9WVRphF60nQ",
        teo / "Semana02_TEO_Presentacion.pdf",
        "Semana 2 TEO – Presentación"
    )


# ─── Semana 4 ────────────────────────────────────────────────────────────────
def semana_04():
    print("\n── Semana 04 ──")
    teo = REPO / "004" / "004 - TEO"
    ensure(teo)
    download_slides_pdf(
        "1r-aI7s9_nUH93WpzK1fT1L5sgqDBYyam7S8Mr8xIiXQ",
        teo / "Semana04_TEO_Presentacion.pdf",
        "Semana 4 TEO – Presentación"
    )


# ─── Semana 6 ────────────────────────────────────────────────────────────────
def semana_06():
    print("\n── Semana 06 ──")
    teo = REPO / "006_fotografia_digital" / "006 - TEO"
    ensure(teo)
    download_slides_pdf(
        "1dCDqdHGaz7Z-hl3NdEhj9FmwFy_84piJ4DV1TmWajHE",
        teo / "Semana06_TEO_Presentacion.pdf",
        "Semana 6 TEO – Presentación"
    )


# ─── Semana 7 ────────────────────────────────────────────────────────────────
def semana_07():
    print("\n── Semana 07 ──")
    teo = REPO / "007" / "007 - TEO"
    ensure(teo)
    download_slides_pdf(
        "1QBSlce-DIF0now5P0YHmPYt4aFwiDKZ6xjmUqxcGHV4",
        teo / "Semana07_TEO_Presentacion.pdf",
        "Semana 7 TEO – Presentación"
    )
    pra = REPO / "007" / "007 - PRA"
    ensure(pra)
    download_doc_pdf(
        "1pr-bwzj2fJNmrYeYrvFqif1O708x7rH3rwvo-m2kAKE",
        pra / "Semana07_PRA_Guia_TP.pdf",
        "Semana 7 PRA – Guía TP"
    )
    download_doc_pdf(
        "1ibPEi3Yah88S-7HWopk_0pZ5R140PxBY4idCX5Pm_ts",
        pra / "Semana07_PRA_Referentes_Visuales.pdf",
        "Semana 7 PRA – Referentes Visuales"
    )


# ─── Semana 9 ────────────────────────────────────────────────────────────────
def semana_09():
    print("\n── Semana 09 ──")
    lab = REPO / "009" / "009 - LAB"
    ensure(lab)
    download_drive_zip(
        "1fPpXbpHiLulpPeV3UUwGA84ous-aYCWl",
        lab / "Semana09_LAB_recursos.zip",
        "Semana 9 LAB – ZIP de recursos"
    )


# ─── Semana 11 ───────────────────────────────────────────────────────────────
def semana_11():
    print("\n── Semana 11 ──")
    teo = REPO / "011" / "011 - TEO"
    ensure(teo)
    download_slides_pdf(
        "1TSSzM8mfNYGdLMSFouDfmNkDtC0psr5E-JCMgjf1h38",
        teo / "Semana11_TEO_Presentacion.pdf",
        "Semana 11 TEO – Presentación"
    )


# ─── Semana 12 ───────────────────────────────────────────────────────────────
def semana_12():
    print("\n── Semana 12 ──")
    teo = REPO / "012" / "012 - TEO"
    ensure(teo)
    download_slides_pdf(
        "1W62u7Vdtv56NQsiY1L7ZAZoWdTLa-IDdevFU-EUyoUg",
        teo / "Semana12_TEO_Presentacion.pdf",
        "Semana 12 TEO – Presentación"
    )


# ─── Clonar repo del profesor y copiar LABs ──────────────────────────────────
PROF_REPO_URL = "https://github.com/mattbarreto/ifts24-lab-pdi-2026.git"

# Mapeo: carpeta en el repo del profesor → carpeta LAB del usuario
PROF_LAB_MAP = {
    "001 - py5":                     REPO / "001" / "001 - LAB",
    "002 - py5":                     REPO / "002" / "002 - LAB",
    "003 - librerias_fundamentos_pdi": REPO / "003" / "003 - LAB",
    "004 - computer_vision_parte_1": REPO / "004" / "004 - LAB",
    "005 - TFI_1":                   REPO / "005" / "TFI",
    "006 - redes_neuronales_parte_1": REPO / "006_fotografia_digital" / "006 - LAB",
    "007 - redes_neuronales_parte_2": REPO / "007" / "007 - LAB",
    "008 - vision_artificial_aplicada": REPO / "008" / "008 - LAB",
    "009 - modelos_difusion":        REPO / "009" / "009 - LAB",
}


def copiar_labs_del_profesor():
    print("\n── Notebooks del profesor ──")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        print("  Clonando repo del profesor (shallow clone)…")
        result = subprocess.run(
            ["git", "clone", "--depth=1", PROF_REPO_URL, str(tmp_path / "prof")],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  [ERROR] No se pudo clonar el repo del profesor:\n{result.stderr}")
            print("  Podés clonarlo manualmente con:")
            print(f"    git clone --depth=1 {PROF_REPO_URL}")
            return

        prof_root = tmp_path / "prof"
        for carpeta_prof, destino_lab in PROF_LAB_MAP.items():
            src = prof_root / carpeta_prof
            if not src.exists():
                print(f"  [SKIP] {carpeta_prof} no encontrado en el repo del profesor")
                continue
            ensure(destino_lab)
            # Copiar archivos (no sobreescribir los que ya existen)
            copiados = 0
            for item in src.rglob("*"):
                if item.is_file() and not item.name.startswith("."):
                    rel = item.relative_to(src)
                    target = destino_lab / rel
                    if not target.exists():
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, target)
                        copiados += 1
            print(f"  [OK] {carpeta_prof} → {destino_lab.relative_to(REPO)} ({copiados} archivos)")


# ─── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Repo: {REPO}")
    print("=" * 60)

    semana_01()
    semana_02()
    semana_04()
    semana_06()
    semana_07()
    semana_09()
    semana_11()
    semana_12()
    copiar_labs_del_profesor()

    print("\n" + "=" * 60)
    print("¡Listo! Ahora podés hacer git add . && git commit.")
