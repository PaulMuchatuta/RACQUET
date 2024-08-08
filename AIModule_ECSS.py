import logging
import sys
import openai

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
            model="gpt-4", #gpt-4 just came out in July or gpt-3.5-turbo which was the previous standard. test with 3.5 turbo for cost reasons, use gpt 4 sparingly
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Rewrite this requirement in a concise manner focusing strictly on how the system is required to behave, without losing context. The determinant “shall” shall be used whenever a provision is a requirement, The determinant “should” shall be used whenever a provision is a recommendation, the determinant “may” shall be used whenever a provision is a permission, and The determinant “can” shall be used to indicate possibility or capability. State which type of defined ECSS Technical Specification (TS) requirement type is being produced in the format of <requirement type> and then the requirement. Note that anything that isn't a requirement should be treated as a non-requirement. Use the exmaple of good requirements, bad requirements, and prohibited terms as a guideline when generating the new requirement."}
            ]
        )
        response = completion.choices[0].message["content"]
        logging.info(f"Response: {response}")  # log prompt for review
        return response
    except Exception as e:
        logging.error(f"Error: {e}")  # log the error for review
        return None

def classify_input(text): # Count input text aand assign to excessive and insufficient
    word_count = len(text.split())
    
    if word_count < 4:
        return "<Insufficient Text>"
    elif word_count > 20:
        return "<Excessive Text>"
    else:
        return None

