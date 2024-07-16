from fastapi import APIRouter, FastAPI

from routes.form import form_builder_router
from routes.submission import data_submission_router

router: APIRouter = APIRouter(prefix="/api/formbuilder/v1")


def setup_routes(app: FastAPI):

    router.include_router(form_builder_router)
    router.include_router(data_submission_router)
    
    app.include_router(router)
