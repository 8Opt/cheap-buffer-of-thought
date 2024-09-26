"""Define agent using OPENAI's API"""

import time

try:
    import openai

except ImportError as ie:
    raise ImportError("`openai` is not installed. Please try `pip install openai`!") from ie

from tools.base import Generator

class OpenAIGenerator(Generator):
    def __init__(self, model_name, api_key, n=8, max_tokens=512, temperature=0.7, top_p=1, frequency_penalty=0.0, presence_penalty=0.0, stop=['\n\n\n'], wait_till_success=False):
        super().__init__(model_name, api_key)
        self.n = n
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop
        self.wait_till_success = wait_till_success
    
    @staticmethod
    def parse_response(response):
        to_return = []
        for _, g in enumerate(response['choices']):
            text = g['text']
            logprob = sum(g['logprobs']['token_logprobs'])
            to_return.append((text, logprob))
        texts = [r[0] for r in sorted(to_return, key=lambda tup: tup[1], reverse=True)]
        return texts

    def generate(self, query:str, system_prompt=None, text_return:bool=True, **kwargs):
        get_results = False
        while not get_results:
            try:
                result = openai.Completion.create(
                    engine=self.model_name,
                    prompt=query,
                    api_key=self.api_key,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    frequency_penalty=self.frequency_penalty,
                    presence_penalty=self.presence_penalty,
                    top_p=self.top_p,
                    n=self.n,
                    stop=self.stop,
                    logprobs=1
                )
                get_results = True
            except Exception as e:
                if self.wait_till_success:
                    time.sleep(1)
                else:
                    raise e
                    
        if text_return: 
            return self.parse_response(result)
        return result
