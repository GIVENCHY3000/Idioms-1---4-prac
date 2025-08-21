import streamlit as st
import random
import base64

st.set_page_config(page_title="Exam Trainer", page_icon="📘", layout="wide")

# =========================
# Global Styling (Times New Roman, slightly bolder)
# =========================
st.markdown('''
<style>
html, body, [class*="css"]  {
  font-family: "Times New Roman", Times, serif !important;
  font-weight: 500;
}
h1,h2,h3,h4 { font-weight: 700; }
.big-btn button {font-size:1.05rem; padding:0.6rem 1.2rem; border-radius:12px}
.score-badge {display:inline-block; padding:.35rem .8rem; border-radius:999px; background:#eef6ff; color:#1f4b99; font-weight:700}
.card {background:#111418; border:1px solid #1f2430; padding:22px; border-radius:16px; box-shadow: 0 6px 24px rgba(0,0,0,.25)}
.prompt {font-size:1.2rem; line-height:1.6rem}
.feedback {margin-top:.5rem; font-size:1rem}
.subtle {color:#94a3b8}
.cheat-wrap {background:#0e1117; border:1px solid #1f2430; border-radius:14px; padding:10px; overflow: hidden}
.cheat-blur {filter: blur(6px); pointer-events:none}
.cheat table {width:100%; border-collapse:separate; border-spacing:0 6px;}
.cheat th {text-align:left; font-weight:700; font-size:.95rem; color:#cbd5e1; padding:4px 6px;}
.cheat td {vertical-align:top; padding:6px 6px; background:#151a22; border-radius:10px; border:1px solid #1f2430; color:#e2e8f0; font-size:.92rem;}
.cheat td.acc {text-align:right; white-space:nowrap; color:#93c5fd; font-weight:700}
.fullref {max-height: 75vh; overflow: auto; border:1px solid #1f2430; border-radius:16px; padding:10px; background:#0e1117}
.fullref table {width:100%; border-collapse:separate; border-spacing:0 6px;}
.fullref th {text-align:left; font-weight:700; font-size:.95rem; color:#cbd5e1; padding:4px 6px;}
.fullref td {vertical-align:top; padding:6px 6px; background:#151a22; border-radius:10px; border:1px solid #1f2430; color:#e2e8f0; font-size:.92rem;}
.fullref td.acc {text-align:right; white-space:nowrap; color:#93c5fd; font-weight:700}
</style>
''', unsafe_allow_html=True)

# =========================
# Sounds: typing ambience (loop) + click (one-shot)
# =========================
AMBIENCE_B64 = """
UklGRmQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABYAAAACAAACAAABAAAAAAAAPwAAAP8AAP8AAP///wAAAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8AAP8A
"""
CLICK_B64 = """
UklGRgAAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABYAAAABAAAAgICAAP8AAP8A////AP8AAP8AgICA
"""  # короткий "тик" (очень тихо)

def audio_loop(b64):
    return f'''<audio autoplay loop style="display:none">
      <source src="data:audio/wav;base64,{b64.strip()}" type="audio/wav">
    </audio>'''

def audio_once(b64):
    return f'''<audio autoplay style="display:none">
      <source src="data:audio/wav;base64,{b64.strip()}" type="audio/wav">
    </audio>'''

# =========================
# Helpers
# =========================
def norm(s: str) -> str:
    return " ".join(s.lower().strip().replace("—","-").replace("–","-").split())

def pick(*xs):
    return random.choice(xs)

def make_item(answer, meaning, gens=None):
    # gens: list of generator lambdas returning a prompt string with blank
    if gens is None:
        gens = [
            lambda: f"In this course, we focus on __________, which means {meaning}.",
            lambda: f"The role requires __________: {meaning}.",
            lambda: f"One key challenge here is a lack of __________ ({meaning}).",
            lambda: f"To succeed, you need __________ — {meaning}.",
        ]
    return {"answer": answer, "meaning": meaning, "gen": lambda: random.choice(gens)()}

# =========================
# Idioms Data (answers + meaning + multiple generators each)
# =========================
IDIOMS_1 = {
    "get_ahold_of": make_item("get ahold of", "contact/reach someone", [
        lambda: "I tried to call him several times but couldn’t __________.",
        lambda: "I emailed her yesterday, but still can’t __________ her.",
        lambda: "Could you please __________ the supplier this afternoon?",
        lambda: "I wasn’t able to __________ my manager; his phone was off.",
        lambda: "Before the meeting, try to __________ all the participants.",
        lambda: "It took me hours to __________ the customer.",
    ]),
    "went_through_the_roof": make_item("went through the roof", "increase drastically / get very angry", [
        lambda: "After the new campaign, sales __________.",
        lambda: "Prices __________ last month due to inflation.",
        lambda: "When he heard the bad news, his anger __________.",
        lambda: "During Black Friday, demand just __________.",
        lambda: "The number of sign-ups suddenly __________ overnight.",
        lambda: "Our energy bill __________ in winter.",
    ]),
    "go_the_extra_mile": make_item("go the extra mile", "make more effort than expected", [
        lambda: "She always tries to __________ for her clients.",
        lambda: "If you want this job, you need to __________ on the project.",
        lambda: "Good customer service means staff who __________.",
        lambda: "He decided to __________ and stay late to finish the task.",
        lambda: "Winners are those who consistently __________.",
        lambda: "Our team is ready to __________ to meet the deadline.",
    ]),
    "give_green_light": make_item("gave a green light to", "approve / authorize", [
        lambda: "The government finally __________ the new project.",
        lambda: "The board __________ the merger after months of talks.",
        lambda: "Our manager __________ the marketing plan.",
        lambda: "Investors __________ the second funding round.",
        lambda: "The committee __________ the pilot program.",
        lambda: "The CEO __________ the product launch.",
    ]),
    "flogging_dead_horse": make_item("flogging a dead horse", "waste effort on something hopeless", [
        lambda: "Trying to convince him is just __________.",
        lambda: "Fixing that ancient printer is like __________.",
        lambda: "Pushing this failed idea any further is __________.",
        lambda: "Arguing with her about it is __________.",
        lambda: "Reopening that closed issue feels like __________.",
        lambda: "At this point, discussing budget cuts is __________.",
    ]),
    "think_outside_box": make_item("think outside the box", "think creatively/unconventionally", [
        lambda: "We need to __________ to solve this creatively.",
        lambda: "The brief asks us to __________ and find a fresh angle.",
        lambda: "Innovative teams constantly __________.",
        lambda: "To win this tender, we must __________.",
        lambda: "Great designers always __________.",
        lambda: "The coach told us to __________ during the workshop.",
    ]),
    "keep_up_to_date": make_item("keep up to date", "stay informed", [
        lambda: "I read blogs daily to __________ with tech news.",
        lambda: "To stay competitive, marketers must __________ with trends.",
        lambda: "Engineers need to __________ with new standards.",
        lambda: "I subscribe to newsletters to __________ on industry changes.",
        lambda: "HR should __________ with legal requirements.",
        lambda: "Doctors must __________ with the latest research.",
    ]),
}

