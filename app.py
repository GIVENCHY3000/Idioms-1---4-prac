import streamlit as st
import random
import base64

st.set_page_config(page_title="Idioms Trainer", page_icon="📘", layout="centered")

# ----------------------- Styling -----------------------
st.markdown("""
<style>
.big-btn button {font-size:1.05rem; padding:0.6rem 1.2rem; border-radius:12px}
.score-badge {display:inline-block; padding:.35rem .8rem; border-radius:999px; background:#eef6ff; color:#1f4b99; font-weight:600}
.card {background:#111418; border:1px solid #1f2430; padding:22px; border-radius:16px; box-shadow: 0 6px 24px rgba(0,0,0,.25)}
.prompt {font-size:1.15rem; line-height:1.55rem}
.feedback {margin-top:.5rem; font-size:1rem}
.subtle {color:#94a3b8}
</style>
""", unsafe_allow_html=True)

# ----------------------- Typing ambience (base64 in-code) -----------------------
# Мягкий лофай-петлевой звук (очень тихий). Можно выключить тумблером.
AUDIO_B64 = """
UklGRmQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABYAAAACAAACAAABAAAAAAAAPwAAAP8AAP8A
AP///wAAAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8A
"""  # короткий "тиш-шур" (заглушка); браузер зациклит его. сделано ultra-тихо

def audio_tag(base64_data: str):
    return f"""
    <audio autoplay loop>
      <source src="data:audio/wav;base64,{base64_data.strip()}" type="audio/wav">
    </audio>
    """

# ----------------------- Helpers -----------------------
def norm(s: str) -> str:
    return " ".join(s.lower().strip().replace("—","-").replace("–","-").split())

def pick(*xs):
    return random.choice(xs)

# ----------------------- Idioms DB (с генераторами формулировок) -----------------------
# === Idioms 1
IDIOMS_1 = {
    "get_ahold_of": {"answer": "get ahold of", "gen": lambda: pick(
        "I tried to call him several times but couldn’t __________.",
        "I emailed her yesterday, but still can’t __________ her.",
        "Could you please __________ the supplier this afternoon?",
        "I wasn’t able to __________ my manager; his phone was off.",
        "Before the meeting, try to __________ all the participants.",
        "It took me hours to __________ the customer."
    )},
    "went_through_the_roof": {"answer": "went through the roof", "gen": lambda: pick(
        "After the new campaign, sales __________.",
        "Prices __________ last month due to inflation.",
        "When he heard the bad news, his anger __________.",
        "During Black Friday, demand just __________.",
        "The number of sign-ups suddenly __________ overnight.",
        "Our energy bill __________ in winter."
    )},
    "go_the_extra_mile": {"answer": "go the extra mile", "gen": lambda: pick(
        "She always tries to __________ for her clients.",
        "If you want this job, you need to __________ on the project.",
        "Good customer service means staff who __________.",
        "He decided to __________ and stay late to finish the task.",
        "Winners are those who consistently __________.",
        "Our team is ready to __________ to meet the deadline."
    )},
    "give_green_light": {"answer": "gave a green light to", "gen": lambda: pick(
        "The government finally __________ the new project.",
        "The board __________ the merger after months of talks.",
        "Our manager __________ the marketing plan.",
        "Investors __________ the second funding round.",
        "The committee __________ the pilot program.",
        "The CEO __________ the product launch."
    )},
    "flogging_dead_horse": {"answer": "flogging a dead horse", "gen": lambda: pick(
        "Trying to convince him is just __________.",
        "Fixing that ancient printer is like __________.",
        "Pushing this failed idea any further is __________.",
        "Arguing with her about it is __________.",
        "Reopening that closed issue feels like __________.",
        "At this point, discussing budget cuts is __________."
    )},
    "think_outside_box": {"answer": "think outside the box", "gen": lambda: pick(
        "We need to __________ to solve this creatively.",
        "The brief asks us to __________ and find a fresh angle.",
        "Innovative teams constantly __________.",
        "To win this tender, we must __________.",
        "Great designers always __________.",
        "The coach told us to __________ during the workshop."
    )},
    "keep_up_to_date": {"answer": "keep up to date", "gen": lambda: pick(
        "I read blogs daily to __________ with tech news.",
        "To stay competitive, marketers must __________ with trends.",
        "Engineers need to __________ with new standards.",
        "I subscribe to newsletters to __________ on industry changes.",
        "HR should __________ with legal requirements.",
        "Doctors must __________ with the latest research."
    )},
}

