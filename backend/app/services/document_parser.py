"""
SignBridge AI - Document Parsing Service
Extracts text from PDF, DOCX, and PPTX documents for engineering translation.
"""

from pathlib import Path
from typing import Tuple, Dict, Any, List
import re
import pymupdf as fitz
from docx import Document
from pptx import Presentation
from fastapi import UploadFile, HTTPException

from backend.app.core.config import settings

class DocumentParserService:

    @staticmethod
    def validate_file(file: UploadFile) -> Tuple[str, Path]:
        # Sanitize filename to prevent directory traversal
        raw_filename = file.filename or "unknown_file"
        safe_filename = Path(raw_filename).name
        ext = Path(safe_filename).suffix.lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{ext}'. Supported formats: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        target_path = settings.UPLOADS_DIR / safe_filename
        return ext, target_path

    @classmethod
    def extract_from_pdf(cls, file_path: Path) -> Tuple[str, int]:
        """Extracts text and page count from PDF using PyMuPDF."""
        doc = fitz.open(file_path)
        page_count = len(doc)
        text_parts = []
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text_parts.append(page_text.strip())
        doc.close()
        full_text = "\n\n".join(text_parts)
        return full_text, page_count

    @classmethod
    def extract_from_docx(cls, file_path: Path) -> Tuple[str, int]:
        """Extracts text from DOCX."""
        doc = Document(file_path)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        full_text = "\n".join(paragraphs)
        # Approximate page count based on word count
        words = len(full_text.split())
        approx_pages = max(1, words // 350)
        return full_text, approx_pages

    @classmethod
    def extract_from_pptx(cls, file_path: Path) -> Tuple[str, int]:
        """Extracts text and slide count from PPTX."""
        prs = Presentation(file_path)
        slide_count = len(prs.slides)
        slide_texts = []
        for i, slide in enumerate(prs.slides):
            slide_content = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        text = paragraph.text.strip()
                        if text:
                            slide_content.append(text)
            if slide_content:
                slide_texts.append(f"[Slide {i+1}]: " + " | ".join(slide_content))
        full_text = "\n".join(slide_texts)
        return full_text, slide_count

    @classmethod
    def extract_sections(cls, raw_text: str, ext: str) -> List[Dict[str, Any]]:
        """
        Splits document text into logical sections (headings, slides, or thematic paragraphs).
        """
        sections: List[Dict[str, Any]] = []
        clean = raw_text.strip()
        if not clean:
            return [{
                "section_index": 1,
                "heading": "Section 1",
                "text": "No content",
                "sentence_count": 0
            }]

        if ext == ".pptx" or "[Slide " in clean:
            # Split by slide tags
            raw_blocks = re.split(r"(\[Slide\s+\d+\]:?)", clean)
            current_slide = "Slide 1"
            idx = 1
            for block in raw_blocks:
                b = block.strip()
                if not b:
                    continue
                if re.match(r"^\[Slide\s+\d+\]:?$", b, re.IGNORECASE):
                    current_slide = b.replace("[", "").replace("]:", "").replace("]", "")
                else:
                    sentences = [s.strip() for s in b.split(".") if s.strip()]
                    sections.append({
                        "section_index": idx,
                        "heading": current_slide,
                        "text": b,
                        "sentence_count": len(sentences)
                    })
                    idx += 1
        else:
            # Split by double newline or numbered sections
            raw_blocks = re.split(r"\n\s*\n+", clean)
            idx = 1
            for block in raw_blocks:
                b = block.strip()
                if not b or len(b) < 15: # Skip negligible snippets
                    continue
                lines = b.split("\n")
                first_line = lines[0].strip()
                heading = f"Section {idx}"
                if len(first_line) < 60 and not first_line.endswith("."):
                    heading = first_line.replace("#", "").strip() or heading

                sentences = [s.strip() for s in b.split(".") if s.strip()]
                sections.append({
                    "section_index": idx,
                    "heading": heading,
                    "text": b,
                    "sentence_count": max(1, len(sentences))
                })
                idx += 1

        if not sections:
            sentences = [s.strip() for s in clean.split(".") if s.strip()]
            sections.append({
                "section_index": 1,
                "heading": "Overview",
                "text": clean[:1000],
                "sentence_count": len(sentences)
            })

        return sections

    @classmethod
    def parse_document(cls, file_path: Path, ext: str) -> Dict[str, Any]:
        """Parses document based on extension."""
        if ext == ".pdf":
            raw_text, count = cls.extract_from_pdf(file_path)
        elif ext == ".docx":
            raw_text, count = cls.extract_from_docx(file_path)
        elif ext == ".pptx":
            raw_text, count = cls.extract_from_pptx(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")

        words = raw_text.split()
        sentences = [s.strip() for s in raw_text.replace("\n", " ").split(".") if s.strip()]

        return {
            "text": raw_text,
            "page_or_slide_count": count,
            "word_count": len(words),
            "sentence_count": len(sentences),
            "preview": raw_text[:500] + ("..." if len(raw_text) > 500 else "")
        }
