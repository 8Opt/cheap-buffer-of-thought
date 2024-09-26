INSTANTIATION_INSTRUCT = """
You are an expert problem solver. Analyze the user's task and generate a specific solution based on the provided thought template. If the solution involves Python code, only provide the code. If not, provide a clear and extractable final answer.
All Python code should be within one code block. The answer should not include more than one code block! Strictly follow the thought template but adjust input parameters as needed.
"""

INSPECTOR_PROMPT = """
You are a skilled Python programmer. Analyze the given Python code and edit it to ensure correctness and problem-solving ability. Provide the edited code in a code block.
"""

def formated_query(distilled_information, query, thought_template): 
    "Reformated query for reasoning initiation"
    FORMATTED_QUERY = f"""
Distilled information:
{distilled_information}
User Input:
{query}
Thought template:
{thought_template}

Instantiated Solution:
Please analyze the above user task description and thought template, and generate a specific, detailed solution. If the solution involves Python code, only provide the code. If not, provide a clear and extractable final answer.
"""
    return FORMATTED_QUERY