# === Idioms 2
IDIOMS_2 = {
    "drawing_board": {"answer":"go back to the drawing board","gen":lambda: pick(
        "That idea didn’t work, so we have to __________.",
        "The prototype failed; time to __________.",
        "The client rejected it; let's __________ and rethink.",
        "We missed the target — we must __________.",
        "Budget cuts force us to __________.",
        "It’s not viable yet; better __________."
    )},
    "way_off": {"answer":"way off the mark","gen":lambda: pick(
        "Your estimate was __________ — completely wrong.",
        "That forecast is __________; check the data.",
        "The assumptions were __________ this quarter.",
        "Sorry, your guess is __________.",
        "Our pricing was __________ compared to rivals.",
        "The timeline was __________ from reality."
    )},
    "tweak": {"answer":"tweak","gen":lambda: pick(
        "Let’s __________ the design a little before launching.",
        "We just need to __________ the wording on slide 3.",
        "Can you __________ the layout to improve readability?",
        "We’ll __________ the color palette and test again.",
        "Please __________ the copy to sound more formal.",
        "They asked us to __________ the pricing model."
    )},
    "in_the_loop": {"answer":"in the loop","gen":lambda: pick(
        "I’ll keep you __________ about any updates.",
        "Please keep finance __________ on this deal.",
        "Stay __________ as we roll out the changes.",
        "Add me __________ regarding supplier talks.",
        "Keep the team __________ during migration.",
        "Are all stakeholders __________?"
    )},
    "a_lot_on_my_plate": {"answer":"a lot on my plate","gen":lambda: pick(
        "Sorry, I can’t help — I’ve got __________.",
        "He’s stressed because he has __________ at work.",
        "She’s juggling kids and studies — really __________.",
        "The PM has __________ this sprint.",
        "We all have __________ before year-end.",
        "Don’t overload John; he already has __________."
    )},
    "rule_of_thumb": {"answer":"rule of thumb","gen":lambda: pick(
        "As a __________, we spend 10% of budget on ads.",
        "A good __________ is to double-check contracts.",
        "By __________, save 20% for taxes.",
        "A common __________ is to test with 5 users.",
        "Use the __________: measure twice, cut once.",
        "As a simple __________, ship small and often."
    )},
    "set_record_straight": {"answer":"set the record straight","gen":lambda: pick(
        "He wanted to __________ about what really happened.",
        "Let me __________ regarding the delays.",
        "PR must __________ after the rumor.",
        "We should __________ in tomorrow’s memo.",
        "The CEO will __________ in the interview.",
        "It’s time to __________ with the stakeholders."
    )},
    "back_burner": {"answer":"put it on the back burner","gen":lambda: pick(
        "We had to __________ the less important project.",
        "Let’s __________ until Q4.",
        "Due to costs, we’ll __________ the app redesign.",
        "They decided to __________ hiring plans.",
        "We can __________ research for now.",
        "I’ll __________ that idea until resources free up."
    )},
    "pull_the_plug": {"answer":"pull the plug","gen":lambda: pick(
        "The company decided to __________ the project completely.",
        "Investors may __________ if KPIs aren’t met.",
        "The board will __________ next week.",
        "They threatened to __________ on funding.",
        "We had to __________ after repeated failures.",
        "The sponsor might __________ due to risk."
    )},
    "in_a_nutshell": {"answer":"in a nutshell","gen":lambda: pick(
        "__________, the project was a success.",
        "__________, we need more time and money.",
        "__________, the plan failed due to scope creep.",
        "__________, users loved the prototype.",
        "__________, we’re staying the course.",
        "__________, the merger is postponed."
    )},
    "bring_up_to_speed": {"answer":"bring her up to speed","gen":lambda: pick(
        "Can you __________ the new intern to speed?",
        "I’ll __________ the trainee to speed today.",
        "Please __________ the new PM to speed on this.",
        "We must __________ everyone to speed before launch.",
        "Help me __________ the team to speed by Monday.",
        "HR will __________ newcomers to speed."
    )},
    "calling_the_shots": {"answer":"calling the shots","gen":lambda: pick(
        "The boss is __________ in this company.",
        "Who’s actually __________ on this project?",
        "She’s the one __________ here.",
        "Legal is __________ regarding contracts.",
        "The sponsor is __________ now.",
        "Ultimately, the board is __________."
    )},
}