IDIOMS_2 = {
    "drawing_board": make_item("go back to the drawing board", "start over / rethink", [
        lambda: "That idea didn’t work, so we have to __________.",
        lambda: "The prototype failed; time to __________.",
        lambda: "The client rejected it; let's __________ and rethink.",
        lambda: "We missed the target — we must __________.",
        lambda: "Budget cuts force us to __________.",
        lambda: "It’s not viable yet; better __________.",
    ]),
    "way_off": make_item("way off the mark", "completely wrong", [
        lambda: "Your estimate was __________ — completely wrong.",
        lambda: "That forecast is __________; check the data.",
        lambda: "The assumptions were __________ this quarter.",
        lambda: "Sorry, your guess is __________.",
        lambda: "Our pricing was __________ compared to rivals.",
        lambda: "The timeline was __________ from reality.",
    ]),
    "tweak": make_item("tweak", "make small adjustments", [
        lambda: "Let’s __________ the design a little before launching.",
        lambda: "We just need to __________ the wording on slide 3.",
        lambda: "Can you __________ the layout to improve readability?",
        lambda: "We’ll __________ the color palette and test again.",
        lambda: "Please __________ the copy to sound more formal.",
        lambda: "They asked us to __________ the pricing model.",
    ]),
    "in_the_loop": make_item("in the loop", "kept informed / included", [
        lambda: "I’ll keep you __________ about any updates.",
        lambda: "Please keep finance __________ on this deal.",
        lambda: "Stay __________ as we roll out the changes.",
        lambda: "Add me __________ regarding supplier talks.",
        lambda: "Keep the team __________ during migration.",
        lambda: "Are all stakeholders __________?",
    ]),
    "a_lot_on_my_plate": make_item("a lot on my plate", "many tasks/responsibilities", [
        lambda: "Sorry, I can’t help — I’ve got __________.",
        lambda: "He’s stressed because he has __________ at work.",
        lambda: "She’s juggling kids and studies — really __________.",
        lambda: "The PM has __________ this sprint.",
        lambda: "We all have __________ before year-end.",
        lambda: "Don’t overload John; he already has __________.",
    ]),
    "rule_of_thumb": make_item("rule of thumb", "general practical rule", [
        lambda: "As a __________, we spend 10% of budget on ads.",
        lambda: "A good __________ is to double-check contracts.",
        lambda: "By __________, save 20% for taxes.",
        lambda: "A common __________ is to test with 5 users.",
        lambda: "Use the __________: measure twice, cut once.",
        lambda: "As a simple __________, ship small and often.",
    ]),
    "set_record_straight": make_item("set the record straight", "clarify the truth", [
        lambda: "He wanted to __________ about what really happened.",
        lambda: "Let me __________ regarding the delays.",
        lambda: "PR must __________ after the rumor.",
        lambda: "We should __________ in tomorrow’s memo.",
        lambda: "The CEO will __________ in the interview.",
        lambda: "It’s time to __________ with the stakeholders.",
    ]),
    "back_burner": make_item("put it on the back burner", "postpone / de-prioritize", [
        lambda: "We had to __________ the less important project.",
        lambda: "Let’s __________ until Q4.",
        lambda: "Due to costs, we’ll __________ the app redesign.",
        lambda: "They decided to __________ hiring plans.",
        lambda: "We can __________ research for now.",
        lambda: "I’ll __________ that idea until resources free up.",
    ]),
    "pull_the_plug": make_item("pull the plug", "stop / terminate", [
        lambda: "The company decided to __________ the project completely.",
        lambda: "Investors may __________ if KPIs aren’t met.",
        lambda: "The board will __________ next week.",
        lambda: "They threatened to __________ on funding.",
        lambda: "We had to __________ after repeated failures.",
        lambda: "The sponsor might __________ due to risk.",
    ]),
    "in_a_nutshell": make_item("in a nutshell", "briefly / in short", [
        lambda: "__________, the project was a success.",
        lambda: "__________, we need more time and money.",
        lambda: "__________, the plan failed due to scope creep.",
        lambda: "__________, users loved the prototype.",
        lambda: "__________, we’re staying the course.",
        lambda: "__________, the merger is postponed.",
    ]),
    "bring_up_to_speed": make_item("bring her up to speed", "update someone quickly", [
        lambda: "Can you __________ the new intern to speed?",
        lambda: "I’ll __________ the trainee to speed today.",
        lambda: "Please __________ the new PM to speed on this.",
        lambda: "We must __________ everyone to speed before launch.",
        lambda: "Help me __________ the team to speed by Monday.",
        lambda: "HR will __________ newcomers to speed.",
    ]),
    "calling_the_shots": make_item("calling the shots", "being in control / making decisions", [
        lambda: "The boss is __________ in this company.",
        lambda: "Who’s actually __________ on this project?",
        lambda: "She’s the one __________ here.",
        lambda: "Legal is __________ regarding contracts.",
        lambda: "The sponsor is __________ now.",
        lambda: "Ultimately, the board is __________.",
    ]),
}

