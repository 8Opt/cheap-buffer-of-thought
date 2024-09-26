"""Define agent using COHERE's API"""

import time
try:
    import cohere

except ImportError as ie:
    raise ImportError("`cohere` is not installed. Please try `pip install cohere`!") from ie

from src.base import Generator


class CohereGenerator(Generator):
    def __init__(self, model_name:str, api_key:str, n=8, max_tokens=512, temperature=0.7, p=1, frequency_penalty=0.0, presence_penalty=0.0, stop=['\n\n\n'], wait_till_success=False):
        super().__init__(api_key, model_name)
        self.cohere = cohere.Client(self.api_key)
        self.n = n
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.p = p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop
        self.wait_till_success = wait_till_success

    
    @staticmethod
    def parse_response(response):
        text = response.generations[0].text
        return text
    
    def generate(self, query:str, system_prompt=None, text_return:bool=True, **kwargs):
        texts = []
        for _ in range(self.n):
            get_result = False
            while not get_result:
                try:
                    result = self.cohere.chat(
                        prompt=query,
                        model=self.model_name,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        frequency_penalty=self.frequency_penalty,
                        presence_penalty=self.presence_penalty,
                        p=self.p,
                        k=0,
                        stop=self.stop,
                    )
                    get_result = True
                except Exception as e:
                    if self.wait_till_success:
                        time.sleep(1)
                    else:
                        raise e
            if text_return: 
                text = self.parse_response(result)
            texts.append(text)
        return texts