# === Idioms 3
IDIOMS_3 = {
    "heads_above_water":{"answer":"keep our heads above water","gen":lambda: pick(
        "It’s been hard, but we’re managing to __________ financially.",
        "With rising costs, we barely __________.",
        "Freelancers struggle to __________ in summer.",
        "Restaurants tried to __________ during lockdowns.",
        "We cut expenses to __________ this quarter.",
        "They took a loan to __________."
    )},
    "rocketed":{"answer":"rocketed","gen":lambda: pick(
        "Sales __________ after the campaign.",
        "Downloads __________ in one day.",
        "The price __________ to a record high.",
        "Registrations __________ last night.",
        "Visits __________ during the livestream.",
        "Their popularity __________ on TikTok."
    )},
    "dried_up":{"answer":"dried up","gen":lambda: pick(
        "Funding has completely __________.",
        "The leads __________ this month.",
        "Tourism __________ in winter.",
        "Orders __________ after the scandal.",
        "The cash flow __________ suddenly.",
        "New applicants __________ recently."
    )},
    "skys_limit":{"answer":"the sky’s the limit","gen":lambda: pick(
        "When it comes to opportunities, __________.",
        "With AI, __________ for innovation.",
        "For a talent like her, __________.",
        "In this market, __________ if we execute well.",
        "With this budget, __________.",
        "For creative ideas, __________."
    )},
    "bounce_back":{"answer":"bounce back","gen":lambda: pick(
        "Don’t worry, he’ll __________ after this failure.",
        "The brand will __________ next quarter.",
        "Athletes can __________ from injuries.",
        "Small caps may __________ in H2.",
        "Tourism tends to __________ in spring.",
        "We expect stocks to __________ soon."
    )},
    "safe_landing":{"answer":"a safe landing","gen":lambda: pick(
        "Luckily, the project had __________.",
        "We managed __________ despite the risks.",
        "Policy changes ensured __________.",
        "Hedging gave us __________.",
        "Careful planning led to __________.",
        "Diversification helped achieve __________."
    )},
    "turbulence":{"answer":"turbulence","gen":lambda: pick(
        "The economy experienced some __________ last year.",
        "Markets faced heavy __________ in May.",
        "Expect __________ during the transition.",
        "There was __________ after the announcement.",
        "We’re entering a phase of __________.",
        "Political news created __________."
    )},
    "take_off":{"answer":"take off","gen":lambda: pick(
        "Our business really started to __________ last month.",
        "The new feature helped the product __________.",
        "Her career began to __________ after the award.",
        "Subscriptions will __________ with ads.",
        "The channel will __________ after shorts.",
        "The brand is ready to __________ this season."
    )},
    "plunged":{"answer":"plunged","gen":lambda: pick(
        "Profits __________ by 40% this year.",
        "The stock __________ at the open.",
        "Revenue __________ after churn rose.",
        "User time __________ post-update.",
        "Confidence __________ overnight.",
        "The index __________ on Monday."
    )},
    "a_flood":{"answer":"a flood","gen":lambda: pick(
        "We had __________ of applications for the job.",
        "There was __________ of support from users.",
        "They received __________ of complaints.",
        "We saw __________ of preorders.",
        "The inbox got __________ of messages.",
        "PR got __________ of press requests."
    )},
    "flying_start":{"answer":"got off to a flying start","gen":lambda: pick(
        "The project __________ and was an instant success.",
        "Her campaign __________ in the first week.",
        "The show __________ with record ratings.",
        "The venture __________ thanks to influencers.",
        "Negotiations __________ after the intro call.",
        "Sales __________ this quarter."
    )},
    "soar":{"answer":"soar","gen":lambda: pick(
        "The company’s shares continue to __________.",
        "Premium demand will __________ in Q4.",
        "Engagement tends to __________ with giveaways.",
        "Profits may __________ as costs fall.",
        "Expect conversion to __________ after redesign.",
        "Flights bookings will __________ in summer."
    )},
    "buoyant":{"answer":"buoyant","gen":lambda: pick(
        "The market is very __________ right now.",
        "Investor sentiment remains __________.",
        "Demand for EVs is __________.",
        "The mood stays __________ despite risks.",
        "Hiring remains __________ in tech.",
        "Exports look __________ this year."
    )},
    "nosedive":{"answer":"taken a nosedive","gen":lambda: pick(
        "The stock prices have __________ recently.",
        "Confidence has __________ since the scandal.",
        "User growth has __________ after changes.",
        "Ad revenue has __________ this quarter.",
        "Attendance has __________ lately.",
        "The currency has __________ again."
    )},
    "doldrums":{"answer":"in the doldrums","gen":lambda: pick(
        "The economy is still __________.",
        "PC sales remain __________.",
        "Housing is __________ for months.",
        "The team felt __________ before the win.",
        "Startups are __________ amid rates.",
        "Crypto is __________ this season."
    )},
    "kick_start":{"answer":"give it a kick start","gen":lambda: pick(
        "We need to __________ the new campaign.",
        "A discount will __________ sales.",
        "Influencers could __________ growth.",
        "Let’s __________ the project with a sprint.",
        "Ads should __________ demand.",
        "PR will __________ awareness."
    )},
    "long_shot":{"answer":"a long shot","gen":lambda: pick(
        "It’s __________, but it might work.",
        "Landing that client is __________.",
        "Winning now is __________ at best.",
        "Beating the record is __________.",
        "Raising now is __________ in this market.",
        "This hypothesis is __________."
    )},
    "jumped_gun":{"answer":"jumped the gun","gen":lambda: pick(
        "They __________ by announcing the deal too early.",
        "We __________ with the press release.",
        "The team __________ before QA finished.",
        "She __________ by hiring first.",
        "He __________ posting results.",
        "Marketing __________ with the teaser."
    )},
    "ball_in_your_court":{"answer":"the ball is in your court","gen":lambda: pick(
        "I’ve done my part — now __________.",
        "We sent the offer; __________.",
        "Over to you — __________.",
        "We replied; __________ to accept or not.",
        "I gave the report; __________.",
        "Your move — __________."
    )},
    "bail_out":{"answer":"bail out","gen":lambda: pick(
        "The government had to __________ the bank.",
        "Taxpayers won’t __________ failing firms again.",
        "They asked the parent company to __________ them.",
        "Will the fund __________ the startup?",
        "Lenders agreed to __________ the airline.",
        "Investors refused to __________ the project."
    )},
    "drop_in_ocean":{"answer":"a drop in the ocean","gen":lambda: pick(
        "That amount is just __________ compared to what we need.",
        "Ten volunteers are __________ for this event.",
        "One scholarship is __________ given demand.",
        "This budget is __________ for global rollout.",
        "Those savings are __________ against our debt.",
        "These fines are __________ for the giant."
    )},
    "cold_water_on":{"answer":"threw cold water on","gen":lambda: pick(
        "The critics __________ the new proposal.",
        "Legal __________ our timeline.",
        "Finance __________ the expansion plan.",
        "Security concerns __________ the idea.",
        "The board __________ our optimism.",
        "Early feedback __________ the concept."
    )},
    "rally_troops":{"answer":"rally the troops","gen":lambda: pick(
        "We need to __________ to finish this project.",
        "The coach tried to __________ before the final.",
        "Let’s __________ for the last sprint.",
        "Leaders must __________ during crises.",
        "We’ll __________ for the big release.",
        "Time to __________ and push together."
    )},
}