IDIOMS_3 = {
    "heads_above_water": make_item("keep our heads above water", "survive financially", [
        lambda: "It’s been hard, but we’re managing to __________ financially.",
        lambda: "With rising costs, we barely __________.",
        lambda: "Freelancers struggle to __________ in summer.",
        lambda: "Restaurants tried to __________ during lockdowns.",
        lambda: "We cut expenses to __________ this quarter.",
        lambda: "They took a loan to __________.",
    ]),
    "rocketed": make_item("rocketed", "increased very fast", [
        lambda: "Sales __________ after the campaign.",
        lambda: "Downloads __________ in one day.",
        lambda: "The price __________ to a record high.",
        lambda: "Registrations __________ last night.",
        lambda: "Visits __________ during the livestream.",
        lambda: "Their popularity __________ on TikTok.",
    ]),
    "dried_up": make_item("dried up", "dwindled / disappeared", [
        lambda: "Funding has completely __________.",
        lambda: "The leads __________ this month.",
        lambda: "Tourism __________ in winter.",
        lambda: "Orders __________ after the scandal.",
        lambda: "The cash flow __________ suddenly.",
        lambda: "New applicants __________ recently.",
    ]),
    "skys_limit": make_item("the sky’s the limit", "no limits to potential", [
        lambda: "When it comes to opportunities, __________.",
        lambda: "With AI, __________ for innovation.",
        lambda: "For a talent like her, __________.",
        lambda: "In this market, __________ if we execute well.",
        lambda: "With this budget, __________.",
        lambda: "For creative ideas, __________.",
    ]),
    "bounce_back": make_item("bounce back", "recover", [
        lambda: "Don’t worry, he’ll __________ after this failure.",
        lambda: "The brand will __________ next quarter.",
        lambda: "Athletes can __________ from injuries.",
        lambda: "Small caps may __________ in H2.",
        lambda: "Tourism tends to __________ in spring.",
        lambda: "We expect stocks to __________ soon.",
    ]),
    "safe_landing": make_item("a safe landing", "soft/safe outcome", [
        lambda: "Luckily, the project had __________.",
        lambda: "We managed __________ despite the risks.",
        lambda: "Policy changes ensured __________.",
        lambda: "Hedging gave us __________.",
        lambda: "Careful planning led to __________.",
        lambda: "Diversification helped achieve __________.",
    ]),
    "turbulence": make_item("turbulence", "instability / volatility", [
        lambda: "The economy experienced some __________ last year.",
        lambda: "Markets faced heavy __________ in May.",
        lambda: "Expect __________ during the transition.",
        lambda: "There was __________ after the announcement.",
        lambda: "We’re entering a phase of __________.",
        lambda: "Political news created __________.",
    ]),
    "take_off": make_item("take off", "begin to grow fast", [
        lambda: "Our business really started to __________ last month.",
        lambda: "The new feature helped the product __________.",
        lambda: "Her career began to __________ after the award.",
        lambda: "Subscriptions will __________ with ads.",
        lambda: "The channel will __________ after shorts.",
        lambda: "The brand is ready to __________ this season.",
    ]),
    "plunged": make_item("plunged", "dropped sharply", [
        lambda: "Profits __________ by 40% this year.",
        lambda: "The stock __________ at the open.",
        lambda: "Revenue __________ after churn rose.",
        lambda: "User time __________ post-update.",
        lambda: "Confidence __________ overnight.",
        lambda: "The index __________ on Monday.",
    ]),
    "a_flood": make_item("a flood", "a very large number", [
        lambda: "We had __________ of applications for the job.",
        lambda: "There was __________ of support from users.",
        lambda: "They received __________ of complaints.",
        lambda: "We saw __________ of preorders.",
        lambda: "The inbox got __________ of messages.",
        lambda: "PR got __________ of press requests.",
    ]),
    "flying_start": make_item("got off to a flying start", "begin very successfully", [
        lambda: "The project __________ and was an instant success.",
        lambda: "Her campaign __________ in the first week.",
        lambda: "The show __________ with record ratings.",
        lambda: "The venture __________ thanks to influencers.",
        lambda: "Negotiations __________ after the intro call.",
        lambda: "Sales __________ this quarter.",
    ]),
    "soar": make_item("soar", "rise quickly to a high level", [
        lambda: "The company’s shares continue to __________.",
        lambda: "Premium demand will __________ in Q4.",
        lambda: "Engagement tends to __________ with giveaways.",
        lambda: "Profits may __________ as costs fall.",
        lambda: "Expect conversion to __________ after redesign.",
        lambda: "Flight bookings will __________ in summer.",
    ]),
    "buoyant": make_item("buoyant", "upbeat/strong (market/sentiment)", [
        lambda: "The market is very __________ right now.",
        lambda: "Investor sentiment remains __________.",
        lambda: "Demand for EVs is __________.",
        lambda: "The mood stays __________ despite risks.",
        lambda: "Hiring remains __________ in tech.",
        lambda: "Exports look __________ this year.",
    ]),
    "nosedive": make_item("taken a nosedive", "fallen dramatically", [
        lambda: "The stock prices have __________ recently.",
        lambda: "Confidence has __________ since the scandal.",
        lambda: "User growth has __________ after changes.",
        lambda: "Ad revenue has __________ this quarter.",
        lambda: "Attendance has __________ lately.",
        lambda: "The currency has __________ again.",
    ]),
    "doldrums": make_item("in the doldrums", "stagnant / sluggish", [
        lambda: "The economy is still __________.",
        lambda: "PC sales remain __________.",
        lambda: "Housing is __________ for months.",
        lambda: "The team felt __________ before the win.",
        lambda: "Startups are __________ amid rates.",
        lambda: "Crypto is __________ this season.",
    ]),
    "kick_start": make_item("give it a kick start", "boost to restart", [
        lambda: "We need to __________ the new campaign.",
        lambda: "A discount will __________ sales.",
        lambda: "Influencers could __________ growth.",
        lambda: "Let’s __________ the project with a sprint.",
        lambda: "Ads should __________ demand.",
        lambda: "PR will __________ awareness.",
    ]),
    "long_shot": make_item("a long shot", "unlikely to succeed", [
        lambda: "It’s __________, but it might work.",
        lambda: "Landing that client is __________.",
        lambda: "Winning now is __________ at best.",
        lambda: "Beating the record is __________.",
        lambda: "Raising now is __________ in this market.",
        lambda: "This hypothesis is __________.",
    ]),
    "jumped_gun": make_item("jumped the gun", "acted too soon", [
        lambda: "They __________ by announcing the deal too early.",
        lambda: "We __________ with the press release.",
        lambda: "The team __________ before QA finished.",
        lambda: "She __________ by hiring first.",
        lambda: "He __________ posting results.",
        lambda: "Marketing __________ with the teaser.",
    ]),
    "ball_in_your_court": make_item("the ball is in your court", "your turn to act", [
        lambda: "I’ve done my part — now __________.",
        lambda: "We sent the offer; __________.",
        lambda: "Over to you — __________.",
        lambda: "We replied; __________ to accept or not.",
        lambda: "I gave the report; __________.",
        lambda: "Your move — __________.",
    ]),
    "bail_out": make_item("bail out", "rescue with money", [
        lambda: "The government had to __________ the bank.",
        lambda: "Taxpayers won’t __________ failing firms again.",
        lambda: "They asked the parent company to __________ them.",
        lambda: "Will the fund __________ the startup?",
        lambda: "Lenders agreed to __________ the airline.",
        lambda: "Investors refused to __________ the project.",
    ]),
    "drop_in_ocean": make_item("a drop in the ocean", "very small amount", [
        lambda: "That amount is just __________ compared to what we need.",
        lambda: "Ten volunteers are __________ for this event.",
        lambda: "One scholarship is __________ given demand.",
        lambda: "This budget is __________ for global rollout.",
        lambda: "Those savings are __________ against our debt.",
        lambda: "These fines are __________ for the giant.",
    ]),
    "cold_water_on": make_item("threw cold water on", "discouraged/criticised", [
        lambda: "The critics __________ the new proposal.",
        lambda: "Legal __________ our timeline.",
        lambda: "Finance __________ the expansion plan.",
        lambda: "Security concerns __________ the idea.",
        lambda: "The board __________ our optimism.",
        lambda: "Early feedback __________ the concept.",
    ]),
    "rally_troops": make_item("rally the troops", "motivate/assemble the team", [
        lambda: "We need to __________ to finish this project.",
        lambda: "The coach tried to __________ before the final.",
        lambda: "Let’s __________ for the last sprint.",
        lambda: "Leaders must __________ during crises.",
        lambda: "We’ll __________ for the big release.",
        lambda: "Time to __________ and push together.",
    ]),
}

