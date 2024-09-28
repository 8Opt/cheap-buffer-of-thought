"Pipeline for buffer-of-thought"

from src.llm import GeneratorFactory
from src.helper.meta_distill import extract_and_execute_code
from src.helper.utils import set_logger
from src.prompts.test_templates import GAME24, CHECKMATE, WORD_SORTING
from src.prompts.distiller import META_DISTILLER_PROMPT
from src.prompts.reasoner import INSTANTIATION_INSTRUCT, INSPECTOR_PROMPT, formated_query

class BoT:
    def __init__(self,
                 query,
                 problem_id,
                 provider:str=None,
                 api_key:str=None,
                 model_name:str=None, 
                 need_check:bool=False
                ):
        self.api_key = api_key
        self.model_name = model_name
        self.provider = provider
        self.llm = GeneratorFactory.call_generator(provider, api_key, model_name)
        self.query = query
        self.problem_id = problem_id  # For testing purposes only
        self.need_check = need_check

        self.logger = set_logger(provider=provider, 
                                 model_name=model_name)

    def update_query(self, new_input):
        """Update nput"""
        self.query = new_input

    def problem_distillation(self):
        "Distil problem"
        self.logger.info(f"User prompt: {self.query}")
        self.distilled_information = self.llm.generate(query=self.query, system_prompt=META_DISTILLER_PROMPT)
        self.logger.info(f"Distilled information: {self.distilled_information}")

    def buffer_retrieve(self):
        "Retrieve template from buffer"
        # For initial testing, use a simple mapping. Consider using embedding retrieval later
        self.thought_template = {
            0: GAME24,
            1: CHECKMATE,
            2: WORD_SORTING
        }.get(self.problem_id)

    def reasoner_instantiation(self):
        # Temporary selection method for answer extraction
        problem_id_list = [0, 1, 2]

        self.instantiation_instruct = INSTANTIATION_INSTRUCT

        self.formated_input = formated_query(distilled_information=self.distilled_information, 
                                             query=self.query, 
                                             thought_template=self.thought_template)
        
        self.inspector_prompt = INSPECTOR_PROMPT

        self.result = self.llm.generate(self.instantiation_instruct, self.formated_input)
        self.logger.info(f"Instantiated reasoning result: {self.result}")

        if self.problem_id in problem_id_list:
            self.final_result, code_str = extract_and_execute_code(self.result)

            if self.need_check:
                self.count = 0
                self.inter_input = f"""
                User_input: {self.query}
                {code_str}
                {self.final_result}
                """
                self.inter_result = self.final_result

                while ('An error occurred' in self.inter_result) or (self.inter_result == '') or (self.inter_result == 'None'):
                    self.logger.info('The code cannot be executed correctly. Continuing the edit phase:', self.inter_result)
                    self.logger.info('The problem code is:', code_str)
                    self.inter_input = self.llm.generate(self.inspector_prompt, self.inter_input)
                    self.logger.info(self.inter_input)
                    self.inter_result, inter_code_str = extract_and_execute_code(self.inter_input)
                    self.inter_input = f"""
                    User_input: {self.query}
                    {inter_code_str}
                    The result of code execution: {self.inter_result}
                    """
                    self.count += 1

                    if self.count > 3:
                        break

                self.final_result = self.inter_result

            self.logger.info(f"The result of code execution: {self.final_result}")
        else:
            self.final_result = self.result

    def generate(self):
        self.problem_distillation()
        self.buffer_retrieve()
        self.reasoner_instantiation()
        return self.final_result