"""Define abstract class for tools"""

from abc import ABC, abstractmethod

class Generator(ABC):
    "Abstract class for LLMs' Generator"
    def __init__(self, api_key, model_name):
        self.api_key = api_key
        self.model_name = model_name
    
    @abstractmethod
    def generate(self, query:str, system_prompt=None, text_return:bool=True, **kwargs):
        "Generate response based on user's query"
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def parse_response(response:str) -> str:
        "Using to parse response to text-only"
        raise NotImplementedError