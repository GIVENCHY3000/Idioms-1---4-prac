import streamlit as st
import random

# --- Idioms database ---
idioms = {
    "Idioms 1": {
        "I tried to call him several times but couldn’t __________.": "get ahold of",
        "After the campaign, sales __________.": "went through the roof",
        "She always tries to __________ for her clients.": "go the extra mile",
        "The government finally __________ the new project.": "gave a green light to",
        "Trying to convince him is just __________.": "flogging a dead horse",
        "We need to __________ to solve this creatively.": "think outside the box",
        "I read blogs daily to __________ with tech news.": "keep up to date"
    },
    "Idioms 2": {
        "That idea didn’t work, so we have to __________.": "go back to the drawing board",
        "Your answer was __________ – completely wrong.": "way off the mark",
        "Let’s __________ the design a little before launching.": "tweak",
        "I’ll keep you __________ about any updates.": "in the loop",
        "Sorry, I can’t help – I’ve got __________.": "a lot on my plate",
        "As a __________, we spend 10% of budget on ads.": "rule of thumb",
        "He wanted to __________ about what really happened.": "set the record straight",
        "We had to __________ the less important project.": "put it on the back burner",
        "The company decided to __________ the project completely.": "pull the plug",
        "In __________, the project was a success.": "a nutshell",
        "Can you __________ the new intern to speed?": "bring her up to speed",
        "The boss is __________ in this company.": "calling the shots"
    },
    "Idioms 3": {
        "It’s been hard, but we’re managing to __________ financially.": "keep our heads above water",
        "Sales __________ after the campaign.": "rocketed",
        "Funding has completely __________.": "dried up",
        "When it comes to opportunities, __________.": "the sky’s the limit",
        "Don’t worry, he’ll __________ after this failure.": "bounce back",
        "Luckily, the project had __________.": "a safe landing",
        "The economy experienced some __________ last year.": "turbulence",
        "Our business really started to __________ last month.": "take off",
        "Profits __________ by 40% this year.": "plunged",
        "We had __________ of applications for the job.": "a flood",
        "The project __________ and was an instant success.": "got off to a flying start",
        "The company’s shares continue to __________.": "soar",
        "The market is very __________ right now.": "buoyant",
        "The stock prices have __________ recently.": "taken a nosedive",
        "The economy is still __________.": "in the doldrums",
        "We need to __________ the new campaign.": "give it a kick start",
        "It’s a __________, but it might work.": "a long shot",
        "They __________ by announcing the deal too early.": "jumped the gun",
        "I’ve done my part – now __________.": "the ball is in your court",
        "The government had to __________ the bank.": "bail out",
        "That amount is just __________ compared to what we need.": "a drop in the ocean",
        "The critics __________ the new proposal.": "threw cold water on",
        "We need to __________ to finish this project.": "rally the troops"
    },
    "Idioms 4": {
        "Give me __________, not an exact number.": "a ballpark figure",
        "We finally __________ the differences in the contract.": "ironed out",
        "If this fails, __________ will.": "heads will roll",
        "He works hard and really __________.": "brings home the bacon",
        "The new iPhone is __________ in stores.": "selling like hotcakes",
        "They are just __________ the problem instead of solving it.": "throwing money at",
        "We had to __________ to save costs.": "cut corners",
        "Let’s __________ and launch it now!": "strike while the iron is hot",
        "He’s been __________ since losing his job.": "living from hand to mouth",
        "The cashier had __________ – he was stealing.": "sticky fingers",
        "That watch will __________ you.": "pay an arm and a leg",
        "We need to __________ because of inflation.": "tighten our belts"
    }
}

# --- UI ---
st.title("🎓 Idioms Exam Trainer")

theme = st.selectbox("Выбери тему:", ["Idioms 1", "Idioms 2", "Idioms 3", "Idioms 4", "Mixed"])

# --- Выбор базы ---
if theme == "Mixed":
    selected = {k: v for d in idioms.values() for k, v in d.items()}
else:
    selected = idioms[theme]

# --- State ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "question" not in st.session_state:
    st.session_state.question = random.choice(list(selected.keys()))
    st.session_state.answer = selected[st.session_state.question]

# --- Question ---
st.subheader("Вопрос:")
st.write(st.session_state.question)

user_answer = st.text_input("Твой ответ:")

if st.button("Проверить"):
    if user_answer.lower().strip() == st.session_state.answer.lower().strip():
        st.success("✅ Верно!")
        st.session_state.score += 25
    else:
        st.error(f"❌ Неверно! Правильный ответ: {st.session_state.answer}")
        st.session_state.score -= 25

    # Следующий вопрос
    st.session_state.question = random.choice(list(selected.keys()))
    st.session_state.answer = selected[st.session_state.question]

st.metric("Очки", st.session_state.score)