IDIOMS_4 = {
    "ballpark": make_item("a ballpark figure", "rough estimate", [
        lambda: "Give me __________, not an exact number.",
        lambda: "What’s __________ for the total cost?",
        lambda: "Can you provide __________ for headcount?",
        lambda: "Just __________ will do for now.",
        lambda: "We need __________ for the brief.",
        lambda: "Any __________ is fine at this stage.",
    ]),
    "ironed_out": make_item("ironed out", "resolved differences", [
        lambda: "We finally __________ the differences in the contract.",
        lambda: "The teams __________ most issues.",
        lambda: "They __________ the bugs before launch.",
        lambda: "We __________ the details yesterday.",
        lambda: "Legal and sales __________ the conflicts.",
        lambda: "They __________ the remaining problems.",
    ]),
    "heads_will_roll": make_item("heads will roll", "people will be punished/fired", [
        lambda: "If this fails, __________ will.",
        lambda: "When the audit ends, __________.",
        lambda: "If the leak continues, __________.",
        lambda: "If KPIs aren’t met, __________.",
        lambda: "Mess this up and __________.",
        lambda: "When the boss returns, __________.",
    ]),
    "brings_bacon": make_item("brings home the bacon", "earns the money", [
        lambda: "He works hard and really __________.",
        lambda: "She __________ for the whole family.",
        lambda: "That product __________ for the company.",
        lambda: "Our services __________ these days.",
        lambda: "He’s the one who __________ here.",
        lambda: "This client __________ for us.",
    ]),
    "hotcakes": make_item("selling like hotcakes", "selling very fast", [
        lambda: "The new phone is __________ in stores.",
        lambda: "Those sneakers are __________ online.",
        lambda: "Tickets are __________ this morning.",
        lambda: "The limited edition is __________.",
        lambda: "Her merch is __________ already.",
        lambda: "Subscriptions are __________ today.",
    ]),
    "throwing_money": make_item("throwing money at", "spending without fixing root cause", [
        lambda: "They are just __________ the problem instead of solving it.",
        lambda: "Stop __________ marketing; fix the product.",
        lambda: "We’re __________ ads without strategy.",
        lambda: "Management keeps __________ symptoms.",
        lambda: "Investors are __________ growth issues.",
        lambda: "He thinks __________ everything helps.",
    ]),
    "cut_corners": make_item("cut corners", "save time/money by lowering quality", [
        lambda: "We had to __________ to save costs.",
        lambda: "Some builders __________ on safety.",
        lambda: "Don’t __________ with security.",
        lambda: "They __________ and shipped buggy code.",
        lambda: "Never __________ on QA.",
        lambda: "The vendor __________ to meet the deadline.",
    ]),
    "strike_while": make_item("strike while the iron is hot", "seize opportunity immediately", [
        lambda: "Let’s __________ and launch it now!",
        lambda: "We should __________ before rivals react.",
        lambda: "Marketing wants to __________ today.",
        lambda: "Invest now — __________.",
        lambda: "We must __________ after this hype.",
        lambda: "Time to __________ and close the deal.",
    ]),
    "hand_to_mouth": make_item("living from hand to mouth", "barely surviving, no savings", [
        lambda: "He’s been __________ since losing his job.",
        lambda: "Many artists are __________ these days.",
        lambda: "Families are __________ after layoffs.",
        lambda: "They’re __________ on minimum wage.",
        lambda: "Students are __________ till summer.",
        lambda: "Refugees are __________ for months.",
    ]),
    "sticky_fingers": make_item("sticky fingers", "tendency to steal", [
        lambda: "The cashier had __________ — he was stealing.",
        lambda: "Beware of staff with __________.",
        lambda: "The intern showed __________ at the store.",
        lambda: "Someone here has __________.",
        lambda: "They fired him for __________.",
        lambda: "Audit revealed __________ in accounting.",
    ]),
    "arm_leg": make_item("pay an arm and a leg", "very expensive", [
        lambda: "That watch will __________ you.",
        lambda: "We had to __________ for the seats.",
        lambda: "You’ll __________ for that repair.",
        lambda: "They’ll __________ for this view.",
        lambda: "Expect to __________ in that city.",
        lambda: "He had to __________ for tuition.",
    ]),
    "tighten_belts": make_item("tighten our belts", "reduce spending", [
        lambda: "We need to __________ because of inflation.",
        lambda: "After Q1 losses, we must __________.",
        lambda: "Households will __________ this year.",
        lambda: "Let’s __________ until cash improves.",
        lambda: "Time to __________ and cut extras.",
        lambda: "We’ll __________ over winter.",
    ]),
}

