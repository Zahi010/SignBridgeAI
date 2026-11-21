from fastapi import APIRouter
from backend.app.api.endpoints import (
    health, translation, vocabulary, branches, subjects, history, documents, signs, validation, videos, avatar, ingestion, speech, validation_v2, community
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(translation.router, tags=["Translation"])
api_router.include_router(vocabulary.router, tags=["Vocabulary"])
api_router.include_router(branches.router, tags=["Branches"])
api_router.include_router(subjects.router, tags=["Subjects"])
api_router.include_router(history.router, tags=["History"])
api_router.include_router(documents.router, tags=["Documents"])
api_router.include_router(signs.router, tags=["Signs"])
api_router.include_router(validation.router, prefix="/validation", tags=["Validation"])
api_router.include_router(validation_v2.router, prefix="/validation", tags=["Validation V2"])
api_router.include_router(community.router, prefix="/community", tags=["Community Research"])
api_router.include_router(videos.router, prefix="/videos", tags=["Videos"])
api_router.include_router(avatar.router, prefix="/avatar", tags=["Avatar"])
api_router.include_router(ingestion.router, prefix="/ingestion", tags=["Dataset Ingestion"])
api_router.include_router(speech.router, prefix="/speech", tags=["Speech-to-ISL"])
