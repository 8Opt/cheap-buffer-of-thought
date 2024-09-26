TEXT_COMPREHENSION = """
Task Description:
The task involves analyzing a table with various attributes of penguins, such as name, age,
height, and weight, and answering questions about these attributes. The table may be updated
with new entries, and additional context or comparisons may be provided in natural language.

Solution Description:
To accurately answer questions about the penguins’ attributes, one must be able to interpret
the data presented in tabular form, understand any additional information provided in natural
language, and apply logical reasoning to identify the correct attribute based on the question
asked.

Thought Template:
Step 1: Parse the initial table, extracting the header information and each penguin’s attributes
into a structured format (e.g., a list of dictionaries).
Step 2: Read and integrate any additional natural language information that updates or adds
to the table, ensuring the data remains consistent.
Step 3: Identify the attribute in question (e.g., oldest penguin, heaviest penguin) and the
corresponding column in the table.
Step 4: Apply logical reasoning to compare the relevant attribute across all entries to find the
correct answer (e.g., the highest age for the oldest penguin).
Step 5: Select the answer from the provided options that matches the result of the logical
comparison.
"""

CREATIVE_LANG_GENERATION = """
Task Description:
The task is to generate a sonnet that adheres to the traditional English sonnet rhyme scheme
of "ABAB CDCD EFEF GG" and includes three specific words verbatim in the text.

Solution Description:
Writing a sonnet involves crafting 14 lines of poetry that follow a specific rhyme pattern.
The lines are typically in iambic pentameter, though flexibility in rhythm can be allowed for
creative reasons. The given rhyme scheme dictates the end sounds of each line, ensuring a
structured poetic form. Incorporating the three provided words verbatim requires strategic
placement within the lines to maintain the poem’s coherence and thematic unity.

Thought Template:
Step 1: Identify the three words that must be included in the sonnet.
Step 2: Understand the rhyme scheme "ABAB CDCD EFEF GG" and prepare a list of
rhyming words that could be used.
Step 3: Develop a theme or story for the sonnet that can naturally incorporate the three
provided words.
Step 4: Begin drafting the sonnet by writing the first quatrain (four lines) following the
"ABAB" rhyme scheme, ensuring one or more of the provided words are included.
Step 5: Continue with the second quatrain "CDCD," the third quatrain "EFEF," and finally
the closing couplet "GG," each time incorporating the provided words as needed.
Step 6: Review the sonnet for coherence, flow, and adherence to the rhyme scheme, making
adjustments as necessary
"""

COMMON_SENSE_REASONING = """
Task Description:
Given a specific date and an event, such as a holiday or historical event, determine the
following date.

Solution Description:
To determine the next date, we need to consider the structure of the calendar, the number of
days in each month, and whether it’s a leap year. Typically, the number of days in a month
is fixed, except February may vary due to leap years. The next day in a year is usually the
date increased by one day unless it’s the end of the month, then the next day will be the first
day of the following month. For the end of the year, the next day will be January 1st of the
following year.

Thought Template:
Step 1: Identify the given date’s month and day number.
Step 2: Check if it’s the end of the month; if so, confirm the start date of the next month.
Step 3: If it’s not the end of the month, simply add one to the day number.
Step 4: Pay special attention to the end of the year, ensuring the year increments.
"""

MATHEMATICAL_REASONING = """
Task Description:
Solve an quadratic equation of the form ax2 + bx + c = 0 considering any situations.

Solution Description:
To solve any quadratic equation of the form ax2 + bx + c = 0, we can follow a general
approach based on the method described. Here is the structured template for solving such
equations:

Thought Template:
Step 1: Calculate the Discriminant
- Compute the discriminant D using the formula D = b2 − 4ac.
Step 2: Determine the Nature of the Roots
- If D > 0, the equation has two distinct real roots.
- If D = 0, the equation has exactly one real root (also known as a repeated or double root).
- If D < 0, the equation has two complex roots.
Step 3: Compute the Roots - For D ≥ 0, calculate the roots using the formula x = −b±2a√D .
- For D < 0, calculate the real and imaginary parts of the complex roots using the formula
x = (−b ± √2−aD*i)/2a, where i is the imaginary unit.
"""

CODE_PROGRAMMING = """
Task Description:
When given a list of numbers, try to utilize 4 basic mathematical operations (+-*/) to get a
target number.

Thought Template:

```
from itertools import permutations , product
def perform_operation (a, b, operation ):
# Define the operation logic (e.g., addition , subtraction ,
etc .).
pass
def evaluate_sequence ( sequence , operations ):
# Apply operations to the sequence and check if the result
meets the criteria .
pass
def generate_combinations ( elements , operations ):
# Generate all possible combinations of elements and
operations .
pass
def format_solution ( sequence , operations ):
# Format the sequence and operations into a human - readable
string .
pass
def find_solution ( input_elements , target_result ):
# Data Input Handling
# Validate and preprocess input data if necessary .
# Core Algorithm Logic
for sequence in permutations ( input_elements ):
for operation_combination in generate_combinations (
sequence , operations ):
try :
if evaluate_sequence ( sequence ,
operation_combination ) == target_result :
# Data Output Formatting
return format_solution ( sequence ,
operation_combination )
except Exception as e:
# Error Handling
# Handle specific exceptions that may occur
during evaluation .
continue
# If no solution is found after all iterations , return a
default message .
# return No solution found message
return
# Example usage :
input_elements = [1, 7, 10, 3]
target_result = 24
print ( find_solution ( input_elements , target_result ))
```
"""

APPLICATION_SCHEDULING = """
Task Description:
Given some Chess moves in SAN, update the chess board state.
```
import chess
def find_checkmate_move ( moves_san ):
# Initialize a new chess board
board = chess . Board ()
# Apply the moves to the board
for move_san in moves_san :
# Remove move numbers and periods (e.g., "1." or "2.")
if len( move_san . split (’.␣’)) > 1:
move_san = move_san . split (’.␣’)[1]
# Skip empty strings resulting from the removal
if move_san :
# Apply each move in SAN format to the board
move = board . parse_san ( move_san )
board . push ( move )
# Generate all possible legal moves from the current
position
for move in board . legal_moves :
# Make the move on a copy of the board to test the
result
board_copy = board . copy ()
board_copy . push ( move )
# Check if the move results in a checkmate
if board_copy . is_checkmate ():
# Return the move that results in checkmate in SAN
format
return board .san ( move )
# return No solution found message
return
# Example usage :
input = ’...... ’
# Check input format and transform the input into legal format
# Remove move numbers and periods (e.g., "1." or "2.")
checkmate_move = find_checkmate_move ( moves_san )
print ( checkmate_move )    
```
"""