# === Idioms 4
IDIOMS_4 = {
    "ballpark":{"answer":"a ballpark figure","gen":lambda: pick(
        "Give me __________, not an exact number.",
        "What’s __________ for the total cost?",
        "Can you provide __________ for headcount?",
        "Just __________ will do for now.",
        "We need __________ for the brief.",
        "Any __________ is fine at this stage."
    )},
    "ironed_out":{"answer":"ironed out","gen":lambda: pick(
        "We finally __________ the differences in the contract.",
        "The teams __________ most issues.",
        "They __________ the bugs before launch.",
        "We __________ the details yesterday.",
        "Legal and sales __________ the conflicts.",
        "They __________ the remaining problems."
    )},
    "heads_will_roll":{"answer":"heads will roll","gen":lambda: pick(
        "If this fails, __________ will.",
        "When the audit ends, __________.",
        "If the leak continues, __________.",
        "If KPIs aren’t met, __________.",
        "Mess this up and __________.",
        "When the boss returns, __________."
    )},
    "brings_bacon":{"answer":"brings home the bacon","gen":lambda: pick(
        "He works hard and really __________.",
        "She __________ for the whole family.",
        "That product __________ for the company.",
        "Our services __________ these days.",
        "He’s the one who __________ here.",
        "This client __________ for us."
    )},
    "hotcakes":{"answer":"selling like hotcakes","gen":lambda: pick(
        "The new phone is __________ in stores.",
        "Those sneakers are __________ online.",
        "Tickets are __________ this morning.",
        "The limited edition is __________.",
        "Her merch is __________ already.",
        "Subscriptions are __________ today."
    )},
    "throwing_money":{"answer":"throwing money at","gen":lambda: pick(
        "They are just __________ the problem instead of solving it.",
        "Stop __________ marketing; fix the product.",
        "We’re __________ ads without strategy.",
        "Management keeps __________ symptoms.",
        "Investors are __________ growth issues.",
        "He thinks __________ everything helps."
    )},
    "cut_corners":{"answer":"cut corners","gen":lambda: pick(
        "We had to __________ to save costs.",
        "Some builders __________ on safety.",
        "Don’t __________ with security.",
        "They __________ and shipped buggy code.",
        "Never __________ on QA.",
        "The vendor __________ to meet the deadline."
    )},
    "strike_while":{"answer":"strike while the iron is hot","gen":lambda: pick(
        "Let’s __________ and launch it now!",
        "We should __________ before rivals react.",
        "Marketing wants to __________ today.",
        "Invest now — __________.",
        "We must __________ after this hype.",
        "Time to __________ and close the deal."
    )},
    "hand_to_mouth":{"answer":"living from hand to mouth","gen":lambda: pick(
        "He’s been __________ since losing his job.",
        "Many artists are __________ these days.",
        "Families are __________ after layoffs.",
        "They’re __________ on minimum wage.",
        "Students are __________ till summer.",
        "Refugees are __________ for months."
    )},
    "sticky_fingers":{"answer":"sticky fingers","gen":lambda: pick(
        "The cashier had __________ — he was stealing.",
        "Beware of staff with __________.",
        "The intern showed __________ at the store.",
        "Someone here has __________.",
        "They fired him for __________.",
        "Audit revealed __________ in accounting."
    )},
    "arm_leg":{"answer":"pay an arm and a leg","gen":lambda: pick(
        "That watch will __________ you.",
        "We had to __________ for the seats.",
        "You’ll __________ for that repair.",
        "They’ll __________ for this view.",
        "Expect to __________ in that city.",
        "He had to __________ for tuition."
    )},
    "tighten_belts":{"answer":"tighten our belts","gen":lambda: pick(
        "We need to __________ because of inflation.",
        "After Q1 losses, we must __________.",
        "Households will __________ this year.",
        "Let’s __________ until cash improves.",
        "Time to __________ and cut extras.",
        "We’ll __________ over winter."
    )},
}

