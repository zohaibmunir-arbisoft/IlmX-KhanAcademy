from pydantic import BaseModel, field_validator

# ------------------Request Schema------------------------------------

class LessonPlanEvaluationBaseRequest(BaseModel):
    model: str

    @field_validator("model")
    def check_model(cls, value: str):
        if value not in ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-5-mini", "gpt-5"]:
            raise ValueError(f"Model: {value} isn't supported. Kindly choose one of [gpt-5-mini, gpt-5, gpt-4o-mini, gpt-4o, gpt-4.1-mini]")
        return value

class LessonPlanEvaluationRequest(LessonPlanEvaluationBaseRequest):
    images: list[str]

class LessonPlanEvaluationPDFRequest(LessonPlanEvaluationBaseRequest):
    pdf_base64_str: str

# ------------------Response Schema------------------------------------
class ObjectivesAndLessonPlanning(BaseModel):
    five_part_lesson_plan: float
    appropriateness_according_to_resources: float
    time_allocation: float
    feedback: str

class AppropriatenessOfLessonObjective(BaseModel):
    relevance_of_lesson_objective: float
    feedback: str

class EffectivenessOfWarmUpActivity(BaseModel):
    effectiveness_of_warmup_activity: float
    feedback: str

class MainActivity(BaseModel):
    clearance_and_alignment_of_main_activity: float
    use_of_tools_for_relevance_to_context: float
    student_participation_and_encouragement: float
    feedback: str

class EffectivenessOfWrapUpActivity(BaseModel):
    use_of_formative_assessment_and_consolidation_tools: float
    feedback: str

class LessonPlanObservation(BaseModel):
    objectives_and_lesson_planning: ObjectivesAndLessonPlanning
    appropriateness_of_lesson_objective: AppropriatenessOfLessonObjective
    effectiveness_of_warmup: EffectivenessOfWarmUpActivity
    main_activity: MainActivity
    effectiveness_of_wrapup: EffectivenessOfWrapUpActivity
    suggestions_for_improvement: list[str]
    final_remarks: str

class PDFText(BaseModel):
    text: str
