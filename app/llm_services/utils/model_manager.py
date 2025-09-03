import os
import base64

import instructor
from loguru import logger
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_KEY")


class OpenAIModelManager:
    def __init__(self):
        self.model = self.create_model_instance(OPENAI_API_KEY)
        self.openai_model = OpenAI(api_key=OPENAI_API_KEY)

    def create_model_instance(
        self,
        openai_api_key: str,
    ):
        return instructor.from_openai(OpenAI(api_key=openai_api_key))

    def invoke(self, system_prompt, user_prompt, response_model, model):
        return self.invoke_chat_model(system_prompt=system_prompt, user_prompt=user_prompt, response_model=response_model, model=model)

    def invoke_chat_model(self, system_prompt, user_prompt, response_model, model="gpt-5"):
        response, metadata = self.model.chat.completions.create_with_completion(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_model=response_model,
        )
        return response.model_dump_json(), metadata.usage

    def extract_text_from_image(self, base64_image, model="gpt-4o-mini"):
        """Uses gpt-4o-mini to extract text from a single image."""
        response = self.model.responses.create(
            model=model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Extract the text in this image. The text is both in english and urdu so be careful."},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ],
        )
        return response.output_text.strip(), response.usage

    def extract_text_from_pdf(self, base64_pdf, response_model, system_prompt, user_prompt, model="gpt-4o-mini"):
        """Uses gpt-4o-mini to extract text from a single PDF."""
        response = self.openai_model.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "file",
                            "file": {
                                "filename": "temp.pdf",
                                "file_data": f"data:application/pdf;base64,{base64_pdf}",
                            }
                        },
                        {
                            "type": "text",
                            "text": user_prompt,
                        }
                    ],
                },
            ],
        response_format=response_model,
        )
        return response.choices[0].message.parsed, response.usage

    def invoke_chat_model_with_file(self, system_prompt, user_prompt, response_model, model="gpt-5"):
        response, metadata = self.model.chat.completions.create_with_completion(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [{
                    "type": "input_file",
                    "file_id": 'file-Qmp3Vx5dDViRXzdHWjFt7S',
                },
                {
                    "type": "input_text",
                    "text": user_prompt,
                }],}
            ],
            response_model=response_model,
            temperature=0.1,
            top_p=0.3
        )
        return response.model_dump_json(), metadata.usage
