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
    "user_level":    "Level 1: Beginner (A1–A2)",
    "flash_mode":    "study",
    "study_idx":     0,
    "card_idx":      0,
    "flash_score":   0,
    "flash_status":  None,
    "cards":         [],
    "read_story_idx": 0,
    "read_q_idx":    0,
    "read_score":    0,
    "read_status":   None,
    "read_mode":     "read",
    "read_answers":  {},
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

DB    = load_db()
DB_OK = bool(DB)

def get_pool(level_label: str) -> list[dict]:
    if "A1" in level_label:
        return DB.get("A1", []) + DB.get("A2", [])
    elif "B1" in level_label:
        return DB.get("B1", []) + DB.get("B2", [])
    else:
        return DB.get("C1", []) + DB.get("C2", [])

def pick_cards(level_label: str, n: int = 10) -> list[dict]:
    pool   = get_pool(level_label)
    if not pool:
        return []
    sample = random.sample(pool, min(n, len(pool)))
    cards  = []
    for w in sample:
        thai       = w.get("thai", "").strip()
        definition = w.get("definition", "").strip()
        example    = w.get("example", "").strip()
        if not thai:
            thai = "(ยังไม่มีคำแปล)"
        if not definition or definition.startswith("Core vocabulary"):
            definition = f"{w['word'].capitalize()} ({w.get('pos','')}) — Oxford {w.get('source','5000')}"
        if not example:
            example = f"Please look up '{w['word']}' in a dictionary."
        cards.append({
            "word":        w["word"],
            "pos":         w.get("pos", ""),
            "definition":  definition,
            "thai":        thai,
            "example":     example,
            "source":      w.get("source", "Oxford 5000"),
            "streak":      0,
            "mastered":    False,
        })
    return cards

# ══════════════════════════════════════════════════════════════
# 3. WARM PAPER CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;500;600&display=swap');

:root {
    --paper:       #F5F0E4;
    --page:        #FBF8F0;
    --page-alt:    #F0EAD8;
    --card:        #FDFAF2;
    --border:      #D8CEB8;
    --border-lt:   #E8E0CC;
    --ink:         #241C0E;
    --ink-mid:     #6B5C44;
    --ink-faint:   #9E8E72;
    --amber:       #C4862A;
    --amber-dk:    #9E6C1A;
    --amber-lt:    #E8B84A;
    --amber-bg:    #FDF2DC;
    --spine:       #3A2A16;
    --spine-lt:    #4E3A20;
    --ok-bg:       #EDF6EC;
    --ok-bd:       #A0C8A0;
    --ok-ink:      #1E481E;
    --err-bg:      #FAF0EE;
    --err-bd:      #D8A8A0;
    --err-ink:     #5E2020;
    --shadow-sm:   0 1px 3px rgba(36,28,14,.07);
    --shadow-md:   0 4px 16px rgba(36,28,14,.1);
    --shadow-card: 0 8px 32px rgba(36,28,14,.16);
    --radius:      14px;
    --radius-sm:   9px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Base ── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMainBlockContainer"] {
    background: var(--paper) !important;
    font-family: 'Source Sans 3', sans-serif;
    color: var(--ink);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2.25rem !important;
    padding-bottom: 5rem !important;
    max-width: 680px !important;
}

/* ── Typography ── */
p, span, label, li,
.stMarkdown p,
[data-testid="stMarkdownContainer"] p {
    color: var(--ink);
    font-family: 'Source Sans 3', sans-serif;
    line-height: 1.7;
}
h3, h4 {
    font-family: 'Lora', serif !important;
    color: var(--spine) !important;
    letter-spacing: -0.02em !important;
    line-height: 1.25 !important;
}
h4 { font-size: 1.25rem !important; font-weight: 600 !important; margin-bottom: .1rem !important; }
.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--ink-faint) !important;
    font-size: 0.78rem !important;
}

/* ── App header ── */
.app-header {
    display: flex;
    flex-direction: column;
    gap: 0;
    margin-bottom: 1.75rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border-lt);
}
.app-accent { width: 28px; height: 3px; background: var(--amber); border-radius: 2px; margin-bottom: .65rem; }
.app-title  { font-family: 'Lora', serif; font-size: 2rem; color: var(--spine); font-weight: 600; letter-spacing: -.03em; line-height: 1.1; }
.app-sub    { font-size: .72rem; color: var(--ink-faint); letter-spacing: .13em; text-transform: uppercase; font-weight: 500; margin-top: .35rem; }

