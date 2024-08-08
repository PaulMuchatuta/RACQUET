import logging
import openai
import csv

logging.basicConfig(
   filename="RACQUET Run Log.txt",  # define filename and type
   level=logging.INFO,  # set logging level to info so all info and higher messages will be logged
   format="%(asctime)s\n%(message)s\n\n",  # define that the log will include the time and date of log, prompt sent, and then 2 new lines
   datefmt="%Y-%m-%d %H:%M:%S"  # define date format as YYMMDD and time as HHMMSS
)

openai.api_key = "sk-proj-S5thhOfoSd0QpViNDaBKT3BlbkFJG8UElZn009nyvW7OKcLm"  # replace with your actual API key

def ask_question(prompt):
    # Query OpenAI for an answer to the question
    try:
        logging.info(f"Prompt: {prompt}")  # log prompt for review
        completion = openai.ChatCompletion.create(
            model="gpt-4",  # updated to use GPT-4
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Rewrite this requirement in a concise manner focusing strictly on how the system is required to behave, without losing context. The determinant “shall” shall be used whenever a provision is a requirement, The determinant “should” shall be used whenever a provision is a recommendation, the determinant “may” shall be used whenever a provision is a permission, and The determinant “can” shall be used to indicate possibility or capability. Anything that is not deemed a requirement should not be converted. State which type of BNF EARS template requirement is being produced in the format of <requirement type> and then the requirement. Note that anything that isn't a requirement should be treated as a non-requirement. Use the example of good and bad requirements as a guideline when generating the new requirement."}
            ]
        )
        response = completion.choices[0].message["content"]
        logging.info(f"Response: {response}")  # log response for review
        return response
    except Exception as e:
        logging.error(f"Error: {e}")  # log the error for review
        return None

def classify_input(text):  # Count input text and assign to excessive and insufficient
    word_count = len(text.split())
    
    if word_count < 4:
        return "<Insufficient Text>"
    elif word_count > 20:
        return "<Excessive Text>"
    else:
        return None

def main():
    csv_file = "C:/Users/Paulm/OneDrive/Documents/University/Surrey/Y4/output file.csv"  # Update with your known file location

    # Read and process each row in the CSV file
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)  # Read all rows into a list

        # Iterate over each row, process the content, and update the row
        for i, row in enumerate(rows):
            if not row:
                continue
            
            question = row[0]
            
            # Check for excessive or insufficient text
            classification = classify_input(question)
            if classification:
                print(f"{classification}: {question}")
                rows[i][0] = classification  # Update the CSV row with the classification
                continue

            # Feedback loop - Read feedback files
            try:
                with open("Bad Requirement Feedback.txt", "r") as file:
                    bad_feedback = file.read().strip()
            except FileNotFoundError:
                bad_feedback = "No bad feedback available."
            
            try:
                with open("Good Requirement Feedback.txt", "r") as file:
                    good_feedback = file.read().strip()
            except FileNotFoundError:
                good_feedback = "No good feedback available."

            prompt = (
                f'Using the EARS template defined by the BNF grammar below, '
                f'generate the <requirement> from the unformatted requirement: "{question}". Note that anything that is not an immediately obvious requirement should be treated according to the <non-requirement> rules and use the example of good and bad requirements as a guideline when generating the new requirement. \n'
                f'<requirement> ::= <ubiquitous> | <event-driven> | <state-driven> | <optional> | <unwanted>, \n'
                f'<ubiquitous> ::= “The system shall <action>.”, \n'
                f'<event-driven> ::= “When <event>, the system shall <action>.”, \n'
                f'<state-driven> ::= “While <state>, the system shall <action>.”, \n'
                f'<optional> ::= “The system shall <action>.”, \n'
                f'<unwanted>::= “The system shall <preventive-action> to <unwanted-outcome>.”, \n'
                f'<action> ::= <verb-phrase>, \n'
                f'<event> ::= <noun-phrase>, \n'
                f'<state> ::= <noun-phrase>, \n'
                f'<preventive-action> ::= <verb-phrase>, \n'
                f'<unwanted-outcome> ::= <noun-phrase>, \n'
                f'<verb-phrase> ::= “a verb phrase”, \n'
                f'<noun-phrase> ::= “a noun phrase”, \n'
                f'<non-requirement> ::= “This is not a suitable requirement and a failed notice should be given, with no attempt to convert to a requirement”\n\n'
                f'Here are examples of Bad Requirements that should absolutely be avoided and never repeated:\n{bad_feedback}\n'
                f'Here are examples of Good Requirements that should be emulated:\n{good_feedback}\n'
                f'Please consider the above examples of bad requirements while generating the new requirement. The new requirement should follow the patterns of the good examples and avoid the pitfalls and errors seen in these examples.'
            )

            # Get the answer from OpenAI
            answer = ask_question(prompt)

            # Update the CSV row with the answer
            if answer:
                rows[i][0] = answer

        # Write the updated rows back to the CSV file
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    except Exception as e:
        logging.error(f"Error processing CSV file: {e}")

if __name__ == "__main__":
    main()
