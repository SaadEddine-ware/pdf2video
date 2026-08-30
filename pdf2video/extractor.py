"""PDF content extraction with OCR support for scanned documents."""

import os
import re
from dataclasses import dataclass, field

import pdfplumber


@dataclass
class Section:
    title: str
    items: list[str] = field(default_factory=list)


def _extract_text_pdfplumber(pdf_path: str) -> str:
    """Extract text using pdfplumber (works for digital PDFs)."""
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
    return "\n".join(text_parts)


def _extract_text_ocr(pdf_path: str) -> str:
    """Extract text using OCR (works for scanned PDFs)."""
    try:
        import pymupdf
        import pytesseract
        from PIL import Image
        import io

        doc = pymupdf.open(pdf_path)
        text_parts = []
        total = min(len(doc), 6)  # Max 6 pages for speed

        for page_num in range(total):
            page = doc[page_num]
            mat = pymupdf.Matrix(1.5, 1.5)  # 1.5x = ~108 DPI (fast)
            pix = page.get_pixmap(matrix=mat)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(img, lang="fra+eng")
            if text.strip():
                text_parts.append(text)

        doc.close()
        return "\n".join(text_parts)
    except Exception as e:
        print(f"  WARNING: OCR failed: {e}")
        return ""


def extract_pdf(pdf_path: str) -> tuple[str, list[Section]]:
    """Extract title and sections from a PDF.

    Automatically detects if the PDF is scanned (no text) and uses OCR.
    """
    with pdfplumber.open(pdf_path) as pdf:
        meta = pdf.metadata or {}
        title = meta.get("Title", "") or os.path.splitext(os.path.basename(pdf_path))[0]

    # Try pdfplumber first
    text = _extract_text_pdfplumber(pdf_path)

    # If no real text found (only headers/footers), try OCR
    real_text = text.replace("CamScanner", "").replace("Pr: Mustapha Ez-zaiym", "").strip()
    if len(real_text) < 100:
        print("  Scanned PDF detected, using OCR...")
        text = _extract_text_ocr(pdf_path)

    if not text.strip():
        print("  WARNING: No text could be extracted")
        return title, [Section(title=title, items=["(Could not extract text from this PDF)"])]

    # Parse into sections
    sections: list[Section] = []
    current = Section(title=title)

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Skip page headers/footers
        if line in ("CamScanner",) or re.match(r"^Chapitre \d+", line):
            continue

        # Numbered heading: "1.1 Title", "1. Introduction"
        if re.match(r"^\d+[\.\)]\s*.+", line) and len(line) < 120:
            if current.items:
                sections.append(current)
            current = Section(title=line)
        # "Definition", "Theorem", "Proposition", "Exemple" etc.
        elif re.match(r"^(Definition|Theoreme|Theorem|Proposition|Exemple|Remarque|Notation|Propriete)\s+\d", line, re.IGNORECASE):
            if current.items:
                sections.append(current)
            current = Section(title=line)
        # Bullet point
        elif line.startswith(("-", "\u2022", "\u2013", "*")):
            current.items.append(line.lstrip("-\u2022\u2013* "))
        # Short line that looks like a heading
        elif len(line) < 60 and not line.endswith(".") and not line.endswith(","):
            if line[0].isupper():
                if current.items:
                    sections.append(current)
                current = Section(title=line)
            else:
                current.items.append(line)
        # Long paragraph - split into sentences
        else:
            sentences = re.split(r"(?<=[.!?])\s+", line)
            for s in sentences:
                s = s.strip()
                if s and len(s) > 5:
                    current.items.append(s)

    if current.items:
        sections.append(current)

    return title, sections
