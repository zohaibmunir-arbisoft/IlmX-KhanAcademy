import base64
from app.llm_services.utils.model_manager import OpenAIModelManager
import time
import concurrent.futures
from app.llm_services.utils.data import LLMPrompts, tools
from app.llm_services.schema import LessonPlanObservation
import json

model_manager = OpenAIModelManager()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_indicator(score):
    return (
        "0-Poor" if score == 0 else
        "1-Fair" if score == 1 else
        "2-Good" if score == 2 else
        "3-Mastered"
    )

def evaluate_images(request_body):
    image_files, model = request_body.images, request_body.model
    if not image_files:
        return {"Error": "Please upload at least one image."}

    start_time = time.time()

    # Extract text from each image in sorted order
    all_text = []
    input_tokens_total, output_tokens_total = 0, 0

    def process_image(img):
        extracted_text, token_usage = model_manager.extract_text_from_image(img)
        return extracted_text, token_usage

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_image, image_files))

    for i, (extracted_text, token_usage) in enumerate(results):
        input_tokens_total += token_usage.input_tokens
        output_tokens_total += token_usage.output_tokens
        all_text.append(extracted_text)
        print(f"Image {i} transcribed: {extracted_text}")

    combined_text = "\n\n".join(all_text)

    # Call the evaluation model with the combined extracted text
    evaluation, token_usage = model_manager.invoke(
        system_prompt=LLMPrompts.lesson_plan_file_observation_system.format(tools=tools),
        user_prompt= LLMPrompts.lesson_plan_file_observation_user + "\n" + combined_text,
        response_model=LessonPlanObservation,
        model=model
    )
    evaluation = json.loads(evaluation)
    # Calculate scores
    scores = [
        evaluation["objectives_and_lesson_planning"]["five_part_lesson_plan"],
        evaluation["objectives_and_lesson_planning"]["appropriateness_according_to_resources"],
        evaluation["objectives_and_lesson_planning"]["time_allocation"],
        evaluation["appropriateness_of_lesson_objective"]["relevance_of_lesson_objective"],
        evaluation["effectiveness_of_warmup"]["effectiveness_of_warmup_activity"],
        evaluation["main_activity"]["clearance_and_alignment_of_main_activity"],
        evaluation["main_activity"]["use_of_tools_for_relevance_to_context"],
        evaluation["main_activity"]["student_participation_and_encouragement"],
        evaluation["effectiveness_of_wrapup"]["use_of_formative_assessment_and_consolidation_tools"]
    ]
    score_1 = sum(scores[:3]) * 30
    score_2 = sum(scores[3:4]) * 10
    score_3 = sum(scores[4:5]) * 15
    score_4 = sum(scores[5:8]) * 30
    score_5 = sum(scores[8:]) * 15
    obtained_score = sum(scores)
    total_score = 27
    percentage_score = round(((score_1 + score_2 + score_3 + score_4 + score_5) / 660) * 100, 5)

    result_json = {
        "Objectives & Lesson Planning": {
            "5-part Lesson Plan": get_indicator(evaluation["objectives_and_lesson_planning"]["five_part_lesson_plan"]),
            "Appropriateness (Resources)": get_indicator(evaluation["objectives_and_lesson_planning"]["appropriateness_according_to_resources"]),
            "Time Allocation": get_indicator(evaluation["objectives_and_lesson_planning"]["time_allocation"]),
            "Feedback": evaluation["objectives_and_lesson_planning"]["feedback"]
        },
        "Appropriateness of Lesson Objective": {
            "Relevance of Lesson Objective": get_indicator(evaluation["appropriateness_of_lesson_objective"]["relevance_of_lesson_objective"]),
            "Feedback": evaluation["appropriateness_of_lesson_objective"]["feedback"]
        },
        "Effectiveness Of Warm-up Activity": {
            "Effectiveness of Warm-up Activity": get_indicator(evaluation["effectiveness_of_warmup"]["effectiveness_of_warmup_activity"]),
            "Feedback": evaluation["effectiveness_of_warmup"]["feedback"]
        },
        "Main Activity (Direct Instructions & Student Practice)": {
            "Clearance and Alignment of Main Activity": get_indicator(evaluation["main_activity"]["clearance_and_alignment_of_main_activity"]),
            "Use Of Tools For Relevance To Context": get_indicator(evaluation["main_activity"]["use_of_tools_for_relevance_to_context"]),
            "Student Participation and Encouragement": get_indicator(evaluation["main_activity"]["student_participation_and_encouragement"]),
            "Feedback": evaluation["main_activity"]["feedback"]
        },
        "Effectiveness Of Wrap-up Activity": {
            "Effective use of Formative Assessment and Consolidation Tools": get_indicator(evaluation["effectiveness_of_wrapup"]["use_of_formative_assessment_and_consolidation_tools"]),
            "Feedback": evaluation["effectiveness_of_wrapup"]["feedback"]
        },
        "Scores": {
            "Obtained Score": obtained_score,
            "Total Score": total_score,
            "Percentage": percentage_score,
        },
        "Token Usage and Time Taken": {
            "Prompt Tokens": token_usage.prompt_tokens + input_tokens_total,
            "Completion Tokens": token_usage.completion_tokens + output_tokens_total,
            "Total Tokens": token_usage.total_tokens + input_tokens_total + output_tokens_total,
            "Time Taken": time.time() - start_time
        }
    }

    return result_json