IDIOMS_TOPICS = {"Idioms 1": IDIOMS_1, "Idioms 2": IDIOMS_2, "Idioms 3": IDIOMS_3, "Idioms 4": IDIOMS_4}

# =========================
# Vocabulary Data (answers + meaning; 2–4 генератора на термин)
# =========================

# Vocab 1
VOCAB_1 = {
    "rewarding": make_item("rewarding", "giving satisfaction / fulfilling", [
        lambda: "I love my job because it’s really __________ – it gives me satisfaction and purpose.",
        lambda: "Teaching can be very __________ for those who like helping others.",
        lambda: "Volunteering felt truly __________ last summer.",
    ]),
    "stimulating": make_item("stimulating", "exciting and motivating; mentally engaging", [
        lambda: "The new project was so __________ that everyone felt motivated.",
        lambda: "His lectures are __________ and thought-provoking.",
        lambda: "A __________ environment keeps the team creative.",
    ]),
    "originality and creativity": make_item("originality and creativity", "fresh, inventive thinking", [
        lambda: "The design shows real __________ and stands out from the competition.",
        lambda: "We hire for __________ as well as technical skills.",
    ]),
    "no two days are the same": make_item("no two days are the same", "every day is different", [
        lambda: "I enjoy this job because __________ — every day is different.",
        lambda: "Journalism is great: __________ in the field.",
    ]),
    "client contact": make_item("client contact", "working directly with customers", [
        lambda: "In sales you get a lot of __________ with people.",
        lambda: "She enjoys daily __________ in her role.",
    ]),
    "hands-on": make_item("hands-on", "practical, directly involved", [
        lambda: "Our boss prefers a __________ approach and works with the team.",
        lambda: "It’s a very __________ role with real lab work.",
    ]),
    "hit it off with": make_item("hit it off with", "quickly become friendly with", [
        lambda: "When I started, I immediately __________ my new colleagues.",
        lambda: "They __________ the client on the first call.",
    ]),
    "get on well with": make_item("get on well with", "have a good relationship with", [
        lambda: "I really __________ my boss and team.",
        lambda: "Do you __________ your new manager?",
    ]),
    "working on my own": make_item("working on my own", "doing tasks independently", [
        lambda: "Sometimes I prefer __________ without distractions.",
        lambda: "He’s productive when __________.",
    ]),
    "teamwork": make_item("teamwork", "collaborating effectively with others", [
        lambda: "Good __________ is essential for any successful project.",
        lambda: "We value __________ more than individual heroics.",
    ]),
    "sense of achievement": make_item("sense of achievement", "feeling of accomplishment", [
        lambda: "Finishing the project gave me a real __________.",
        lambda: "Set small goals to keep a steady __________.",
    ]),
    "chained to a desk": make_item("chained to a desk", "stuck at a desk, sedentary work", [
        lambda: "He hates feeling __________ all day.",
        lambda: "I don’t want to be __________ from nine to five.",
    ]),
    "admin and paperwork": make_item("admin and paperwork", "bureaucratic/clerical tasks", [
        lambda: "I waste too much time doing __________ instead of creative work.",
        lambda: "Let’s automate routine __________.",
    ]),
    "snowed under": make_item("snowed under", "overloaded with work", [
        lambda: "I’m totally __________ with tasks this week.",
        lambda: "We were __________ after the product launch.",
    ]),
    "bureaucracy or red tape": make_item("bureaucracy or red tape", "excessive rules/procedures", [
        lambda: "The deal was delayed because of __________.",
        lambda: "We need to cut __________ in procurement.",
    ]),
    "perks": make_item("perks", "benefits/fringe advantages", [
        lambda: "Free lunches are one of the job __________.",
        lambda: "Gym membership is a great __________ here.",
    ]),
    "flexibility": make_item("flexibility", "ability to adjust schedule/location", [
        lambda: "I like the __________ this job offers — I can choose my hours.",
        lambda: "Remote work adds __________ for parents.",
    ]),
    "breathing down my neck": make_item("breathing down my neck", "over-controlling, watching too closely", [
        lambda: "I can’t work with my manager constantly __________.",
        lambda: "Stop __________ and let me finish the task.",
    ]),
    "commute": make_item("commute", "travel to work", [
        lambda: "Many people spend hours every day to __________ from the suburbs.",
        lambda: "I changed jobs to shorten my __________.",
    ]),
    "telecommute": make_item("telecommute", "work remotely", [
        lambda: "Since the pandemic, many employees started to __________ from home.",
        lambda: "Two days a week we __________ to reduce travel.",
    ]),
}

