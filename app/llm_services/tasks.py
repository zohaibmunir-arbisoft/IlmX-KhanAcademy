import json

from celery_worker import celery
from loguru import logger

from app.llm_services.schema import LessonPlanObservation
from app.llm_services.utils.task_utils import encode_image

def communication_assessment_task(self, data: dict):
    
