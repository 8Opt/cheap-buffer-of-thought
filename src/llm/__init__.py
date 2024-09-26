"Calling all generators"

from src.llm.cohere_ import CohereGenerator
from src.llm.gemini_ import GeminiGenerator
from src.llm.groq_ import GroqGenerator
from src.llm.sambanova import SambaNovaGenerator
from src.llm.openai_ import OpenAIGenerator


class GeneratorFactory: 
    "Building a factory of generators"
    @staticmethod
    def call_generator(provider, api_key, model_name):
        "Calling each generator based on its provider, api_key and model_name"
        try:
            match provider:
                case 'cohere': 
                    return CohereGenerator(api_key, model_name)
                case 'openai':
                    return OpenAIGenerator(api_key, model_name)
                case 'gemini':
                    return GeminiGenerator(api_key, model_name)
                case 'groq': 
                    return GroqGenerator(api_key, model_name)
                case 'sambanova': 
                    return SambaNovaGenerator(api_key, model_name)
        except ValueError as ve: 
            raise ValueError("Your model configuration might not fit our servings!") from ve