# Vocab 2
VOCAB_2 = {}
for term, meaning in [
    ("hard and soft skills", "the combined set of technical and interpersonal abilities"),
    ("hard skills", "technical, measurable abilities (e.g., Excel, coding)"),
    ("soft skills", "interpersonal skills (communication, teamwork)"),
    ("emotional intelligence", "ability to recognize, understand, manage emotions"),
    ("self-awareness", "understanding your own emotions and limits"),
    ("self-regulation", "controlling impulses and emotions"),
    ("motivation", "inner drive to achieve goals"),
    ("empathy", "recognizing and sharing others’ feelings"),
    ("social skills", "skills for interacting effectively"),
    ("optimism", "habit of expecting positive outcomes"),
    ("persuasion", "ability to convince others"),
    ("cooperation", "working together towards a goal"),
    ("dispute resolution", "settling conflicts constructively"),
    ("emotional intelligence 2", "a deeper EI model with drivers/constrainers/enablers"),
    ("drivers", "traits pushing performance forward"),
    ("decisiveness", "ability to make timely decisions"),
    ("constrainers", "traits that limit or hold back performance"),
    ("conscientiousness", "being diligent and responsible"),
    ("integrity", "honesty and strong moral principles"),
    ("enablers", "traits that facilitate performance"),
    ("sensitivity", "awareness of others’ feelings and context"),
    ("influence", "ability to affect others’ actions or opinions"),
]:
    VOCAB_2[term] = make_item(term, meaning)

# Vocab 3
VOCAB_3 = {}
for term, meaning in [
    ("counselor", "a trained advisor/therapist"),
    ("factor", "an element contributing to a result"),
    ("symptom", "a sign/indicator of a problem"),
    ("management", "the act of directing and controlling work"),
    ("industry", "a sector of economic activity"),
    ("stress", "pressure or strain on the mind/body"),
    ("burnout", "exhaustion from prolonged stress"),
    ("work-life balance", "healthy balance of job and personal life"),
    ("heavy workload", "too much work to handle comfortably"),
    ("office politics", "power dynamics and informal influence at work"),
    ("role ambiguity", "unclear job expectations/responsibilities"),
    ("lack of management support", "insufficient help from leaders"),
    ("effort-reward imbalance", "work effort not matched by rewards"),
    ("home-work imbalance", "home demands conflict with work"),
    ("workaholics", "people who work excessively/compulsively"),
    ("quality of life", "overall well-being and life satisfaction"),
    ("downshifting", "choosing a simpler, less demanding lifestyle"),
    ("independence", "ability to act without undue control"),
    ("isolated", "feeling separated from others"),
]:
    VOCAB_3[term] = make_item(term, meaning)

# Vocab 4
VOCAB_4 = {}
for term, meaning in [
    ("hierarchy", "levels of authority in an organization"),
    ("roles of men and women", "gender roles in work/society"),
    ("glass ceiling", "invisible barrier to advancement (often for women)"),
    ("deference", "respectful submission to another’s authority"),
    ("formal", "following established, official style/etiquette"),
    ("turn-taking", "orderly exchange in conversation"),
    ("gestures", "hand/body movements conveying meaning"),
    ("body language", "nonverbal communication with posture/gestures"),
    ("task-oriented", "focused on tasks and results"),
    ("relationship-oriented", "focused on people and rapport"),
    ("planning", "deciding actions in advance"),
    ("punctuality", "being on time"),
    ("hospitality", "warm, friendly reception of guests"),
    ("follows procedure", "adheres strictly to rules/process"),
    ("deferential, respectful of authority", "shows respect to higher status"),
    ("understandable to non-native speakers", "clear and simple for learners"),
    ("multitasker", "person who handles multiple tasks at once"),
    ("work-life balance", "balance between work and personal life"),
    ("sociable", "friendly; enjoys company of others"),
    ("congenial", "pleasant and agreeable"),
    ("direct, sincere", "straightforward and honest"),
    ("efficient", "productive with minimal waste"),
    ("flexible", "adaptable to change"),
    ("proactive", "takes initiative in advance"),
    ("modest", "humble; not boastful"),
    ("not independent", "relies on others; lacks autonomy"),
    ("bureaucratic", "overly procedural and rule-bound"),
    ("rigid", "inflexible; not open to change"),
    ("kowtows to authority", "overly submissive to superiors"),
    ("doesn’t concentrate", "lacks focus"),
    ("easily distracted", "attention is easily diverted"),
    ("lazy", "unwilling to work hard"),
    ("time-waster, over-familiar", "wastes time; too casual"),
    ("tactless", "insensitive; lacks diplomacy"),
    ("rude", "impolite; bad manners"),
    ("acerbic", "sharp, harsh in tone"),
    ("improviser", "relies on spontaneous solutions"),
    ("undisciplined", "lacks self-control or order"),
    ("disorganized", "poorly structured; messy"),
    ("distracted", "unable to maintain focus"),
    ("uncommunicative", "does not share information"),
]:
    VOCAB_4[term] = make_item(term, meaning)

# Vocab 5 (Business)
VOCAB_5 = {}
for term, meaning in [
    ("pitch", "short persuasive presentation of an idea"),
    ("offer", "proposal with terms"),
    ("counter-offer", "revised proposal responding to an offer"),
    ("equity", "ownership stake in a company"),
    ("wholesale price", "price to distributors/retailers"),
    ("retail price", "price to end consumers"),
    ("overhead", "ongoing fixed operating costs"),
    ("scalability", "ability to grow efficiently"),
    ("gross sales", "total sales before deductions"),
    ("net sales", "sales after returns/discounts"),
    ("revenue", "income from business activities"),
    ("margin", "profit as a share of sales"),
    ("scam", "fraudulent scheme"),
    ("royalties", "payments for licensed IP usage"),
    ("landed cost", "total cost incl. shipping, duty, fees"),
    ("skin in the game", "personal financial stake/risk"),
    ("to go viral", "spread quickly online"),
    ("to make a play", "act strategically to gain advantage"),
    ("valuation", "estimated worth of a company"),
]:
    VOCAB_5[term] = make_item(term, meaning)

