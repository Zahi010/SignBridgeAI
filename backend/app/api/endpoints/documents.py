import os
import shutil
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.database.database import get_db
from backend.app.core.config import settings
from backend.app.services.document_parser import DocumentParserService
from backend.app.translation.engine import TranslationEngine
from backend.app.schemas.translation import TranslationRequest
from backend.app.schemas.documents import DocumentUploadResponse

router = APIRouter()

@router.post("/documents/upload", response_model=DocumentUploadResponse, summary="Upload PDF, DOCX, or PPTX and translate technical content")
async def upload_document(
    file: UploadFile = File(...),
    branch_id: Optional[int] = Form(None),
    subject_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    ext, target_path = DocumentParserService.validate_file(file)

    # Read and validate size
    contents = await file.read()
    file_size = len(contents)
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    if file_size > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB (received {file_size / (1024*1024):.2f}MB)"
        )
    
    if file_size == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Save to disk
    with open(target_path, "wb") as f:
        f.write(contents)

    # Parse document
    parsed = DocumentParserService.parse_document(target_path, ext)
    raw_text = parsed["text"].strip()
    if not raw_text:
        raw_text = "No extractable text found in uploaded document."

    # Send through translation engine
    # Truncate text for translation engine if exceptionally large
    text_for_translation = raw_text[:2000]
    engine = TranslationEngine(db)
    translation_res = engine.process_translation(
        TranslationRequest(
            text=text_for_translation,
            branch_id=branch_id,
            subject_id=subject_id
        )
    )

    # Section-by-section breakdown & concept extraction
    raw_sections = DocumentParserService.extract_sections(raw_text, ext)
    from backend.app.schemas.documents import DocumentSectionTranslation, DocumentAnalysisSummary
    from backend.app.models.entities import ValidationStatus

    section_translations = []
    total_found_concepts = set()
    supported_concepts = set()
    explanation_concepts = set()
    unsupported_concepts = set()

    for sec in raw_sections[:10]: # Process up to first 10 sections
        sec_text = sec["text"]
        matched_items, _, _ = engine.extract_and_disambiguate_concepts(
            sec_text[:800], branch_id, subject_id
        )

        sec_concept_names = [c.term for c, _, _, _ in matched_items]
        sec_sup = 0
        sec_exp = 0
        sec_unsup = 0

        for c, sign, _, _ in matched_items:
            term = c.term
            total_found_concepts.add(term)
            if sign.validation_status in (ValidationStatus.VERIFIED, ValidationStatus.PARTIAL):
                sec_sup += 1
                supported_concepts.add(term)
            elif sign.validation_status in (ValidationStatus.EXPLANATION_REQUIRED, ValidationStatus.EXPLANATION_NEEDED):
                sec_exp += 1
                explanation_concepts.add(term)
            else:
                sec_unsup += 1
                unsupported_concepts.add(term)

        if sec_unsup > 0:
            sec_status = "unsupported"
        elif sec_exp > 0:
            sec_status = "explanation_required"
        elif sec_sup > 0:
            sec_status = "supported"
        else:
            sec_status = "neutral"

        gloss_summary = " + ".join([c.upper() for c in sec_concept_names[:4]]) or "NO-CONCEPTS-IN-SECTION"

        section_translations.append(
            DocumentSectionTranslation(
                section_index=sec["section_index"],
                heading=sec["heading"],
                text_preview=sec_text[:180] + ("..." if len(sec_text) > 180 else ""),
                sentence_count=sec["sentence_count"],
                detected_concepts=sec_concept_names,
                supported_count=sec_sup,
                explanation_count=sec_exp,
                unsupported_count=sec_unsup,
                status=sec_status,
                isl_gloss_summary=gloss_summary
            )
        )

    # Compute overall document metrics
    total_unique = len(total_found_concepts)
    cov_pct = 100.0
    if total_unique > 0:
        cov_pct = round(((len(supported_concepts) + len(explanation_concepts)) / float(total_unique)) * 100.0, 1)

    doc_analysis = DocumentAnalysisSummary(
        total_sections=len(section_translations),
        total_concepts_found=total_unique,
        supported_concepts_count=len(supported_concepts),
        explanation_required_count=len(explanation_concepts),
        unsupported_concepts_count=len(unsupported_concepts),
        overall_status=translation_res.status.value,
        coverage_percentage=cov_pct
    )

    return DocumentUploadResponse(
        filename=file.filename,
        file_type=ext.replace(".", "").upper(),
        file_size_bytes=file_size,
        page_or_slide_count=parsed["page_or_slide_count"],
        extracted_text_preview=parsed["preview"],
        total_words=parsed["word_count"],
        total_sentences=parsed["sentence_count"],
        detected_concepts_count=len(translation_res.extracted_concepts),
        translation_summary=translation_res,
        sections=section_translations,
        document_analysis=doc_analysis,
        uploaded_at=datetime.now(timezone.utc)
    )

