import json
import pandas as pd
from openai import OpenAI
from prompts import *

api_key = "<API-KEY>"
model = 'gpt-4'

client = OpenAI(api_key=api_key)
rows = []

questions = [
    {
        "Topic": "The Second Condition for Equilibrium",
        "Problem Name": "equilibrium",
        "Questions": [
            "Two children are balanced on a seesaw of negligible mass. The first child has a mass of 26.0 kg and sits 1.60 m from the pivot. If the second child has a mass of 32.0 kg, how far is she from the pivot?",
            "When opening a door, you push on it perpendicularly with a force of 55.0 N at a distance of 0.850m from the hinges. What torque are you exerting relative to the hinges (in Nm)?",
            "What minimum force must you exert to apply a force of 1250 N to a nail using a nail puller where you exert a force 45 cm from the pivot and the nail is 1.8 cm on the other side?"
        ]
    },
    {
        "Topic": "Physical Quantities and Units",
        "Problem Name": "physical",
        "Questions": [
            """
            a) The speed limit on some interstate highways is roughly 100 km/h. What is this in meters per second?
            b) How many miles per hour is this?
            """,
            "What is the height in meters of a person who is 6 ft 1.0 in. tall? (Assume that 1 meter equals 39.37 in.)"
        ]
    },
    {
        "Topic": "Accuracy, Precision, and Significant Figures",
        "Problem Name": "accuracy",
        "Questions": [
            "Suppose that your bathroom scale reads your mass as 65 kg with a 3% uncertainty. What is the uncertainty in your mass (in kilograms)?",
            "What is the area of a circle 3.102cm in diameter?",
            "A person’s blood pressure is measured to be 120 +/- 2mm Hg. What is its percent uncertainty?"
        ]
    },
    {
        "Topic": "Projectile Motion",
        "Problem Name": "projectile",
        "Questions": [
            """
            a) A projectile is launched at ground level with an initial speed of 50.0 m/s at an angle of 30.0º above the horizontal. It strikes a target above the ground 3.00 seconds later. What is the x distance from where the projectile was launched to where it lands?
            b) What is the y distance from where the projectile was launched to where it lands?
            """,
            """
            a) A ball is thrown horizontally from the top of a 60.0-m building and lands 100.0 m from the base of the building. Ignore air resistance. How long is the ball in the air?
            b) What must have been the initial horizontal component of the velocity?
            """,
            "Can a goalkeeper at her/ his goal kick a soccer ball into the opponent’s goal without the ball touching the ground? The distance will be about 95 m. A goalkeeper can give the ball a speed of 30 m/s."
        ]
    },
    {
        "Topic": "Approximation",
        "Problem Name": "approximation",
        "Questions": [
            "How many heartbeats are there in a lifetime?",
            "A generation is about one-third of a lifetime. Approximately how many generations have passed since the year 0 AD?"
        ]
    },
    {
        "Topic": "Gravitational Potential Energy",
        "Problem Name": "gravitational",
        "Questions": [
            "A hydroelectric power facility converts the gravitational potential energy of water behind a dam to electric energy. What is the gravitational potential energy relative to the generators of a lake of volume 50.0 km^3 (mass=5.00×10^13kg), given that the lake has an average height of 40.0 m above the generators?",
            "Suppose a kookaburra (a large kingfisher bird) picks up a 75g snake and raises it 2.5 m from the ground to a branch. How much work did the bird do on the snake?"
        ]
    }
]

for i in question_formatter(questions[3:4]):
    prompt = instructions + sample_str + i

    messages = [{"role": "system", "content": prompt}]
    completion = client.chat.completions.create(model=model, messages=messages, temperature=0.1)

    response = completion.choices[0].message.content
    print(response)

    response_json = json.loads(response)
    rows.extend(response_json)

my_df = pd.DataFrame(rows)
my_df.to_excel("oatutor_proj-question_gpt-4.xlsx")