/* ── Settings bar ── */
.settings-bar {
    background: var(--page);
    border: 1px solid var(--border-lt);
    border-radius: var(--radius);
    padding: 1rem 1.25rem;
    margin-bottom: 1.25rem;
    box-shadow: var(--shadow-sm);
}

/* ── DB badge ── */
.db-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--amber-bg);
    border: 1px solid rgba(196,134,42,.25);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: .75rem;
    color: var(--amber-dk);
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: .02em;
}

/* ── Mode tab bar ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 3px;
    background: var(--page-alt);
    padding: 5px;
    border-radius: 12px;
    border: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 7px 14px;
    font-size: .82rem;
    font-weight: 500;
    color: var(--ink-faint);
    background: transparent;
    border: none;
    font-family: 'Source Sans 3', sans-serif;
    transition: color .15s;
}
.stTabs [aria-selected="true"] {
    background: var(--page) !important;
    color: var(--spine) !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(36,28,14,.1), 0 0 0 1px var(--border) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ── Buttons ── */
.stButton > button {
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 500 !important;
    font-size: .875rem !important;
    border-radius: var(--radius-sm) !important;
    border: 1.5px solid var(--border) !important;
    background: var(--page) !important;
    color: var(--ink) !important;
    padding: 8px 16px !important;
    transition: all .15s ease !important;
    box-shadow: var(--shadow-sm) !important;
    letter-spacing: .01em !important;
}
.stButton > button:hover {
    border-color: var(--amber) !important;
    background: var(--amber-bg) !important;
    color: var(--amber-dk) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(196,134,42,.18) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button:disabled {
    opacity: .45 !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Primary draw button — amber so text stays readable */
.stButton > button[kind="primary"] {
    background: var(--amber) !important;
    color: #241C0E !important;
    border-color: var(--amber-dk) !important;
    font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--amber-dk) !important;
    color: #FDF4E0 !important;
    border-color: var(--amber-dk) !important;
    box-shadow: 0 4px 14px rgba(160,104,26,.32) !important;
}

/* ── Mode segmented control ── */
.mode-toggle {
    display: flex;
    background: var(--page-alt);
    border: 1.5px solid var(--border);
    border-radius: 10px;
    padding: 4px;
    gap: 3px;
    margin-bottom: .25rem;
}
.mode-btn {
    flex: 1;
    padding: 8px 12px;
    border-radius: 7px;
    border: none;
    background: transparent;
    color: var(--ink-faint);
    font-family: 'Source Sans 3', sans-serif;
    font-size: .85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all .18s ease;
    text-align: center;
    white-space: nowrap;
}
.mode-btn:hover {
    background: var(--amber-bg);
    color: var(--amber-dk);
}
.mode-btn.active {
    background: var(--page);
    color: var(--spine);
    font-weight: 600;
    box-shadow: 0 1px 4px rgba(36,28,14,.12), 0 0 0 1px var(--border);
}
.mode-btn.active-quiz {
    background: var(--spine);
    color: #F5EDD8;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(36,28,14,.2);
}

/* ── Selectbox ── */
.stSelectbox [data-baseweb="select"] > div:first-child {
    border-radius: var(--radius-sm) !important;
    border-color: var(--border) !important;
    background: var(--page) !important;
    color: var(--ink) !important;
    font-size: .875rem !important;
}
.stSelectbox label {
    color: var(--ink-mid) !important;
    font-size: .78rem !important;
    font-weight: 500 !important;
}
[data-baseweb="popover"] li, [role="option"] {
    background: var(--page) !important;
    color: var(--ink) !important;
}
[role="option"]:hover { background: var(--amber-bg) !important; }

/* ── Radio as segmented control ── */
/* wrapper: match the height/padding of .stButton > button */
div[data-testid="stRadio"] {
    background: var(--page-alt) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    padding: 4px !important;
    margin-bottom: 0 !important;
    /* same visual height as button: button has 8px top+bottom pad + font ~1.25rem = ~36px total */
}
/* hide the label above */
div[data-testid="stRadio"] > div:first-child { display: none !important; }

/* radio group row */
div[data-testid="stRadio"] [role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    gap: 3px !important;
    width: 100% !important;
    align-items: stretch !important;
}

/* hide the actual radio dot */
div[data-testid="stRadio"] input[type="radio"] { display: none !important; }

/* each option label */
div[data-testid="stRadio"] label {
    flex: 1 !important;
    margin: 0 !important;
    padding: 6px 10px !important;
    border-radius: 6px !important;
    border: none !important;
    background: transparent !important;
    color: var(--ink-faint) !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: .85rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all .18s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 5px !important;
    white-space: nowrap !important;
    min-height: 30px !important;
}
div[data-testid="stRadio"] label:hover {
    background: var(--amber-bg) !important;
    color: var(--amber-dk) !important;
}
/* selected state */
div[data-testid="stRadio"] label:has(input:checked) {
    background: var(--page) !important;
    color: var(--spine) !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(36,28,14,.1), 0 0 0 1px var(--border) !important;
}
/* text inside label */
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
    font-size: .85rem !important;
    line-height: 1 !important;
    margin: 0 !important;
    color: inherit !important;
}

