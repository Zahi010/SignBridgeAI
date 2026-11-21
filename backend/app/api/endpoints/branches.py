from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.app.database.database import get_db
from backend.app.models.entities import EngineeringBranch
from backend.app.schemas.vocabulary import BranchSchema

router = APIRouter()

@router.get("/branches", response_model=List[BranchSchema], summary="List all engineering branches")
def list_branches(db: Session = Depends(get_db)):
    branches = db.query(EngineeringBranch).all()
    output = []
    for b in branches:
        output.append(
            BranchSchema(
                id=b.id,
                code=b.code,
                name=b.name,
                description=b.description,
                subject_count=len(b.subjects),
                concept_count=len(b.concepts)
            )
        )
    return output

