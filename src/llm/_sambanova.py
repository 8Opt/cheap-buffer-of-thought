"""Define agent using SAMBANOVA's API"""

try:
    import openai

except ImportError as ie:
    raise ImportError("`openai` is not installed. Please try `pip install openai`!") from ie

from src.base import Generator

SUPPORTED_MODEL = [
                "Meta-Llama-3.1-8B-Instruct",          # CL-OL: 8192-1000
                "Meta-Llama-3.1-70B-Instruct",         # CL-OL: 8192-1000
                "Meta-Llama-3.1-405B-Instruct"         # CL-OL: 8192-1000
                    ]

class SambaNovaGenerator(Generator):
    SAMBANOVA_API_URL = "https://fast-api.snova.ai/v1"

    def __init__(self, api_key, model_name=SUPPORTED_MODEL[0]):
        super().__init__(api_key, model_name)
        self.client = openai.OpenAI(base_url=self.SAMBANOVA_API_URL,
                                    api_key=api_key,
                                    )
        self.model_name = model_name

    @staticmethod
    def parse_response(response:str):
        response = ""
        for chunk in response:
            response += chunk.choices[0].delta.content or ""
        return response
  
    def generate(self, query, system_prompt=None, text_return=True, **kwargs):
        """
        Run the model with the given prompt and system prompt.

        Args:
        - prompt (str): The user's input.
        - system_prompt (str, optional): The system prompt. Defaults to None.
        - **kwargs: Additional keyword arguments to pass to the OpenAI client.

        Returns:
        - str: The model's response.
        """
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt},
                        {"role": "user", "content": query}]
        else:
            messages = [{"role": "user", "content": query}]

        response = self.client.chat.completions.create(
        model=self.model_name,
        messages=messages,
        stream=True,
        **kwargs,
        )
        if text_return:
            response = self.parse_response(response)
        return response