import pandas as pd
import json

instructions = """You are an AI assistant that generates educational materials for an adaptive tutoring software.
You will receive a problem name, topic, and question as input.
Convert each question into a list of JSONs that split the question into problem steps, hints, and scaffolding.
Your role is to generate hints and scaffolding that take the student through the process of solving the question correctly.
Be very careful not to mislead the student or give wrong answers.
You will output ONLY a list of JSONs for each question, with the following keys:

{
    "Problem Name": The provided problem name, 
    "Row Type": Specifies if the current JSON is a "problem", "step", "hint", or "scaffold",
    "Title": A few word summary of the information contained in "Body Text". If "Row Type" is "problem", use the question topic,
    "Body Text":
        - if "Row Type" is "problem": If the question has format "<problem statement>: a)..., b)..., etc", use <problem statement> here. Null otherwise.
        - if "Row Type" is "step": The input question. If a question has multiple parts, there will be multiple steps and each "step" row contains one part
        - if "Row Type" is "hint": A hint to solve the question, as a statement
        - if "Row Type" is "scaffold": A question that guides the student towards the solution, with an exact answer
    "Answer": Exact answer to the question under "Body Text" (if "Row Type" is "step" or "scaffold"; null otherwise),
    "answerType": Indicates whether Answer to question is numeric, algebra, or mc (if "Row Type" is "step" or "scaffold"; null otherwise),
    "HintID": Takes the form "h1", "h2", "h3" etc. Within a step, HintID should simply increase by 1 for each successive hint or scaffold. HintID resets at every new step. (if "Row Type" is "hint" or "scaffold"; null otherwise),
    "Dependency": Indicates if the current hint or scaffold depends on previous hint(s) or scaffold(s). If dependent on multiple previous hints, write all separated by commas. (null if h1 or no dependency),
    "mcChoices": Provides multiple choice answers separated by "|" (only applies if "answerType" is "mc"; leave blank otherwise)
}

"answerType" "numeric" means the answer must be given as an exact number.
"answerType" "algebra" means any numerical expression that evaluates to the value of "Answer" is accepted.
"answerType" "mc" means any number or string answer, and "mcChoices" must contain several plausible choices.

"Answer" MUST be type int or float unless "answerType" is "mc".
If "Answer" must have type string, make it a multiple choice question (this includes "%" and any other units/words).
If "Answer" is an approximation and/or a student would not realistically be able to arrive at the exact answer themselves, make it a multiple choice question.
If a question has multiple answers, either split it into multiple questions or include ALL answers under one mc choice (ex: 52,31|25,64|...).
Each question may have multiple hints and/or scaffolds, based on how many are needed to arrive at the answer.

Here are some examples, follow their format exactly: \n
"""


samples = pd.read_excel("OATutor Training OpenAI API.xlsx", sheet_name="Training")
samples_json = samples.to_json(orient="records")
parsed = json.loads(samples_json)

sample1 = json.dumps(parsed[:9], indent=4)
sample2 = json.dumps(parsed[9:15], indent=4)
sample3 = json.dumps(parsed[15:], indent=4)

sample_questions = [
    {
        "Topic": "Kinetic Energy and the Work-Energy Theorem",
        "Problem Name": "work",
        "Questions": [
            """
            a) A shopper pushes a grocery cart 20.0 m at constant speed on level ground, against a 35.0 N frictional force. He pushes in a direction 25.0º below the horizontal. What is the work done on the cart by friction?
            b) What is the work done on the cart by the gravitational force?,
            """,
            "Compare the kinetic energy of a 20,000-kg truck moving at 110 km/h with that of an 80.0-kg astronaut in orbit moving at 27,500 km/h as a ratio.",
            "A person’s blood pressure is measured to be 120 +/- 2mm Hg. What is its percent uncertainty?"
        ]
    },
    {
        "Topic": "Gravitational Potential Energy",
        "Problem Name": "gravitational",
        "Questions": [
            "A hydroelectric power facility converts the gravitational potential energy of water behind a dam to electric energy. What is the gravitational potential energy relative to the generators of a lake of volume 50.0 km^3 (mass=5.00×10^13kg), given that the lake has an average height of 40.0 m above the generators?"
        ]
    }
]

def question_formatter(questions):
    question_list = []
    for i in questions:
        for j in range(len(i['Questions'])):
            one_q = f"""
Human:
    Problem Name: {i['Problem Name']}{j+1}
    Topic: {i['Topic']}
    Question: {i['Questions'][j]}
AI:
"""
            question_list.append(one_q)
    return question_list


s_list = question_formatter(sample_questions)
sample_str = s_list[0] + str(sample1) + s_list[1] + str(sample2) + s_list[2] + str(sample3)
