"Helper functions for the meta-distiller"

import re
import io
import sys


def extract_and_execute_code(text):
    # Possible start and end markers
    code_start_markers = ["```python", "```Python", "```"]
    code_end_marker = "```"

    # Find python part
    code_start_index = -1
    code_start_marker_used = None
    for marker in code_start_markers:
        code_start_index = text.lower().find(marker.lower())
        if code_start_index != -1:
            code_start_marker_used = marker
            break

    # If find code
    if code_start_index != -1:
        # Try to find the end point
        code_end_index = text.find(code_end_marker, code_start_index + len(code_start_marker_used))
        
        # If not, we assume the code is appended to the end of the text
        if code_end_index == -1:
            code_end_index = len(text)
        
        # Extract the code
        code_str = text[code_start_index + len(code_start_marker_used):code_end_index].strip()
        
        # Clean up the code string
        for marker in code_start_markers:
            code_str = code_str.replace(marker, "")
        code_str = code_str.replace(code_end_marker, "").strip()
        
        # Create a stream
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        # Execute the code
        try:
            # pylint: disable-next=exec-used
            exec(code_str, globals())
        except Exception as e:
            # Primary output
            sys.stdout = old_stdout
            return f"An error occurred: {e}", code_str
        
        # Extract the output
        sys.stdout = old_stdout
        return new_stdout.getvalue(), code_str
    else:
        return "No Python code found in the provided string.", None


def extract_answer(text):
    # Define a regular expression pattern to match the answer format
    # The pattern accounts for variations in spacing and line breaks
    pattern = re.compile(r"Answer:\s*(.*?)\s*$", re.DOTALL)

    # Search the text for the pattern
    match = pattern.search(text)

    # If a match is found, return the content; otherwise, return None
    return match.group(1).strip() if match else None