VOCAB_TOPICS = {
    "Vocab 1": VOCAB_1,
    "Vocab 2": VOCAB_2,
    "Vocab 3": VOCAB_3,
    "Vocab 4": VOCAB_4,
    "Vocab 5": VOCAB_5,
}

# =========================
# App State
# =========================
if "mode" not in st.session_state: st.session_state.mode = "Idioms"
if "topic" not in st.session_state: st.session_state.topic = "Idioms 1"
if "score" not in st.session_state: st.session_state.score = 0
if "streak" not in st.session_state: st.session_state.streak = 0
if "q_count" not in st.session_state: st.session_state.q_count = 0
if "locked" not in st.session_state: st.session_state.locked = False
if "cur_key" not in st.session_state: st.session_state.cur_key = None
if "cur_ans" not in st.session_state: st.session_state.cur_ans = ""
if "cur_prompt" not in st.session_state: st.session_state.cur_prompt = ""
if "feedback" not in st.session_state: st.session_state.feedback = ""
if "stats" not in st.session_state: st.session_state.stats = {}  # key -> {"a":attempts,"c":correct}
if "play_click" not in st.session_state: st.session_state.play_click = False
if "show_full_ref" not in st.session_state: st.session_state.show_full_ref = False
if "full_ref_scope" not in st.session_state: st.session_state.full_ref_scope = "Topic only"

MAX_Q = 10

# =========================
# Sidebar (Cheat Sheet, blur toggle, ambience)
# =========================
with st.sidebar:
    st.header("📒 Cheat sheet")
    st.session_state.mode = st.selectbox("Mode", ["Idioms", "Vocabulary"], index=0 if st.session_state.mode=="Idioms" else 1)
    # Topic list depends on mode
    if st.session_state.mode == "Idioms":
        topic_list = ["Idioms 1","Idioms 2","Idioms 3","Idioms 4","Mixed"]
    else:
        topic_list = ["Vocab 1","Vocab 2","Vocab 3","Vocab 4","Vocab 5","Mixed"]
    st.session_state.topic = st.selectbox("Topic", topic_list, index=topic_list.index(st.session_state.topic) if st.session_state.topic in topic_list else 0)

    ambience_on = st.toggle("🎧 Typing ambience", value=False)
    blur_on = st.toggle("Blur cheat sheet", value=True)

    # Build pool for cheat sheet view
    if st.session_state.mode == "Idioms":
        if st.session_state.topic == "Mixed":
            pool_view = {}
            for d in IDIOMS_TOPICS.values(): pool_view.update(d)
        else:
            pool_view = IDIOMS_TOPICS[st.session_state.topic]
    else:
        if st.session_state.topic == "Mixed":
            pool_view = {}
            for d in VOCAB_TOPICS.values(): pool_view.update(d)
        else:
            pool_view = VOCAB_TOPICS[st.session_state.topic]

    # init stats entries for visible pool
    for k in pool_view.keys():
        st.session_state.stats.setdefault(k, {"a":0,"c":0})

    # render table
    rows = []
    for k, item in pool_view.items():
        a = item["answer"]; m = item["meaning"]
        s = st.session_state.stats.get(k, {"a":0,"c":0})
        pct = int(round(100*s["c"]/s["a"])) if s["a"] else 0
        rows.append((a, m, f"{pct}%"))

    table_html = ["<div class='cheat-wrap'><div class='cheat {}'>".format("cheat-blur" if blur_on else "")]
    table_html.append("<table>")
    table_html.append("<tr><th>Term</th><th>Meaning</th><th style='text-align:right'>Accuracy</th></tr>")
    for a,m,p in rows:
        table_html.append(f"<tr><td>{a}</td><td>{m}</td><td class='acc'>{p}</td></tr>")
    table_html.append("</table></div></div>")
    st.markdown("\n".join(table_html), unsafe_allow_html=True)

    # Full reference toggle opens big panel on the right
    st.session_state.show_full_ref = st.toggle("🔎 Open full reference (right/full)", value=st.session_state.show_full_ref)
    if st.session_state.mode == "Idioms":
        ref_scope = st.selectbox("Reference scope", ["Topic only","All Idioms"], index=0 if st.session_state.full_ref_scope=="Topic only" else 1)
    else:
        ref_scope = st.selectbox("Reference scope", ["Topic only","All Vocab"], index=0 if st.session_state.full_ref_scope=="Topic only" else 1)
    st.session_state.full_ref_scope = ref_scope

if ambience_on:
    st.markdown(audio_loop(AMBIENCE_B64), unsafe_allow_html=True)

# =========================
# Build question pool based on mode/topic
# =========================
def get_pool(mode, topic):
    if mode == "Idioms":
        if topic == "Mixed":
            p = {}
            for d in IDIOMS_TOPICS.values(): p.update(d)
            return p
        else:
            return IDIOMS_TOPICS[topic]
    else:
        if topic == "Mixed":
            p = {}
            for d in VOCAB_TOPICS.values(): p.update(d)
            return p
        else:
            return VOCAB_TOPICS[topic]

pool = get_pool(st.session_state.mode, st.session_state.topic)

# =========================
# Question lifecycle
# =========================
def new_question(avoid_key=None, avoid_prompt=None):
    keys = list(pool.keys())
    if avoid_key and len(keys) > 1:
        keys = [k for k in keys if k != avoid_key]
    key = random.choice(keys)
    ans = pool[key]["answer"]
    prompt = pool[key]["gen"]()
    if avoid_prompt:
        for _ in range(5):
            if prompt != avoid_prompt: break
            prompt = pool[key]["gen"]()
    st.session_state.cur_key = key
    st.session_state.cur_ans = ans
    st.session_state.cur_prompt = prompt