def main():
    if len(sys.argv) < 2:
        print("No input provided")
        return

    # Prompt the user for a question
    question = sys.argv[1]
    
    # Check for excessive or insufficient text
    classification = classify_input(question) #run classification function
    if classification: #single if so that it continues if not called
        print(f"{classification}: {question}") #repeats the text back so it's clear it's a fail
        return

    #FEEDBACK LOOP
    # Read the bad requirements text file
    try:
        with open("Bad Requirement Feedback.txt", "r") as file:
            bad_feedback = file.read().strip()
    except FileNotFoundError:
        bad_feedback = "No bad feedback available." # need to think on how the files can be centrally accessible for everyone.
    # Read the good requirements text file
    try:
        with open("Good Requirement Feedback.txt", "r") as file:
            good_feedback = file.read().strip()
    except FileNotFoundError:
        good_feedback = "No good feedback available."

    prompt = (
        f'Using the ECSS Technical Specification (TS) requirement template defined below, '
        f'generate the british english <requirement> from the unformatted requirement: "{question}" in british english. Note that anything that is not an immediately obvious requirement should be treated according to the <non-requirement> rules and use the example of good and bad requirements as a guideline when generating the new requirement. Do not use any prohibited terms listed in the prompt under any circumstances.  \n\n'
        
        f'Definitions of requirement types:\n'
        f'<requirement> ::= <Functional> | <Mission> | <Interface> | <Environmental> | <Operational> | <Human Factor> | <(Integrated) Logistics Support Requirements> | <Physical> | <Product Assurance (PA) Induced> | <Configuration> | <Design> | <verification>, \n' #
        f'<ubiquitous> ::= A requirement that applies broadly across the system and is not tied to any specific condition or state.\n'
        f'<event-driven> ::= A requirement that specifies system behavior in response to certain events.\n'
        f'<state-driven> ::= A requirement that specifies system behavior while in certain states.\n'
        f'<optional> ::= A requirement that may or may not be implemented depending on certain conditions or choices.\n'
        f'<unwanted> ::= A requirement that specifies actions to prevent certain unwanted outcomes.\n'
        f'<Functional> ::= Requirements that define what activity or action the product shall perform, in order to conform to the needs / mission statement or requirements of the user.\n'
        f'<Mission> ::= Requirements related to a task, a function, a constraint, or an action induced by the mission scenario.\n'
        f'<Interface> ::= Requirements related to the interconnection or relationship characteristics between the product and other items - this includes different types of interfaces (e.g. physical, thermal, electrical, and protocol).\n'
        f'<Environmental> ::= Requirements related to a product or the system environment during its life cycle; this includes the natural environments (e.g. planet interactions, free space and dust) and induced environments (e.g. radiation, electromagnetic, heat, vibration and contamination).\n'
        f'<Operational> ::= Requirements related to the system operability - this includes operational profiles and the utilization environment and events to which the product shall respond (e.g. autonomy, control and contingency) for each operational profile.\n'
        f'<Human Factor> ::= Requirements related to a product or a process adapted to human capabilities considering basic human characteristics - this includes basic human capability characteristics such as 1. Decision making; 2. Muscular Strength, coordination and craftsmanship; 3. body dimensions; 4. perception and judgement; 5. workload; and 6. comfort and freedom from environmental stress.\n'
        f'<(Integrated) Logistics Support Requirements> ::= Requirements related to the (integrated) logistics support considerations to ensure the effective and economical support of a system for its life cycle - such as 1. the constraints concerning the maintenance (e.g. minimum periodicity, intervention duration, infrastructure, tooling, intervention modes); 2. packaging, transportation, handling and storage; 3. training of product users; 4. user documentation; 5. implementation of the product at the user site; and 6. reuse of the product or its elements.\n'
        f'<Physical> ::= Requirements that establish the boundary conditions to ensure physical compatibility and that are not defined by the interface requirements, design and construction requirements, or referenced drawings - This includes requirements related to mechanical characteristics, electrical isolation and chemical composition (e.g. weight and dimensional limits).\n'
        f'<Product Assurance (PA) Induced> ::= Requirements related to the relevant activities covered by the product assurance - This can include subjects such as 1. Reliability, availability, maintainability; 2. Safety; and 3. Quality assurance.\n'
        f'<Configuration> ::= Requirements related to the composition of the product or its organization.\n'
        f'<Design> ::= Requirements related to the imposed design and construction standards such as design standards, selection list of components or materials, interchangeability, safety or margins.\n'
        f'<verification> ::= Requirements related to the imposed verification methods, such as compliance to verification standards, usage of test methods or facilities.\n\n'
        f'<action> ::= <verb-phrase>, \n'
        f'<event> ::= <noun-phrase>, \n'
        f'<state> ::= <noun-phrase>, \n'
        f'<preventive-action> ::= <verb-phrase>, \n'
        f'<unwanted-outcome> ::= <noun-phrase>, \n'
        f'<verb-phrase> ::= “a verb phrase”, \n'
        f'<noun-phrase> ::= “a noun phrase”, \n'
        f'<Excessive Text> ::= Any input greater than 20 words, \n'
        f'<Insufficient Text> ::= Any input less than 4 words, \n'
        f'<non-requirement> ::= <action> | <event> | <state> | <preventive-action> | <unwanted-outcome> | <verb-phrase> | <noun-phrase> | <Excessive Text> | <Insufficient Text> Example: “This is not a suitable requirement and a failed notice should be given, with no attempt to convert to a requirement”\n\n'        

        f'Examples of how each rerquirement type might look. These requirements are examples only and should not be used except for when the user input is extremely similar:\n'
        f'<Functional> Example: “The product shall analyze the surface of Mars and transmit the data so that it is at the disposal of the scientific community.”\n'
        f'<Mission> Example: “The product shall be designed to be put in its final position after a transfer duration shorter than 90 days.”\n'
        f'<Interface> Example: “The product shall dialogue with the ground segment using telemetry.”\n'
        f'<Environmental> Example: “The product shall operate within the temperature range from 30 ºC to 50 ºC.”\n'
        f'<Operational> Example: “The product shall be designed to accept control of the viewing function from the ground segment.”\n'
        f'<Human Factor> Example: “The product shall display the information with no more than two windows on the screen at the same time.”\n'
        f'<(Integrated) Logistics Support Requirements> Example: “The product shall be designed to be installed at the customer site within two days.”\n'
        f'<Physical> Example: “The product shall have a mass of (30 +/- 0.1) kg.”\n'
        f'<Product Assurance (PA) Induced> Example: “While testing, the system shall record all anomalies.”\n'
        f'<Configuration> Example: “The product shall have 7 power modules with 2 power outlets per engine.”\n'
        f'<Design> Example: “The receiver shall use a phase-lock loop (PLL).”\n'
        f'<verification> Example: “The thermal balance test shall be performed using solar illumination.”\n'
        f'<non-requirement> Example: “This is not a suitable requirement and a failed notice should be given, with no attempt to convert to a requirement.”\n\n'

        f'Here are examples of Bad Requirements that should absolutely be avoided and never repeated:\n{bad_feedback}\n'
        f'Here are examples of Good Requirements that should be emulated:\n{good_feedback}\n'
        f'Crucially, do not use any of the following prohibited terms in your response under any circumstances: 1. “and/or”, 2. “etc.”, 3. “goal”, 4. “shall be included but not limited to”, 5. “relevant”, 6. “necessary”, 7. “appropriate”, 8. “as far as possible”, 9. “optimize”, 10. “minimize”, 11. “maximize”, 12. “typical”, 13. “rapid”, 14. “user-friendly”, 15. “easy”, 16. “sufficient”, 17. “enough”, 18. “suitable”, 19. “satisfactory”, 20. “adequate”, 21. “quick”, 22. “first rate”, 23. “best possible”, 24. “great”, 25. “small”, 26. “large”, 27. “state of the art”, and 28. “state-of-the-art” - if . Ensure that your response does not include any of these terms. Explicitly state if the requirement does not fit into any of the provided categories.' #explicitly state if the requirement does not fit any provided category.
    )

    # Get the answer from OpenAI
    answer = ask_question(prompt)

    # Print the answer
    if answer:
        print(answer)
    # logging.info(f"Response: {answer}")

if __name__ == "__main__":
    main()