TOPICS = {
    "Idioms 1": IDIOMS_1,
    "Idioms 2": IDIOMS_2,
    "Idioms 3": IDIOMS_3,
    "Idioms 4": IDIOMS_4,
}

# ----------------------- State -----------------------
if "score" not in st.session_state: st.session_state.score = 0
if "streak" not in st.session_state: st.session_state.streak = 0
if "q_count" not in st.session_state: st.session_state.q_count = 0
if "locked" not in st.session_state: st.session_state.locked = False  # блок после проверки
if "cur_key" not in st.session_state: st.session_state.cur_key = None
if "cur_ans" not in st.session_state: st.session_state.cur_ans = ""
if "cur_prompt" not in st.session_state: st.session_state.cur_prompt = ""
if "feedback" not in st.session_state: st.session_state.feedback = ""

MAX_Q = 10

# ----------------------- Header -----------------------
st.title("🎓 Idioms Exam Trainer")
cols = st.columns([1,1,1])
with cols[0]:
    theme = st.selectbox("Тема", ["Idioms 1","Idioms 2","Idioms 3","Idioms 4","Mixed"])
with cols[1]:
    ambience = st.toggle("🎧 typing ambience", value=True)
with cols[2]:
    if st.button("🔁 Restart"):
        for k in ["score","streak","q_count","locked","cur_key","cur_ans","cur_prompt","feedback"]:
            st.session_state.pop(k, None)
        st.rerun()