# reset current question if topic/mode changed
if st.session_state.cur_key is None or st.session_state.topic not in (["Idioms 1","Idioms 2","Idioms 3","Idioms 4","Mixed","Vocab 1","Vocab 2","Vocab 3","Vocab 4","Vocab 5"]):
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.q_count = 0
    st.session_state.locked = False
    st.session_state.feedback = ""
    st.session_state.cur_key = None

if st.session_state.cur_key is None:
    new_question()

# =========================
# Header / Progress
# =========================
left, right = st.columns([2,1])
with left:
    st.title("🎓 Exam Trainer (Idioms + Vocabulary)")
    cols = st.columns([1,1,1,1])
    with cols[0]:
        st.markdown(f"<span class='score-badge'>Score: {st.session_state.score}</span>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"<span class='score-badge'>Streak: {st.session_state.streak}</span>", unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"<span class='score-badge'>Q: {min(st.session_state.q_count+1, MAX_Q)} / {MAX_Q}</span>", unsafe_allow_html=True)
    with cols[3]:
        if st.button("🔁 Restart"):
            st.session_state.play_click = True
            for k in ["score","streak","q_count","locked","cur_key","cur_ans","cur_prompt","feedback"]:
                st.session_state.pop(k, None)
            st.rerun()

    st.progress(st.session_state.q_count / MAX_Q)

    # Card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='prompt'>✍️ {st.session_state.cur_prompt}</div>", unsafe_allow_html=True)
    user = st.text_input("Your answer:")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("✅ Check", disabled=st.session_state.locked or st.session_state.q_count>=MAX_Q):
            st.session_state.play_click = True
            correct = norm(user) == norm(st.session_state.cur_ans)
            st.session_state.locked = True

            # update per-item stats
            s = st.session_state.stats.setdefault(st.session_state.cur_key, {"a":0,"c":0})
            s["a"] += 1
            if correct: s["c"] += 1

            if correct:
                st.session_state.streak += 1
                st.session_state.score += 25
                bonus_msg = ""
                if st.session_state.streak % 3 == 0:
                    st.session_state.score += 50
                    bonus_msg = " (+50 streak bonus)"
                st.session_state.feedback = f"✅ Correct! +25{bonus_msg}"
            else:
                st.session_state.streak = 0
                st.session_state.score -= 25
                st.session_state.feedback = f"❌ Wrong. Right answer: **{st.session_state.cur_ans}**  (−25)"

    with c2:
        if st.button("➡️ Next", disabled=not st.session_state.locked or st.session_state.q_count>=MAX_Q):
            st.session_state.play_click = True
            st.session_state.q_count += 1
            st.session_state.locked = False
            st.session_state.feedback = ""
            prev_key = st.session_state.cur_key
            prev_prompt = st.session_state.cur_prompt
            new_question(avoid_key=prev_key, avoid_prompt=prev_prompt)
            st.rerun()

    with c3:
        if st.button("↻ Rephrase", disabled=st.session_state.locked or st.session_state.q_count>=MAX_Q,
                     help="Другая формулировка того же термина"):
            st.session_state.play_click = True
            prev_prompt = st.session_state.cur_prompt
            # новая формулировка той же идиомы/термина
            prompt = pool[st.session_state.cur_key]["gen"]()
            for _ in range(5):
                if prompt != prev_prompt: break
                prompt = pool[st.session_state.cur_key]["gen"]()
            st.session_state.cur_prompt = prompt
            st.rerun()

    st.markdown(f"<div class='feedback'>{st.session_state.feedback}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Finish screen
    if st.session_state.q_count >= MAX_Q:
        st.success("🏁 Done! Результаты ниже.")
        rough = int(max(0, min(100, round(st.session_state.score / (25*MAX_Q) * 100))))
        st.write(f"**Final score:** {st.session_state.score}")
        st.write(f"**Accuracy (rough):** {rough}%")
        if st.button("Play again"):
            st.session_state.play_click = True
            for k in ["score","streak","q_count","locked","cur_key","cur_ans","cur_prompt","feedback"]:
                st.session_state.pop(k, None)
            st.rerun()

with right:
    # Full reference panel on the right; can expand to full width below
    if st.session_state.show_full_ref:
        # Build reference data
        if st.session_state.mode == "Idioms":
            if st.session_state.full_ref_scope == "All Idioms":
                ref_pool = {}
                for d in IDIOMS_TOPICS.values(): ref_pool.update(d)
            else:
                ref_pool = get_pool("Idioms", st.session_state.topic if st.session_state.topic!="Mixed" else "Idioms 1")
        else:
            if st.session_state.full_ref_scope == "All Vocab":
                ref_pool = {}
                for d in VOCAB_TOPICS.values(): ref_pool.update(d)
            else:
                ref_pool = get_pool("Vocabulary", st.session_state.topic if st.session_state.topic!="Mixed" else "Vocab 1")

        rows = []
        for k, item in ref_pool.items():
            a = item["answer"]; m = item["meaning"]
            s = st.session_state.stats.get(k, {"a":0,"c":0})
            pct = int(round(100*s["c"]/s["a"])) if s["a"] else 0
            rows.append((a, m, f"{pct}%"))

        html = ["<div class='fullref'><table>"]
        html.append("<tr><th>Term</th><th>Meaning</th><th style='text-align:right'>Accuracy</th></tr>")
        for a,m,p in rows:
            html.append(f"<tr><td>{a}</td><td>{m}</td><td class='acc'>{p}</td></tr>")
        html.append("</table></div>")
        st.markdown("\n".join(html), unsafe_allow_html=True)

# Play click sound if requested
if st.session_state.play_click:
    st.markdown(audio_once(CLICK_B64), unsafe_allow_html=True)
    st.session_state.play_click = False
