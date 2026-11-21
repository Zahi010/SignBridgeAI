from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.database.database import get_db
from backend.app.models.entities import Subject
from backend.app.schemas.vocabulary import SubjectSchema

router = APIRouter()

@router.get("/subjects", response_model=List[SubjectSchema], summary="List engineering subjects")
def list_subjects(
    branch_id: Optional[int] = Query(None, description="Filter by branch ID"),
    db: Session = Depends(get_db)
):
    query = db.query(Subject)
    if branch_id:
        query = query.filter(Subject.branch_id == branch_id)
    
    subjects = query.all()
    output = []
    for s in subjects:
        output.append(
            SubjectSchema(
                id=s.id,
                branch_id=s.branch_id,
                code=s.code,
                name=s.name,
                description=s.description,
                concept_count=len(s.concepts)
            )
        )
    return output