if ambience:
    st.markdown(audio_tag(AUDIO_B64), unsafe_allow_html=True)

# Пул вопросов
if theme == "Mixed":
    pool = {}
    for d in TOPICS.values(): pool.update(d)
else:
    pool = TOPICS[theme]

# Инициализация первого вопроса
def new_question(change_key=True):
    if change_key or not st.session_state.cur_key:
        st.session_state.cur_key = random.choice(list(pool.keys()))
    st.session_state.cur_ans = pool[st.session_state.cur_key]["answer"]
    st.session_state.cur_prompt = pool[st.session_state.cur_key]["gen"]()

if not st.session_state.cur_key:
    new_question(change_key=True)

# ----------------------- Progress -----------------------
st.progress(st.session_state.q_count / MAX_Q)
st.markdown(f"**Question:** {st.session_state.q_count+1 if st.session_state.q_count<MAX_Q else MAX_Q} / {MAX_Q}")
st.markdown(f"<span class='score-badge'>Score: {st.session_state.score} • Streak: {st.session_state.streak}</span>", unsafe_allow_html=True)

# ----------------------- Card -----------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown(f"<div class='prompt'>✍️ {st.session_state.cur_prompt}</div>", unsafe_allow_html=True)

user = st.text_input("Your answer:")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("✅ Check", disabled=st.session_state.locked or st.session_state.q_count>=MAX_Q, help="Проверить ответ"):
        correct = norm(user) == norm(st.session_state.cur_ans)
        st.session_state.locked = True

        if correct:
            st.session_state.streak += 1
            st.session_state.score += 25
            bonus_msg = ""
            if st.session_state.streak > 0 and st.session_state.streak % 3 == 0:
                st.session_state.score += 50
                bonus_msg = " (+50 streak bonus)"
            st.session_state.feedback = f"✅ Correct! +25{bonus_msg}"
        else:
            st.session_state.streak = 0
            st.session_state.score -= 25
            st.session_state.feedback = f"❌ Wrong. Right answer: **{st.session_state.cur_ans}**  (−25)"

with c2:
    if st.button("➡️ Next", disabled=not st.session_state.locked or st.session_state.q_count>=MAX_Q):
        st.session_state.q_count += 1
        st.session_state.locked = False
        st.session_state.feedback = ""
        new_question(change_key=True)

with c3:
    if st.button("↻ Rephrase", disabled=st.session_state.locked or st.session_state.q_count>=MAX_Q, help="Другая формулировка той же идиомы"):
        new_question(change_key=False)

st.markdown(f"<div class='feedback'>{st.session_state.feedback}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ----------------------- Finish screen -----------------------
if st.session_state.q_count >= MAX_Q:
    st.success("🏁 Done! Вот твой результат.")
    accuracy = max(0, round((st.session_state.score + 25*MAX_Q) / (50*MAX_Q) * 100))
    # эвристика для процента (если все правильно: 100; если все неправильно: 0)
    st.write(f"**Final score:** {st.session_state.score}")
    st.write(f"**Accuracy (rough):** {accuracy}%")
    if st.button("Play again"):
        for k in ["score","streak","q_count","locked","cur_key","cur_ans","cur_prompt","feedback"]:
            st.session_state.pop(k, None)
        st.rerun()
