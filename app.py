import streamlit as st
import random

st.set_page_config(page_title="Idioms Trainer", page_icon="📘")

# -----------------------
# Helpers
# -----------------------
def norm(s: str) -> str:
    return " ".join(s.lower().strip().replace("—","-").replace("–","-").split())

def pick(*xs):
    return random.choice(xs)

# -----------------------
# Idioms base (answers) + generators
# Каждый элемент: idiom_key -> {"answer": "...", "gen": function()->prompt}
# -----------------------

# Idioms 1
IDIOMS_1 = {
    "get_ahold_of": {
        "answer": "get ahold of",
        "gen": lambda: pick(
            "I tried to call him several times but couldn’t __________.",
            "I emailed her yesterday, but still can’t __________ her.",
            "Could you please __________ the supplier this afternoon?",
            "I wasn’t able to __________ my manager; his phone was off.",
            "Before the meeting, try to __________ all the participants.",
            "It took me hours to __________ the customer."
        )
    },
    "went_through_the_roof": {
        "answer": "went through the roof",
        "gen": lambda: pick(
            "After the new campaign, sales __________.",
            "Prices __________ last month due to inflation.",
            "When he heard the bad news, his anger __________.",
            "During Black Friday, demand just __________.",
            "The number of sign-ups suddenly __________ overnight.",
            "Our energy bill __________ in winter."
        )
    },
    "go_the_extra_mile": {
        "answer": "go the extra mile",
        "gen": lambda: pick(
            "She always tries to __________ for her clients.",
            "If you want this job, you need to __________ on the project.",
            "Good customer service means staff who __________.",
            "He decided to __________ and stay late to finish the task.",
            "Winners are those who consistently __________.",
            "Our team is ready to __________ to meet the deadline."
        )
    },
    "give_green_light": {
        "answer": "gave a green light to",
        "gen": lambda: pick(
            "The government finally __________ the new project.",
            "The board __________ the merger after months of talks.",
            "Our manager __________ the marketing plan.",
            "Investors __________ the second funding round.",
            "The committee __________ the pilot program.",
            "The CEO __________ the product launch."
        )
    },
    "flogging_dead_horse": {
        "answer": "flogging a dead horse",
        "gen": lambda: pick(
            "Trying to convince him is just __________.",
            "Fixing that ancient printer is like __________.",
            "Pushing this failed idea any further is __________.",
            "Arguing with her about it is __________.",
            "Reopening that closed issue feels like __________.",
            "At this point, discussing budget cuts is __________."
        )
    },
    "think_outside_box": {
        "answer": "think outside the box",
        "ge
