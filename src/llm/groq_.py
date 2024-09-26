"""Define agent using GROQ's API"""

import os
import requests
from typing import Optional

try:
    from groq import Groq
except ImportError:
    raise ValueError(
        "Groq is not installed. Please install it with "
        "`pip install 'groq'`."
    )

from src.base import Generator

SUPPORTED_MODEL = {
    "llama3-8b": "llama3-8b-8192",
    "llama3-70b": "llama3-70b-8192",
    "mixtral-8x7b": "mixtral-8x7b-32768",
    "gemma-7b": "gemma-7b-it",
    }

class GroqGenerator(Generator):


    def __init__(self,
                api_key: Optional[str] = None,
                model_name: str='llama3-8b',
                max_retries:int=5,
                ):
                
        api_key = api_key or os.getenv("GROQ_API_KEY")
        super().__init__(api_key=api_key, model_name=model_name)
        
        self.model = Groq(api_key=api_key, max_retries=max_retries)

    def get_models(self):
        return ', '.join(SUPPORTED_MODEL)

    @staticmethod
    def parse_response(response:str): 
        return response.choices[0].message.content

    def generate(self, query:str, system_prompt=None, text_return: bool = True,**kwargs):
        try:
            if system_prompt:
                messages = [{"role": "system", "content": system_prompt},
                            {"role": "user", "content": query}]
            else:
                messages = [{"role": "user", "content": query}]

            chat_completion = self.model.chat.completions.create(messages=messages, 
                                                                 model=self.model_name, 
                                                                 **kwargs)
            if text_return:
                return self.parse_response(chat_completion)
            return chat_completion
        except ValueError as ve:
            raise ValueError("Got something wrong with the input") from ve
        except requests.exceptions.HTTPError as httpe:
            raise httpe