from fastapi import APIRouter, Depends

from app.auth.service import JWTBearer
from app.llm_services.schema import LessonPlanEvaluationRequest, LessonPlanEvaluationPDFRequest
from app.llm_services.utils.task_utils import evaluate_images, evaluate_pdf

llm_services_router = APIRouter(
    prefix="/llm",
    tags=["LLM Services"],
    dependencies=[Depends(JWTBearer())],
)

@llm_services_router.post("/evaluate_images")
def evaluate_images_route(request_body: LessonPlanEvaluationRequest):
    return evaluate_images(request_body)

@llm_services_router.post("/evaluate_pdf")
def evaluate_pdf_route(request_body: LessonPlanEvaluationPDFRequest):
    return evaluate_pdf(request_body)
