"""Define agent using GEMINI's API"""

import os
import requests
from typing import Any, Optional, Dict

try:
    import google.generativeai as genai
except ImportError:
    raise ValueError(
        "Gemini is not installed. Please install it with "
        "`pip install 'google-generativeai>=0.3.0'`."
    )

from google.generativeai.types import HarmCategory, HarmBlockThreshold

SAFETY_SETTINGS = {
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        }

from src.base import Generator

class GeminiGenerator(Generator):

    def __init__(self, 
                api_key: Optional[str]=None,
                model_name: Optional[str]='models/gemini-1.5-flash',
                safety_settings: "genai.types.SafetySettingOptions" = SAFETY_SETTINGS, 
                system_prompt:str=None,
                ):
        super().__init__(api_key, model_name)
        config_params: Dict[str, Any] = {
            "api_key": api_key or os.getenv("GOOGLE_API_KEY"),
        }
    
        self.system_prompt = system_prompt
        
        genai.configure(**config_params)

        self.model = genai.GenerativeModel(
            model_name=model_name,
            safety_settings=safety_settings,
        )

        self._model_meta = genai.get_model(model_name)

        supported_methods = self._model_meta.supported_generation_methods
        
        if "generateContent" not in supported_methods:
            raise ValueError(
                f"Model {model_name} does not support content generation, only "
                f"{supported_methods}."
            )

    @staticmethod
    def parse_response(response: str) -> str:
        return response.text

    def generate(self, query:str, system_prompt=None, text_return:bool=True, **kwargs):
        try:
            messages = [{"role": "user", "parts": query}]
            if system_prompt:
                sys_msg = {
                    "role": "system", 
                    "parts": [system_prompt]
                }
                messages.insert(0, sys_msg)
            response = self.model.generate_content(messages)
            if text_return:
                return response.text
            return response
        except ValueError as ve:
            raise ValueError("Got something wrong with the input") from ve
        except requests.exceptions.HTTPError as httpe:
            raise httpe

    def get_model_catalog(self):
        return [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]