/* align-items: make radio column same height as adjacent button column */
.action-row > div[data-testid="stHorizontalBlock"] > div {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

/* ── Section divider ── */
.section-divider {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.25rem 0;
    color: var(--ink-faint);
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
}
.section-divider::before,
.section-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border-lt);
}

/* ── Flashcard (front/back CSS flip) ── */
/* handled inside components.html — see render_flashcard() */

/* ── Quiz word box ── */
.quiz-box {
    background: linear-gradient(145deg, var(--spine) 0%, var(--spine-lt) 100%);
    border-radius: var(--radius);
    padding: 2rem 1.75rem;
    text-align: center;
    box-shadow: var(--shadow-card);
    margin-bottom: 1.25rem;
    position: relative;
    overflow: hidden;
}
.quiz-box::before {
    content: 'Oxford 5000';
    position: absolute;
    top: 12px; right: 16px;
    font-size: .55rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--amber-lt);
    opacity: .55;
}
.quiz-word   { font-family: 'Lora', serif; font-size: 2.25rem; color: var(--amber); letter-spacing: -.02em; line-height: 1.1; }
.quiz-pos    { font-size: .75rem; color: rgba(255,255,255,.32); margin-top: 4px; }
.quiz-streak { font-size: .82rem; color: var(--amber-lt); margin-top: 10px; }

/* ── Quiz answer options ── */
div[data-testid="stHorizontalBlock"] .stButton > button {
    text-align: left !important;
    font-weight: 400 !important;
    min-height: 52px !important;
    height: auto !important;
    font-family: 'Lora', serif !important;
    font-size: .9rem !important;
    line-height: 1.45 !important;
    padding: 12px 14px !important;
}

/* ── Result boxes ── */
.result-ok, .result-err {
    border-radius: var(--radius-sm);
    padding: .9rem 1.2rem;
    font-size: .9rem;
    line-height: 1.65;
    margin-top: .6rem;
    font-family: 'Lora', serif;
}
.result-ok  { background: var(--ok-bg);  border: 1px solid var(--ok-bd);  color: var(--ok-ink); }
.result-err { background: var(--err-bg); border: 1px solid var(--err-bd); color: var(--err-ink); }

/* ── Completion card ── */
.done-card {
    border-radius: var(--radius);
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
    border: 1px solid;
}

/* ── Progress ── */
.stProgress > div > div > div { background: var(--amber) !important; border-radius: 4px; }
.stProgress > div > div       { background: var(--border-lt) !important; border-radius: 4px; }

/* ── Info / Alert ── */
.stAlert {
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--border-lt) !important;
    font-size: .875rem !important;
    background: var(--page) !important;
}

/* ── Story card (header) ── */
.story-header {
    background: linear-gradient(145deg, var(--spine) 0%, var(--spine-lt) 100%);
    border-radius: var(--radius);
    padding: 1.1rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-md);
}
.story-label { font-size: .58rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--amber-lt); opacity: .7; margin-bottom: 4px; }
.story-title { font-family: 'Lora', serif; font-size: 1.4rem; color: var(--amber); letter-spacing: -.02em; line-height: 1.2; }

/* ── Passage card ── */
.passage-card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-left: 3px solid var(--amber);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 1.5rem 1.75rem;
    font-family: 'Lora', serif;
    font-size: 1rem;
    line-height: 1.95;
    color: var(--ink);
    margin-bottom: 1rem;
    box-shadow: var(--shadow-sm);
}

/* ── Review answer items ── */
.review-item {
    border-radius: var(--radius-sm);
    padding: .9rem 1.1rem;
    margin-bottom: .65rem;
    border: 1px solid;
}

