import streamlit as st
import streamlit.components.v1 as components
import json
import os
import random
from reading_db import STORIES

# ══════════════════════════════════════════════════════════════
# 1. CONFIG & SESSION STATE
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Oxford Flashcards",
    page_icon="📇",
    layout="centered"
)

DEFAULTS = {
    "user_level": "Level 1: Beginner (A1–A2)",
    "flash_mode": "study",
    "study_idx":  0,
    "card_idx":   0,
    "flash_score": 0,
    "flash_status": None,
    "cards": [],
    
    "read_story_idx": 0,
    "read_q_idx": 0,
    "read_score": 0,
    "read_status": None,   # None | "correct" | "wrong"
    "read_mode": "read",   # "read" | "quiz"
    "read_answers": {},    # {q_idx: chosen_option}
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════
# 2. LOAD OXFORD DB
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_db() -> dict:
    path = os.path.join(os.path.dirname(__file__), "oxford_db_enriched.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

DB = load_db()
DB_OK = bool(DB)

def get_pool(level_label: str) -> list[dict]:
    if "A1" in level_label:
        return DB.get("A1", []) + DB.get("A2", [])
    elif "B1" in level_label:
        return DB.get("B1", []) + DB.get("B2", [])
    else:
        return DB.get("C1", []) + DB.get("C2", [])

def pick_cards(level_label: str, n: int = 10) -> list[dict]:
    """สุ่ม n คำจาก pool แล้วสร้าง card objects พร้อมใช้งาน"""
    pool = get_pool(level_label)
    if not pool:
        return []
    sample = random.sample(pool, min(n, len(pool)))
    cards = []
    for w in sample:
        thai = w.get("thai", "").strip()
        definition = w.get("definition", "").strip()
        example = w.get("example", "").strip()

        # Fallback ถ้าข้อมูลยังว่าง (ก่อนรัน enrich script)
        if not thai or thai == "":
            thai = f"(ยังไม่มีคำแปล — รัน enrich_oxford_db.py)"
        if not definition or definition.startswith("Core vocabulary"):
            definition = f"{w['word'].capitalize()} ({w.get('pos','')}) — Oxford {w.get('source','5000')}"
        if not example:
            example = f"Please look up '{w['word']}' in a dictionary for example sentences."

        cards.append({
            "word":         w["word"],
            "pos":          w.get("pos", ""),
            "pronunciation": w.get("pronunciation", ""),
            "definition":   definition,
            "thai":         thai,
            "example":      example,
            "source":       w.get("source", "Oxford 5000"),
            "streak":       0,
            "mastered":     False,
        })
    return cards

# ══════════════════════════════════════════════════════════════
# 3. CSS — same warm parchment theme
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,400&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

:root {
    --ink:        #1E1810;
    --ink-muted:  #6B5E4A;
    --ink-faint:  #9E8E78;
    --parchment:  #F5F0E4;
    --page:       #FBF8F2;
    --page-warm:  #F8F3E8;
    --rule:       #DDD5C4;
    --rule-light: #EAE4D8;
    --amber:      #C8922A;
    --amber-light:#E8B855;
    --amber-bg:   #FDF4E0;
    --amber-deep: #9E6E18;
    --sepia-1:    #3A2E1E;
    --sepia-2:    #4A3C26;
    --correct-bg: #EFF7EE;
    --correct-bd: #A8C9A0;
    --correct-txt:#1C4A1E;
    --wrong-bg:   #FBF0EE;
    --wrong-bd:   #E0A8A0;
    --wrong-txt:  #5A1A18;
}

*, *::before, *::after { box-sizing: border-box; }

.stApp, html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMainBlockContainer"] {
    background-color: var(--parchment) !important;
    color: var(--ink) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem;
    padding-bottom: 5rem;
    max-width: 700px;
    position: relative;
}

/* Typography */
.app-title {
    font-family: 'Fraunces', serif;
    font-size: 2.2rem;
    color: var(--ink);
    font-weight: 600;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin-bottom: 0;
}
.app-sub {
    font-size: 0.75rem;
    color: var(--ink-faint);
    letter-spacing: 0.13em;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 2rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.title-bar {
    display: inline-block;
    width: 32px; height: 3px;
    background: var(--amber);
    border-radius: 2px;
    margin-bottom: 1rem;
}

/* Selectbox / inputs */
.stSelectbox [data-baseweb="select"] > div:first-child {
    border-radius: 10px !important;
    border-color: var(--rule) !important;
    background: var(--page) !important;
    color: var(--ink) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.875rem !important;
}
.stSelectbox label {
    color: var(--ink-muted) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important;
}
[data-baseweb="popover"] li, [role="option"] {
    background: var(--page) !important;
    color: var(--ink) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[role="option"]:hover { background: var(--amber-bg) !important; }

/* Buttons */
.stButton > button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    border-radius: 10px !important;
    border: 1.5px solid var(--rule) !important;
    background: var(--page) !important;
    color: var(--ink) !important;
    padding: 9px 18px !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
}
.stButton > button:hover {
    border-color: var(--amber) !important;
    background: var(--amber-bg) !important;
    color: var(--amber-deep) !important;
    transform: translateY(-1px) !important;
}

/* Mode pills */
.mode-row { display: flex; gap: 8px; margin-bottom: 1rem; }

/* Result boxes */
.result-correct {
    background: var(--correct-bg);
    border: 1px solid var(--correct-bd);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    color: var(--correct-txt);
    font-family: 'Source Serif 4', serif;
    font-size: 0.95rem;
    line-height: 1.65;
    margin-top: 0.5rem;
}
.result-wrong {
    background: var(--wrong-bg);
    border: 1px solid var(--wrong-bd);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    color: var(--wrong-txt);
    font-family: 'Source Serif 4', serif;
    font-size: 0.95rem;
    line-height: 1.65;
    margin-top: 0.5rem;
}

/* Quiz box */
.quiz-box {
    background: linear-gradient(135deg, #3A2E1E, #4A3C26);
    color: white;
    border-radius: 16px;
    padding: 2rem 1.75rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    margin-bottom: 1.25rem;
}
.quiz-word { font-family: 'Fraunces', serif; font-size: 2.4rem; color: #C8922A; letter-spacing: -0.02em; }
.quiz-pos  { font-size: 0.78rem; color: rgba(255,255,255,0.35); margin-top: 4px; font-family: 'Plus Jakarta Sans', sans-serif; }
.quiz-streak { font-size: 0.85rem; color: #f59e0b; margin-top: 8px; }

/* Progress */
.stProgress > div > div > div { background-color: var(--amber) !important; border-radius: 4px; }
.stProgress > div > div { background-color: var(--rule-light) !important; border-radius: 4px; }

/* Stats row */
.stat-chip {
    display: inline-block;
    background: var(--page-warm);
    border: 1px solid var(--rule-light);
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 0.78rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--ink-muted);
    margin-right: 6px;
}

/* Quiz answer buttons */
div[data-testid="stHorizontalBlock"] .stButton > button {
    text-align: left !important;
    font-weight: 400 !important;
    min-height: 52px !important;
    height: auto !important;
    font-family: 'Source Serif 4', serif !important;
    font-size: 0.9rem !important;
    line-height: 1.4 !important;
}

h4 {
    font-family: 'Fraunces', serif !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
    color: var(--ink) !important;
    font-size: 1.3rem !important;
}

p, span, div, label, li,
.stMarkdown,
[data-testid="stMarkdownContainer"] p {
    color: var(--ink);
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stCaption {
    color: var(--ink-faint) !important;
    font-size: 0.8rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stAlert {
    border-radius: 12px !important;
    border: none !important;
    font-size: 0.875rem !important;
    background: var(--page-warm) !important;
}

hr { border-color: var(--rule) !important; margin: 1.25rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 4. FLASHCARD HTML COMPONENT
# ══════════════════════════════════════════════════════════════
def render_flashcard(card: dict):
    oxford_tag = '<div style="position:absolute;top:12px;right:16px;font-size:0.58rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#E8B855;opacity:0.7;">Oxford 5000</div>'
    pos_tag = f'<div style="font-size:0.72rem;color:rgba(255,255,255,0.3);margin-top:4px;">{card.get("pos","")}</div>' if card.get("pos") else ""

    thai_val = card.get("thai", "")
    def_val  = card.get("definition", "")
    ex_val   = card.get("example", "")

    components.html(f"""<!DOCTYPE html>
<html>
<head>
<style>
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{background:transparent;font-family:sans-serif;padding:2px;}}
  .scene{{width:100%;height:220px;perspective:1200px;}}
  .card{{width:100%;height:100%;position:relative;transform-style:preserve-3d;
         transition:transform 0.55s cubic-bezier(0.4,0,0.2,1);border-radius:16px;cursor:pointer;}}
  .card.flipped{{transform:rotateY(180deg);}}
  .face{{position:absolute;inset:0;border-radius:16px;backface-visibility:hidden;
         -webkit-backface-visibility:hidden;display:flex;flex-direction:column;padding:1.75rem 2rem;}}
  .front{{background:linear-gradient(135deg,#3A2E1E,#4A3C26);color:white;
          box-shadow:0 8px 32px rgba(0,0,0,0.25);align-items:center;justify-content:center;text-align:center;}}
  .back{{background:#FBF8F2;border:1.5px solid #DDD5C4;transform:rotateY(180deg);
         align-items:flex-start;justify-content:flex-start;gap:8px;overflow-y:auto;}}
  .word{{font-size:2.4rem;color:#C8922A;letter-spacing:-0.02em;line-height:1.1;font-weight:700;}}
  .hint{{font-size:0.72rem;color:rgba(255,255,255,0.3);margin-top:10px;}}
  .lbl{{font-size:0.6rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#9E8E78;margin-bottom:2px;}}
  .val{{font-size:0.9rem;color:#1E1810;line-height:1.6;}}
  .sec{{margin-top:8px;width:100%;}}
  .flip-btn{{margin-top:10px;width:100%;padding:9px 0;border-radius:10px;
             border:1.5px solid #DDD5C4;background:#FBF8F2;color:#1E1810;
             font-size:0.875rem;font-weight:500;cursor:pointer;transition:all 0.15s;}}
  .flip-btn:hover{{border-color:#C8922A;background:#FDF4E0;color:#9E6E18;}}
</style>
</head>
<body>
<div class="scene">
  <div class="card" id="fc">
    <div class="face front">
      {oxford_tag}
      <div class="word">{card['word']}</div>
      {pos_tag}
      <div class="hint">แตะการ์ดหรือกดปุ่มเพื่อพลิกดูความหมาย</div>
    </div>
    <div class="face back">
      <div class="sec">
        <div class="lbl">ความหมายภาษาไทย</div>
        <div class="val" style="font-weight:600;font-size:1rem;">{thai_val}</div>
      </div>
      <div class="sec">
        <div class="lbl">Definition</div>
        <div class="val">{def_val}</div>
      </div>
      <div class="sec">
        <div class="lbl">Example</div>
        <div class="val" style="font-style:italic;color:#6B5E4A;">"{ex_val}"</div>
      </div>
    </div>
  </div>
</div>
<!-- <button class="flip-btn" onclick="flip()">🔄 พลิกการ์ด</button> -->
<script>
  const fc = document.getElementById('fc');
  fc.addEventListener('click', flip);
  function flip(){{ fc.classList.toggle('flipped'); }}
</script>
</body>
</html>""", height=290, scrolling=False)

# ══════════════════════════════════════════════════════════════
# 5. HEADER
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="title-bar"></div>', unsafe_allow_html=True)
st.markdown('<p class="app-title">Oxford Flashcards</p>', unsafe_allow_html=True)
st.markdown('<p class="app-sub">Offline · Oxford 5000 · </p>', unsafe_allow_html=True)

if not DB_OK:
    st.error("❌ ไม่พบ oxford_db.json — วางไฟล์ไว้ในโฟลเดอร์เดียวกับ flashcard_offline.py")
    st.stop()

# ══════════════════════════════════════════════════════════════
# 6. SETTINGS BAR
# ══════════════════════════════════════════════════════════════
LEVELS = [
    "Level 1: Beginner (A1–A2)",
    "Level 2: Intermediate (B1–B2)",
    "Level 3: Advanced (C1)",
]
col_lvl, col_n = st.columns([3, 1])
with col_lvl:
    level = st.selectbox(
        "ระดับภาษาอังกฤษ",
        LEVELS,
        index=LEVELS.index(st.session_state["user_level"]) if st.session_state["user_level"] in LEVELS else 0,
        key="level_sel"
    )
    if level != st.session_state["user_level"]:
        st.session_state["user_level"] = level
        st.session_state["cards"] = []
        st.rerun()

with col_n:
    n_cards = st.selectbox("จำนวนการ์ด", [5, 10, 15, 20], index=1, key="n_cards_sel")

pool = get_pool(st.session_state["user_level"])
st.caption(f"📦 Oxford DB พร้อมใช้ · ระดับนี้มี **{len(pool):,}** คำ")

# ══════════════════════════════════════════════════════════════
# 7. MODE SELECTOR + DRAW BUTTON
# ══════════════════════════════════════════════════════════════
col_m1, col_m2, col_draw = st.columns([2, 2, 2])
col_m3 = st.columns(1)[0]
with col_m1:
    if st.button("📖 โหมดเรียนรู้", use_container_width=True):
        st.session_state["flash_mode"] = "study"
        st.rerun()
with col_m2:
    if st.button("🎮 โหมดควิซ", use_container_width=True):
        st.session_state["flash_mode"] = "quiz"
        st.rerun()
with col_m3:
    if st.button("📚 อ่านเรื่องสั้น", use_container_width=True):
        st.session_state["flash_mode"] = "reading"
        st.rerun()
with col_draw:
    if st.button("🎲 สุ่มการ์ดใหม่", use_container_width=True, type="primary"):
        cards = pick_cards(st.session_state["user_level"], n_cards)
        st.session_state["cards"]        = cards
        st.session_state["study_idx"]    = 0
        st.session_state["card_idx"]     = 0
        st.session_state["flash_score"]  = 0
        st.session_state["flash_status"] = None
        if "current_options" in st.session_state:
            del st.session_state["current_options"]
        st.rerun()

st.markdown("---")

# ══════════════════════════════════════════════════════════════
# 8. MAIN CONTENT
# ══════════════════════════════════════════════════════════════
cards = st.session_state.get("cards", [])

if not cards:
    st.info("👆สุ่มการ์ดใหม่")
    st.stop()

mode = st.session_state["flash_mode"]

# ── STUDY MODE ────────────────────────────────────────────────
if mode == "study":
    st.markdown("#### 👀 ฝึกจำคำศัพท์")

    s_idx = st.session_state.get("study_idx", 0)
    if s_idx >= len(cards):
        s_idx = 0
        st.session_state["study_idx"] = 0

    card = cards[s_idx]

    # Flashcard HTML
    render_flashcard(card)

    # Nav
    st.markdown("<br>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b1:
        if st.button("⬅️ ก่อนหน้า", disabled=(s_idx == 0), use_container_width=True):
            st.session_state["study_idx"] = s_idx - 1
            st.rerun()
    with col_b2:
        st.markdown(
            f"<p style='text-align:center;font-size:0.82rem;color:#9E8E78;margin-top:10px;"
            f"font-family:sans-serif;'>ใบที่ {s_idx+1} / {len(cards)}</p>",
            unsafe_allow_html=True
        )
    with col_b3:
        if st.button("ถัดไป ➡️", disabled=(s_idx == len(cards)-1), use_container_width=True):
            st.session_state["study_idx"] = s_idx + 1
            st.rerun()

    st.markdown("---")
    st.info("💡 จำให้ครบก่อน แล้วกด **โหมดควิซ** เพื่อทดสอบตัวเอง")

# ── QUIZ MODE ─────────────────────────────────────────────────
elif mode == "quiz":
    st.markdown("#### 🎮 โหมดควิซ — เลือกคำแปลที่ถูกต้อง")

    # check all mastered
    unmastered = [c for c in cards if not c.get("mastered", False)]
    mastered_count = len(cards) - len(unmastered)

    # Progress
    col_prog, col_sco = st.columns([3, 1])
    with col_prog:
        st.markdown(
            f"<p style='font-size:0.82rem;color:#9E8E78;font-weight:500;margin-bottom:4px;"
            f"font-family:sans-serif;'>จำได้แม่นยำแล้ว {mastered_count} / {len(cards)} คำ</p>",
            unsafe_allow_html=True
        )
        st.progress(mastered_count / len(cards))
    with col_sco:
        st.markdown(
            f"<p style='text-align:right;font-weight:600;color:#C8922A;font-size:1rem;"
            f"margin-top:4px;font-family:sans-serif;'>🏆 {st.session_state['flash_score']} คะแนน</p>",
            unsafe_allow_html=True
        )

    # ── All mastered ──
    if not unmastered:
        st.balloons()
        st.markdown(f"""
        <div style="background:#EFF7EE;border-radius:16px;padding:2rem;text-align:center;
                    border:1px solid #A8C9A0;margin:1rem 0;">
            <h2 style="font-family:'Fraunces',serif;color:#1C4A1E;margin:0 0 0.5rem;font-size:1.75rem;">
                🏆 ยอดเยี่ยม! จำได้ครบเซ็ตแล้ว
            </h2>
            <p style="color:#1C4A1E;margin:0;font-size:1rem;font-family:sans-serif;">
                ผ่านเงื่อนไขตอบถูก 3 ครั้งติดต่อกันครบทั้ง {len(cards)} คำ!
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 เริ่มใหม่", use_container_width=True):
            for c in cards:
                c["streak"]   = 0
                c["mastered"] = False
            st.session_state.update({"card_idx":0,"flash_score":0,"flash_status":None})
            if "current_options" in st.session_state:
                del st.session_state["current_options"]
            st.rerun()
        st.stop()

    # ── Current card ──
    idx  = st.session_state.get("card_idx", 0)
    if idx >= len(cards):
        idx = 0
        st.session_state["card_idx"] = 0
    card = cards[idx]

    # Build options once
    if "current_options" not in st.session_state:
        correct = card.get("thai", "")
        # ใช้คำแปลจากการ์ดอื่นเป็นตัวลวง
        distractors = [
            c.get("thai", "—") for i, c in enumerate(cards)
            if i != idx and c.get("thai", "").strip()
               and not c["thai"].startswith("(ยังไม่มี")
        ]
        # ถ้าตัวลวงน้อยกว่า 3 ให้ดึงจาก pool ของ DB ตรงๆ
        if len(distractors) < 3:
            extra_pool = [
                w.get("thai","") for w in get_pool(st.session_state["user_level"])
                if w.get("thai","").strip() and w["word"] != card["word"]
            ]
            random.shuffle(extra_pool)
            distractors += extra_pool
        distractors = distractors[:3]
        opts = distractors + [correct]
        random.shuffle(opts)
        st.session_state["current_options"] = opts

    # Quiz card display
    streak = card.get("streak", 0)
    stars  = "⭐" * streak if streak > 0 else "🎯 พยายามเข้า"
    st.markdown(f"""
    <div class="quiz-box">
      <div class="quiz-word">{card['word']}</div>
      <div class="quiz-pos">{card.get('pos','')}</div>
      <div class="quiz-streak">🔥 ตอบถูกต่อเนื่อง: {stars} ({streak}/3)</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size:0.82rem;font-weight:600;color:#9E8E78;"
        "letter-spacing:0.05em;text-transform:uppercase;font-family:sans-serif;'>"
        "เลือกคำแปลที่ถูกต้อง</p>",
        unsafe_allow_html=True
    )

    options     = st.session_state["current_options"]
    user_choice = None
    locked      = st.session_state["flash_status"] is not None

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    for i, col in enumerate([col1, col2, col3, col4]):
        with col:
            if st.button(f"{i+1}. {options[i]}", key=f"opt_{idx}_{i}",
                         use_container_width=True, disabled=locked):
                user_choice = options[i]

    # ── Process answer ──
    if user_choice:
        correct_thai = card.get("thai", "")
        if user_choice == correct_thai:
            st.session_state["flash_status"] = "correct"
            st.session_state["flash_score"]  += 1
            card["streak"] += 1
            if card["streak"] >= 3:
                card["mastered"] = True
        else:
            st.session_state["flash_status"] = "wrong"
            card["streak"] = 0
        st.rerun()

    # ── Result feedback ──
    status = st.session_state["flash_status"]

    if status == "correct":
        st.markdown(f"""
        <div class="result-correct">
            🎉 <strong>ถูกต้อง!</strong> แปลว่า <strong>{card.get('thai','')}</strong><br>
            <span style="opacity:0.85;">{card['definition']}</span><br>
            <em style="opacity:0.7;">"{card.get('example','')}"</em>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("ข้อถัดไป ➡️", key="next_c", use_container_width=True):
            remains = [c for c in cards if not c.get("mastered", False)]
            if remains:
                st.session_state["card_idx"] = cards.index(random.choice(remains))
            st.session_state["flash_status"] = None
            if "current_options" in st.session_state:
                del st.session_state["current_options"]
            st.rerun()

    elif status == "wrong":
        st.markdown(f"""
        <div class="result-wrong">
            ❌ <strong>ยังไม่ถูก</strong> — คำตอบที่ถูกต้องคือ <strong>{card.get('thai','')}</strong><br>
            <span style="opacity:0.85;">{card['definition']}</span><br>
            <em style="opacity:0.7;">"{card.get('example','')}"</em>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("ข้ามไปข้อถัดไป ➡️", key="next_w", use_container_width=True):
            remains = [c for c in cards if not c.get("mastered", False)]
            if remains:
                st.session_state["card_idx"] = cards.index(random.choice(remains))
            st.session_state["flash_status"] = None
            if "current_options" in st.session_state:
                del st.session_state["current_options"]
            st.rerun()

# ══════════════════════════════════════════════════════════════
# FULL READING MODE CODE — วางต่อท้าย elif mode == "quiz": block
# ══════════════════════════════════════════════════════════════
 
# ── READING MODE ──────────────────────────────────────────────
elif mode == "reading":
    from reading_db import STORIES
 
    # ── Story selector ──────────────────────────────────────────
    st.markdown("#### 📚 ฝึกอ่านเรื่องสั้น")
 
    story_labels = [f"{s['emoji']} {s['title']} ({s['topic']})" for s in STORIES]
    sel = st.selectbox(
        "เลือกเรื่องที่อยากอ่าน",
        story_labels,
        index=st.session_state.get("read_story_idx", 0),
        key="story_sel"
    )
    sel_idx = story_labels.index(sel)
    if sel_idx != st.session_state.get("read_story_idx", 0):
        st.session_state["read_story_idx"] = sel_idx
        st.session_state["read_mode"]      = "read"
        st.session_state["read_q_idx"]     = 0
        st.session_state["read_score"]     = 0
        st.session_state["read_status"]    = None
        st.session_state["read_answers"]   = {}
        st.rerun()
 
    story = STORIES[sel_idx]
 
    # ── Sub-mode toggle ─────────────────────────────────────────
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("📖 อ่านเรื่อง", use_container_width=True):
            st.session_state["read_mode"] = "read"
            st.rerun()
    with col_r2:
        if st.button("📝 ทำแบบทดสอบ", use_container_width=True):
            st.session_state["read_mode"] = "quiz"
            st.session_state["read_q_idx"]   = 0
            st.session_state["read_score"]   = 0
            st.session_state["read_status"]  = None
            st.session_state["read_answers"] = {}
            st.rerun()
 
    st.markdown("---")
    read_sub = st.session_state.get("read_mode", "read")
 
    # ════════════════════════════════════════════════════════════
    # SUB-MODE: READ
    # ════════════════════════════════════════════════════════════
    if read_sub == "read":
        # Story card
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#3A2E1E,#4A3C26);
                    border-radius:16px;padding:1.25rem 1.75rem;margin-bottom:1rem;">
            <div style="font-size:0.6rem;font-weight:700;letter-spacing:0.12em;
                        text-transform:uppercase;color:#E8B855;opacity:0.7;margin-bottom:4px;">
                {story['level']} · {story['topic']}
            </div>
            <div style="font-family:'Fraunces',serif;font-size:1.5rem;color:#C8922A;
                        letter-spacing:-0.02em;line-height:1.2;">
                {story['emoji']} {story['title']}
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        # English text
        st.markdown(
            "<div style='font-size:0.7rem;font-weight:700;letter-spacing:0.1em;"
            "text-transform:uppercase;color:#9E8E78;margin-bottom:6px;'>"
            "📄 English Text</div>",
            unsafe_allow_html=True
        )
        st.markdown(f"""
        <div style="background:#FBF8F2;border:1.5px solid #DDD5C4;border-radius:14px;
                    padding:1.5rem;font-family:'Source Serif 4',serif;font-size:1rem;
                    line-height:1.85;color:#1E1810;margin-bottom:1rem;">
            {story['text']}
        </div>
        """, unsafe_allow_html=True)
 
        # Thai translation (collapsible)
        with st.expander("🇹🇭 ดูคำแปลภาษาไทย"):
            st.markdown(f"""
            <div style="background:#FDF4E0;border:1px solid #DDD5C4;border-radius:12px;
                        padding:1.25rem;font-size:0.92rem;color:#4A3C26;line-height:1.8;">
                {story['thai']}
            </div>
            """, unsafe_allow_html=True)
 
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"📝 เรื่องนี้มี **{len(story['questions'])} ข้อ** — กด **ทำแบบทดสอบ** ด้านบนเพื่อทดสอบความเข้าใจ")
 
    # ════════════════════════════════════════════════════════════
    # SUB-MODE: QUIZ
    # ════════════════════════════════════════════════════════════
    elif read_sub == "quiz":
        questions  = story["questions"]
        q_idx      = st.session_state.get("read_q_idx", 0)
        score      = st.session_state.get("read_score", 0)
        answers    = st.session_state.get("read_answers", {})
 
        # ── All done ──────────────────────────────────────────
        if q_idx >= len(questions):
            pct = int(score / len(questions) * 100)
            if pct == 100:
                st.balloons()
                grade_msg  = "🏆 ยอดเยี่ยม! ได้คะแนนเต็ม!"
                grade_color = "#1C4A1E"
                grade_bg    = "#EFF7EE"
                grade_bd    = "#A8C9A0"
            elif pct >= 75:
                grade_msg  = "👍 เก่งมาก! ความเข้าใจดีมาก"
                grade_color = "#3A2E1E"
                grade_bg    = "#FDF4E0"
                grade_bd    = "#C8922A"
            elif pct >= 50:
                grade_msg  = "📖 พอใช้ได้ ลองอ่านอีกครั้งนะ"
                grade_color = "#3A2E1E"
                grade_bg    = "#FBF8F2"
                grade_bd    = "#DDD5C4"
            else:
                grade_msg  = "💪 ยังต้องฝึกอีกนิด ลองอ่านแล้วทำใหม่นะ"
                grade_color = "#5A1A18"
                grade_bg    = "#FBF0EE"
                grade_bd    = "#E0A8A0"
 
            st.markdown(f"""
            <div style="background:{grade_bg};border:1px solid {grade_bd};
                        border-radius:16px;padding:2rem;text-align:center;margin-bottom:1.5rem;">
                <div style="font-family:'Fraunces',serif;font-size:1.75rem;
                            color:{grade_color};margin-bottom:0.5rem;">{grade_msg}</div>
                <div style="font-size:2.5rem;font-weight:700;color:#C8922A;">{score}/{len(questions)}</div>
                <div style="font-size:1rem;color:{grade_color};opacity:0.8;">{pct}% ถูกต้อง</div>
            </div>
            """, unsafe_allow_html=True)
 
            # Review answers
            st.markdown("#### 📋 เฉลยข้อสอบ")
            for i, q in enumerate(questions):
                chosen  = answers.get(i, "—")
                correct = q["answer"]
                is_ok   = chosen == correct
                icon    = "✅" if is_ok else "❌"
                bg      = "#EFF7EE" if is_ok else "#FBF0EE"
                bd      = "#A8C9A0" if is_ok else "#E0A8A0"
                st.markdown(f"""
                <div style="background:{bg};border:1px solid {bd};border-radius:12px;
                            padding:1rem 1.25rem;margin-bottom:0.75rem;">
                    <div style="font-size:0.85rem;font-weight:600;margin-bottom:4px;">
                        {icon} ข้อ {i+1}: {q['q']}
                    </div>
                    <div style="font-size:0.82rem;color:#1E1810;">
                        คำตอบของคุณ: <strong>{chosen}</strong>
                    </div>
                    {"" if is_ok else f'<div style="font-size:0.82rem;color:#1C4A1E;">เฉลย: <strong>{correct}</strong></div>'}
                    <div style="font-size:0.78rem;color:#6B5E4A;margin-top:4px;font-style:italic;">
                        💡 {q['explanation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
 
            col_retry, col_read = st.columns(2)
            with col_retry:
                if st.button("🔄 ทำใหม่อีกครั้ง", use_container_width=True):
                    st.session_state["read_q_idx"]   = 0
                    st.session_state["read_score"]   = 0
                    st.session_state["read_status"]  = None
                    st.session_state["read_answers"] = {}
                    st.rerun()
            with col_read:
                if st.button("📖 กลับไปอ่านเรื่อง", use_container_width=True):
                    st.session_state["read_mode"] = "read"
                    st.rerun()
            st.stop()
 
        # ── Current question ──────────────────────────────────
        q       = questions[q_idx]
        locked  = st.session_state.get("read_status") is not None
 
        # Progress
        st.markdown(
            f"<p style='font-size:0.82rem;color:#9E8E78;font-weight:500;"
            f"margin-bottom:4px;font-family:sans-serif;'>"
            f"ข้อ {q_idx+1} / {len(questions)} · คะแนน: {score}</p>",
            unsafe_allow_html=True
        )
        st.progress((q_idx) / len(questions))
 
        # Story title reminder
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#3A2E1E,#4A3C26);
                    border-radius:12px;padding:0.75rem 1.25rem;margin-bottom:0.75rem;">
            <div style="font-size:0.7rem;color:#E8B855;opacity:0.8;">
                {story['emoji']} {story['title']}
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        # Question box
        st.markdown(f"""
        <div style="background:#FBF8F2;border:1.5px solid #DDD5C4;border-radius:14px;
                    padding:1.25rem 1.5rem;margin-bottom:1rem;">
            <div style="font-size:0.6rem;font-weight:700;letter-spacing:0.1em;
                        text-transform:uppercase;color:#9E8E78;margin-bottom:8px;">
                คำถามที่ {q_idx+1}
            </div>
            <div style="font-family:'Source Serif 4',serif;font-size:1.05rem;
                        color:#1E1810;line-height:1.6;">
                {q['q']}
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        # Options
        user_choice = None
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        for i, col in enumerate([col1, col2, col3, col4]):
            with col:
                if st.button(
                    q["options"][i],
                    key=f"rq_{sel_idx}_{q_idx}_{i}",
                    use_container_width=True,
                    disabled=locked
                ):
                    user_choice = q["options"][i]
 
        # Process answer
        if user_choice:
            st.session_state["read_answers"][q_idx] = user_choice
            if user_choice == q["answer"]:
                st.session_state["read_status"] = "correct"
                st.session_state["read_score"] += 1
            else:
                st.session_state["read_status"] = "wrong"
                st.session_state["read_answers"][q_idx] = user_choice
            st.rerun()
 
        # Feedback
        status = st.session_state.get("read_status")
 
        if status == "correct":
            st.markdown(f"""
            <div class="result-correct">
                🎉 <strong>ถูกต้อง!</strong><br>
                <em style="opacity:0.8;">💡 {q['explanation']}</em>
            </div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ข้อถัดไป ➡️", key=f"rq_next_c_{q_idx}", use_container_width=True):
                st.session_state["read_q_idx"]  = q_idx + 1
                st.session_state["read_status"] = None
                st.rerun()
 
        elif status == "wrong":
            chosen = st.session_state["read_answers"].get(q_idx, "—")
            st.markdown(f"""
            <div class="result-wrong">
                ❌ <strong>ยังไม่ถูก</strong> — คำตอบที่ถูกต้องคือ <strong>{q['answer']}</strong><br>
                คุณเลือก: {chosen}<br>
                <em style="opacity:0.8;">💡 {q['explanation']}</em>
            </div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ข้อถัดไป ➡️", key=f"rq_next_w_{q_idx}", use_container_width=True):
                st.session_state["read_q_idx"]  = q_idx + 1
                st.session_state["read_status"] = None
                st.rerun()
            
