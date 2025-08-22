from fastapi import APIRouter, Depends

from app.auth.service import JWTBearer
from app.llm_services.schema import LessonPlanEvaluationRequest
from app.llm_services.utils.task_utils import evaluate_images

llm_services_router = APIRouter(
    prefix="/llm",
    tags=["LLM Services"],
    dependencies=[Depends(JWTBearer())],
)

@llm_services_router.post("/evaluate_images")
def evaluate_images_route(request_body: LessonPlanEvaluationRequest):
    return evaluate_images(request_body)