hr { border-color: var(--border-lt) !important; margin: 1.25rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 4. FLASHCARD HTML COMPONENT
# ══════════════════════════════════════════════════════════════
def render_flashcard(card: dict):
    pos_html  = f'<div class="pos">{card.get("pos","")}</div>' if card.get("pos") else ""
    thai_val  = card.get("thai", "")
    def_val   = card.get("definition", "")
    ex_val    = card.get("example", "")

    components.html(f"""<!DOCTYPE html>
<html>
<head>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:transparent;font-family:'Lora',Georgia,serif;padding:2px;}}
.scene{{width:100%;height:218px;perspective:1200px;}}
.card{{width:100%;height:100%;position:relative;transform-style:preserve-3d;
       transition:transform .55s cubic-bezier(.4,0,.2,1);border-radius:14px;cursor:pointer;}}
.card.flipped{{transform:rotateY(180deg);}}
.face{{position:absolute;inset:0;border-radius:14px;backface-visibility:hidden;
       -webkit-backface-visibility:hidden;display:flex;flex-direction:column;padding:1.6rem 1.9rem;}}
.front{{background:linear-gradient(145deg,#3A2A16,#4E3A20);color:#fff;
        box-shadow:0 8px 32px rgba(36,28,14,.22);align-items:center;justify-content:center;text-align:center;
        position:relative;overflow:hidden;}}
.front::after{{content:'Oxford 5000';position:absolute;top:11px;right:15px;
               font-size:.52rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
               color:#E8B84A;opacity:.55;font-family:sans-serif;}}
.back{{background:#FDFAF2;border:1.5px solid #D8CEB8;transform:rotateY(180deg);
       align-items:flex-start;justify-content:flex-start;gap:9px;overflow-y:auto;
       box-shadow:0 8px 28px rgba(36,28,14,.08);}}
.word{{font-size:2.35rem;color:#C4862A;letter-spacing:-.02em;line-height:1.05;font-weight:700;}}
.pos{{font-size:.7rem;color:rgba(255,255,255,.32);margin-top:5px;font-family:sans-serif;letter-spacing:.04em;}}
.hint{{font-size:.68rem;color:rgba(255,255,255,.25);margin-top:12px;font-family:sans-serif;letter-spacing:.04em;}}
.lbl{{font-size:.58rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#9E8E72;
      margin-bottom:2px;font-family:sans-serif;}}
.val{{font-size:.9rem;color:#241C0E;line-height:1.6;}}
.sec{{width:100%;}}
</style>
</head>
<body>
<div class="scene">
  <div class="card" id="fc">
    <div class="face front">
      <div class="word">{card['word']}</div>
      {pos_html}
      <div class="hint">แตะการ์ดเพื่อพลิกดูความหมาย</div>
    </div>
    <div class="face back">
      <div class="sec">
        <div class="lbl">ความหมายภาษาไทย</div>
        <div class="val" style="font-weight:600;font-size:.98rem;color:#3A2A16;">{thai_val}</div>
      </div>
      <div class="sec">
        <div class="lbl">Definition</div>
        <div class="val">{def_val}</div>
      </div>
      <div class="sec">
        <div class="lbl">Example</div>
        <div class="val" style="font-style:italic;color:#6B5C44;">"{ex_val}"</div>
      </div>
    </div>
  </div>
</div>
<script>
  document.getElementById('fc').addEventListener('click',function(){{
    this.classList.toggle('flipped');
  }});
</script>
</body>
</html>""", height=228, scrolling=False)

# ══════════════════════════════════════════════════════════════
# 5. HEADER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="app-header">
  <div class="app-accent"></div>
  <div class="app-title">Oxford Flashcards</div>
  <div class="app-sub">Offline · Oxford 5000 · ฝึกคำศัพท์วิชาการ</div>
</div>
""", unsafe_allow_html=True)

if not DB_OK:
    st.error("❌ ไม่พบ oxford_db_enriched.json — วางไฟล์ไว้ในโฟลเดอร์เดียวกับ flashcard_offline.py")
    st.stop()

# ══════════════════════════════════════════════════════════════
# 6. MAIN TAB BAR  (Flashcards / Reading แยกชัด ไม่ต้องสุ่มก่อน)
# ══════════════════════════════════════════════════════════════
tab_flash, tab_read = st.tabs(["📇 Flashcards & Quiz", "📚 อ่านเรื่องสั้น"])

# ══════════════════════════════════════════════════════════════
# ─────────────────────── TAB 1: FLASHCARDS ───────────────────
# ══════════════════════════════════════════════════════════════
with tab_flash:

    # ── Settings row ──────────────────────────────────────────
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
    st.markdown(
        f'<div class="db-badge">📦 Oxford DB · ระดับนี้มี {len(pool):,} คำ</div>',
        unsafe_allow_html=True
    )

    # ── Action row ────────────────────────────────────────────
    st.markdown('<div class="action-row">', unsafe_allow_html=True)
    col_toggle = st.columns([1])[0]
    with col_toggle:
        mode_choice = st.radio(
            "โหมดจำคำศัพท์",
            options=["📖 เรียนรู้", "🎮 ควิซ"],
            index=0 if st.session_state["flash_mode"] == "study" else 1,
            horizontal=True,
            label_visibility="collapsed",
            key="mode_radio"
        )
        new_mode = "study" if "เรียนรู้" in mode_choice else "quiz"
        if new_mode != st.session_state["flash_mode"]:
            st.session_state["flash_mode"] = new_mode
            st.rerun()
    with col_draw:
        if st.button("🎲 สุ่มการ์ดใหม่", use_container_width=True, type="primary"):
            cards_new = pick_cards(st.session_state["user_level"], n_cards)
            st.session_state.update({
                "cards":        cards_new,
                "study_idx":    0,
                "card_idx":     0,
                "flash_score":  0,
                "flash_status": None,
            })
            if "current_options" in st.session_state:
                del st.session_state["current_options"]
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    cards = st.session_state.get("cards", [])
    mode  = st.session_state["flash_mode"]

    # ── No cards yet ───────────────────────────────────────────
    if not cards:
        st.markdown("""
        <div style="text-align:center;padding:2.5rem 1rem;">
            <div style="font-size:2.5rem;margin-bottom:.75rem;">🎴</div>
            <div style="font-family:'Lora',serif;font-size:1.1rem;color:#6B5C44;margin-bottom:.4rem;">
                ยังไม่มีการ์ดในเซ็ตนี้
            </div>
            <div style="font-size:.85rem;color:#9E8E72;">กด <strong style="color:#6B5C44;">สุ่มการ์ดใหม่</strong> ด้านบนเพื่อเริ่มฝึก</div>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # STUDY MODE
    # ══════════════════════════════════════════════════════════
    elif mode == "study":
        st.markdown("#### 👀 ฝึกจำคำศัพท์")

        s_idx = st.session_state.get("study_idx", 0)
        if s_idx >= len(cards):
            s_idx = 0
            st.session_state["study_idx"] = 0
        card = cards[s_idx]

        render_flashcard(card)

        st.markdown("<br>", unsafe_allow_html=True)
        col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
        with col_b1:
            if st.button("⬅️ ก่อนหน้า", disabled=(s_idx == 0), use_container_width=True):
                st.session_state["study_idx"] = s_idx - 1
                st.rerun()
        with col_b2:
            st.markdown(
                f"<p style='text-align:center;font-size:.82rem;color:#9E8E72;margin-top:10px;'>"
                f"ใบที่ {s_idx+1} / {len(cards)}</p>",
                unsafe_allow_html=True
            )
        with col_b3:
            if st.button("ถัดไป ➡️", disabled=(s_idx == len(cards)-1), use_container_width=True):
                st.session_state["study_idx"] = s_idx + 1
                st.rerun()

        st.markdown("---")
        st.info("💡 จำให้ครบก่อน แล้วกด **โหมดควิซ** ด้านบนเพื่อทดสอบตัวเอง")

    # ══════════════════════════════════════════════════════════
    # QUIZ MODE
    # ══════════════════════════════════════════════════════════
    elif mode == "quiz":
        st.markdown("#### 🎮 โหมดควิซ — เลือกคำแปลที่ถูกต้อง")

        unmastered    = [c for c in cards if not c.get("mastered", False)]
        mastered_count = len(cards) - len(unmastered)

        col_prog, col_sco = st.columns([3, 1])
        with col_prog:
            st.markdown(
                f"<p style='font-size:.82rem;color:#9E8E72;font-weight:500;margin-bottom:4px;'>"
                f"จำได้แม่นยำ {mastered_count} / {len(cards)} คำ</p>",
                unsafe_allow_html=True
            )
            st.progress(mastered_count / len(cards))
        with col_sco:
            st.markdown(
                f"<p style='text-align:right;font-weight:600;color:#C4862A;font-size:1rem;margin-top:4px;'>"
                f"🏆 {st.session_state['flash_score']} คะแนน</p>",
                unsafe_allow_html=True
            )

        # ── All mastered ──
        if not unmastered:
            st.balloons()
            st.markdown(f"""
            <div class="done-card" style="background:#EDF6EC;border-color:#A0C8A0;">
                <div style="font-family:'Lora',serif;font-size:1.6rem;color:#1E481E;margin-bottom:.4rem;">
                    🏆 ยอดเยี่ยม! จำได้ครบเซ็ตแล้ว
                </div>
                <div style="font-size:.95rem;color:#1E481E;opacity:.85;">
                    ผ่านเงื่อนไขตอบถูก 3 ครั้งติดต่อกันครบทั้ง {len(cards)} คำ
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 เริ่มใหม่", use_container_width=True):
                for c in cards:
                    c["streak"] = 0
                    c["mastered"] = False
                st.session_state.update({"card_idx":0,"flash_score":0,"flash_status":None})
                if "current_options" in st.session_state:
                    del st.session_state["current_options"]
                st.rerun()
            st.stop()

        idx  = st.session_state.get("card_idx", 0)
        if idx >= len(cards): idx = 0; st.session_state["card_idx"] = 0
        card = cards[idx]

        if "current_options" not in st.session_state:
            correct    = card.get("thai", "")
            distractors = [
                c.get("thai","—") for i,c in enumerate(cards)
                if i != idx and c.get("thai","").strip() and not c["thai"].startswith("(ยังไม่มี")
            ]
            if len(distractors) < 3:
                extra = [w.get("thai","") for w in get_pool(st.session_state["user_level"])
                         if w.get("thai","").strip() and w["word"] != card["word"]]
                random.shuffle(extra)
                distractors += extra
            opts = distractors[:3] + [correct]
            random.shuffle(opts)
            st.session_state["current_options"] = opts

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
            "<p style='font-size:.78rem;font-weight:600;color:#9E8E72;"
            "letter-spacing:.06em;text-transform:uppercase;margin-bottom:.5rem;'>"
            "เลือกคำแปลที่ถูกต้อง</p>",
            unsafe_allow_html=True
        )

        options    = st.session_state["current_options"]
        locked     = st.session_state["flash_status"] is not None
        user_choice = None
        col1,col2 = st.columns(2)
        col3,col4 = st.columns(2)
        for i,col in enumerate([col1,col2,col3,col4]):
            with col:
                if st.button(f"{i+1}. {options[i]}", key=f"opt_{idx}_{i}",
                             use_container_width=True, disabled=locked):
                    user_choice = options[i]

        if user_choice:
            correct_thai = card.get("thai","")
            if user_choice == correct_thai:
                st.session_state["flash_status"] = "correct"
                st.session_state["flash_score"] += 1
                card["streak"] += 1
                if card["streak"] >= 3:
                    card["mastered"] = True
            else:
                st.session_state["flash_status"] = "wrong"
                card["streak"] = 0
            st.rerun()

        status = st.session_state["flash_status"]

        if status == "correct":
            st.markdown(f"""
            <div class="result-ok">
                🎉 <strong>ถูกต้อง!</strong> แปลว่า <strong>{card.get('thai','')}</strong><br>
                <span style="opacity:.85;">{card['definition']}</span><br>
                <em style="opacity:.7;">"{card.get('example','')}"</em>
            </div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ข้อถัดไป ➡️", key="next_c", use_container_width=True):
                remains = [c for c in cards if not c.get("mastered",False)]
                if remains:
                    st.session_state["card_idx"] = cards.index(random.choice(remains))
                st.session_state["flash_status"] = None
                if "current_options" in st.session_state:
                    del st.session_state["current_options"]
                st.rerun()

        elif status == "wrong":
            st.markdown(f"""
            <div class="result-err">
                ❌ <strong>ยังไม่ถูก</strong> — คำตอบที่ถูกต้องคือ <strong>{card.get('thai','')}</strong><br>
                <span style="opacity:.85;">{card['definition']}</span><br>
                <em style="opacity:.7;">"{card.get('example','')}"</em>
            </div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ข้ามไปข้อถัดไป ➡️", key="next_w", use_container_width=True):
                remains = [c for c in cards if not c.get("mastered",False)]
                if remains:
                    st.session_state["card_idx"] = cards.index(random.choice(remains))
                st.session_state["flash_status"] = None
                if "current_options" in st.session_state:
                    del st.session_state["current_options"]
                st.rerun()


# ══════════════════════════════════════════════════════════════
# ─────────────────────── TAB 2: READING ──────────────────────
# ══════════════════════════════════════════════════════════════
with tab_read:
    st.markdown("#### 📚 ฝึกอ่านเรื่องสั้น")

    story_labels = [f"{s['emoji']} {s['title']}  ({s['topic']})" for s in STORIES]
    sel = st.selectbox(
        "เลือกเรื่องที่อยากอ่าน",
        story_labels,
        index=st.session_state.get("read_story_idx", 0),
        key="story_sel"
    )
    sel_idx = story_labels.index(sel)
    if sel_idx != st.session_state.get("read_story_idx", 0):
        st.session_state.update({
            "read_story_idx": sel_idx,
            "read_mode":      "read",
            "read_q_idx":     0,
            "read_score":     0,
            "read_status":    None,
            "read_answers":   {},
        })
        st.rerun()

    story = STORIES[sel_idx]

    read_choice = st.radio(
        "โหมดอ่าน",
        options=["📖 อ่านเรื่อง", "📝 ทำแบบทดสอบ"],
        index=0 if st.session_state.get("read_mode", "read") == "read" else 1,
        horizontal=True,
        label_visibility="collapsed",
        key="read_mode_radio"
    )
    new_read_mode = "read" if "อ่านเรื่อง" in read_choice else "quiz"
    if new_read_mode != st.session_state.get("read_mode", "read"):
        st.session_state.update({
            "read_mode":    new_read_mode,
            "read_q_idx":   0,
            "read_score":   0,
            "read_status":  None,
            "read_answers": {},
        })
        st.rerun()

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    read_sub = st.session_state.get("read_mode", "read")

    # ══════════════════════════════════════════════════════════
    # READ SUB-MODE
    # ══════════════════════════════════════════════════════════
    if read_sub == "read":
        st.markdown(f"""
        <div class="story-header">
            <div class="story-label">{story['level']} · {story['topic']}</div>
            <div class="story-title">{story['emoji']} {story['title']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            "<div style='font-size:.65rem;font-weight:700;letter-spacing:.1em;"
            "text-transform:uppercase;color:#9E8E72;margin-bottom:6px;'>📄 English Text</div>",
            unsafe_allow_html=True
        )
        st.markdown(f'<div class="passage-card">{story["text"]}</div>', unsafe_allow_html=True)

        with st.expander("🇹🇭 ดูคำแปลภาษาไทย"):
            st.markdown(f"""
            <div style="background:#FDF2DC;border:1px solid #D8CEB8;border-radius:10px;
                        padding:1.2rem;font-size:.92rem;color:#4E3A20;line-height:1.8;">
                {story['thai']}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"📝 เรื่องนี้มี **{len(story['questions'])} ข้อ** — กด **ทำแบบทดสอบ** ด้านบนเพื่อทดสอบความเข้าใจ")

    # ══════════════════════════════════════════════════════════
    # QUIZ SUB-MODE
    # ══════════════════════════════════════════════════════════
    elif read_sub == "quiz":
        questions = story["questions"]
        q_idx     = st.session_state.get("read_q_idx", 0)
        score     = st.session_state.get("read_score", 0)
        answers   = st.session_state.get("read_answers", {})

        # ── All done ──
        if q_idx >= len(questions):
            pct = int(score / len(questions) * 100)
            if pct == 100:
                st.balloons()
                g_msg, g_color, g_bg, g_bd = "🏆 ยอดเยี่ยม! ได้คะแนนเต็ม!", "#1E481E", "#EDF6EC", "#A0C8A0"
            elif pct >= 75:
                g_msg, g_color, g_bg, g_bd = "👍 เก่งมาก! ความเข้าใจดีมาก", "#3A2A16", "#FDF2DC", "#C4862A"
            elif pct >= 50:
                g_msg, g_color, g_bg, g_bd = "📖 พอใช้ได้ ลองอ่านอีกครั้งนะ", "#3A2A16", "#FBF8F0", "#D8CEB8"
            else:
                g_msg, g_color, g_bg, g_bd = "💪 ยังต้องฝึกอีกนิด ลองอ่านแล้วทำใหม่", "#5E2020", "#FAF0EE", "#D8A8A0"

            st.markdown(f"""
            <div class="done-card" style="background:{g_bg};border-color:{g_bd};">
                <div style="font-family:'Lora',serif;font-size:1.55rem;color:{g_color};margin-bottom:.4rem;">
                    {g_msg}
                </div>
                <div style="font-size:2.25rem;font-weight:700;color:#C4862A;">{score}/{len(questions)}</div>
                <div style="font-size:.95rem;color:{g_color};opacity:.8;">{pct}% ถูกต้อง</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### 📋 เฉลยข้อสอบ")
            for i, q in enumerate(questions):
                chosen  = answers.get(i, "—")
                correct = q["answer"]
                is_ok   = chosen == correct
                icon    = "✅" if is_ok else "❌"
                bg      = "#EDF6EC" if is_ok else "#FAF0EE"
                bd      = "#A0C8A0" if is_ok else "#D8A8A0"
                wrong_line = "" if is_ok else f'<div style="font-size:.82rem;color:#1E481E;">เฉลย: <strong>{correct}</strong></div>'
                st.markdown(f"""
                <div class="review-item" style="background:{bg};border-color:{bd};">
                    <div style="font-size:.85rem;font-weight:600;margin-bottom:4px;color:#241C0E;">
                        {icon} ข้อ {i+1}: {q['q']}
                    </div>
                    <div style="font-size:.82rem;color:#241C0E;">คำตอบของคุณ: <strong>{chosen}</strong></div>
                    {wrong_line}
                    <div style="font-size:.78rem;color:#6B5C44;margin-top:5px;font-style:italic;">
                        💡 {q['explanation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            col_retry, col_read = st.columns(2)
            with col_retry:
                if st.button("🔄 ทำใหม่อีกครั้ง", use_container_width=True):
                    st.session_state.update({
                        "read_q_idx":   0,
                        "read_score":   0,
                        "read_status":  None,
                        "read_answers": {},
                    })
                    st.rerun()
            with col_read:
                if st.button("📖 กลับไปอ่านเรื่อง", use_container_width=True):
                    st.session_state["read_mode"] = "read"
                    st.rerun()
            st.stop()

        # ── Current question ──
        q      = questions[q_idx]
        locked = st.session_state.get("read_status") is not None

        st.markdown(
            f"<p style='font-size:.82rem;color:#9E8E72;font-weight:500;margin-bottom:4px;'>"
            f"ข้อ {q_idx+1} / {len(questions)} · คะแนน: {score}</p>",
            unsafe_allow_html=True
        )
        st.progress(q_idx / len(questions))

        st.markdown(f"""
        <div class="story-header" style="padding:.7rem 1.25rem;margin-bottom:.75rem;">
            <div style="font-size:.7rem;color:#E8B84A;opacity:.8;">{story['emoji']} {story['title']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#FBF8F0;border:1.5px solid #D8CEB8;border-radius:12px;
                    padding:1.2rem 1.4rem;margin-bottom:1rem;">
            <div style="font-size:.58rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
                        color:#9E8E72;margin-bottom:8px;">คำถามที่ {q_idx+1}</div>
            <div style="font-family:'Lora',serif;font-size:1.05rem;color:#241C0E;line-height:1.6;">
                {q['q']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        user_choice = None
        col1,col2 = st.columns(2)
        col3,col4 = st.columns(2)
        for i, col in enumerate([col1,col2,col3,col4]):
            with col:
                if st.button(q["options"][i], key=f"rq_{sel_idx}_{q_idx}_{i}",
                             use_container_width=True, disabled=locked):
                    user_choice = q["options"][i]

        if user_choice:
            st.session_state["read_answers"][q_idx] = user_choice
            if user_choice == q["answer"]:
                st.session_state["read_status"] = "correct"
                st.session_state["read_score"] += 1
            else:
                st.session_state["read_status"] = "wrong"
            st.rerun()

        status = st.session_state.get("read_status")

        if status == "correct":
            st.markdown(f"""
            <div class="result-ok">
                🎉 <strong>ถูกต้อง!</strong><br>
                <em style="opacity:.82;">💡 {q['explanation']}</em>
            </div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ข้อถัดไป ➡️", key=f"rq_next_c_{q_idx}", use_container_width=True):
                st.session_state["read_q_idx"]  = q_idx + 1
                st.session_state["read_status"] = None
                st.rerun()

        elif status == "wrong":
            chosen = st.session_state["read_answers"].get(q_idx, "—")
            st.markdown(f"""
            <div class="result-err">
                ❌ <strong>ยังไม่ถูก</strong> — คำตอบที่ถูกต้องคือ <strong>{q['answer']}</strong><br>
                คุณเลือก: {chosen}<br>
                <em style="opacity:.82;">💡 {q['explanation']}</em>
            </div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ข้อถัดไป ➡️", key=f"rq_next_w_{q_idx}", use_container_width=True):
                st.session_state["read_q_idx"]  = q_idx + 1
                st.session_state["read_status"] = None
                st.rerun()
