"Define Ollama Generator"
import ollama

from src.base import Generator

class OllamaGenerator(Generator): 
    def __init__(self, api_key, model_name): 
        super().__init__(api_key, model_name)

        self.model_name = model_name

    @staticmethod
    def parse_response(response: str) -> str:
        return response['message']['content']

    def generate(self, query: str, system_prompt=None, text_return: bool = True, **kwargs):
        if system_prompt: 
            messages = [
                {'role': 'system', 'content': system_prompt}, 
                {'role': 'user', 'content': query}
            ]
        else: 
            messages = [{'role': 'user', 'content': query}]

        response = ollama.chat(model=self.model_name, 
                               messages=messages)
        
        if text_return: 
            response = self.parse_response(response)

        return response
    
