"Calling all generators"

from tools.llm.cohere_ import CohereGenerator
from tools.llm.gemini_ import GeminiGenerator
from tools.llm.groq_ import GroqGenerator
from tools.llm.sambanova import SambaNovaGenerator
from tools.llm.openai_ import OpenAIGenerator


class GeneratorFactory: 
    "Building a factory of generators"
    @staticmethod
    def build_generator(provider, api_key, model_name):
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