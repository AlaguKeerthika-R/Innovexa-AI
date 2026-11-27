"""Global look & feel for ProjectMentor AI (dark developer theme).

All colours live in the :root variables below, so re-theming the whole app
(for example back to a light/pastel palette) only means editing that block.
"""

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root{
  --bg:#0a0e1a; --bg2:#0d1322; --panel:#121a2d; --panel2:#18223a;
  --border:#263250; --border2:#34436b;
  --text:#e7ecf7; --muted:#8c98b5; --dim:#5f6c8a;
  --accent:#7c8cff; --accent2:#22d3b6; --accent3:#c084fc;
  --ok:#34d399; --warn:#fbbf24; --err:#f87171;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}

/* ---------- base ---------- */
.stApp{
  background-color:var(--bg);
  background-image:
    radial-gradient(rgba(140,152,181,.11) 1px, transparent 1px),
    radial-gradient(900px 520px at 6% -8%, rgba(124,140,255,.17), transparent 60%),
    radial-gradient(800px 480px at 100% 0%, rgba(34,211,182,.10), transparent 55%);
  background-size:26px 26px, auto, auto;
  background-attachment:fixed;
  color:var(--text);
  font-family:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;
}
[data-testid="stHeader"]{background:transparent;}
#MainMenu, footer{visibility:hidden;}
.block-container{max-width:1240px;padding-top:2rem;padding-bottom:4rem;}
.stApp p,.stApp li,.stApp label,.stApp input,.stApp textarea,.stApp button{font-family:'Inter',system-ui,sans-serif;}
.stApp p,.stApp li{color:#c3cce0;}
.stApp h1,.stApp h2,.stApp h3,.stApp h4{color:var(--text)!important;letter-spacing:-.02em;font-weight:700;}
.stApp code{font-family:var(--mono)!important;}
.stApp hr{border-color:var(--border);}
[data-testid="stCaptionContainer"]{color:var(--muted);}
[data-testid="stMarkdownContainer"] pre,
[data-testid="stCodeBlock"] pre{background:#070b15!important;border:1px solid var(--border);border-radius:12px;}
::-webkit-scrollbar{width:10px;height:10px;}
::-webkit-scrollbar-thumb{background:#26335a;border-radius:8px;}
::-webkit-scrollbar-track{background:transparent;}

/* ---------- sidebar ---------- */
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0c1222 0%,#0a0e1a 100%);
  border-right:1px solid var(--border);
}
[data-testid="stSidebar"] .block-container{padding-top:1.4rem;}
[data-testid="stSidebar"] .stButton>button{
  background:transparent!important;border:1px solid transparent!important;color:var(--muted)!important;
  justify-content:flex-start;box-shadow:none!important;min-height:40px;font-weight:500!important;
}
[data-testid="stSidebar"] .stButton>button p{color:var(--muted)!important;}
[data-testid="stSidebar"] .stButton>button:hover{background:var(--panel2)!important;border-color:var(--border)!important;transform:none;filter:none;}
[data-testid="stSidebar"] .stButton>button:hover p{color:var(--text)!important;}
[data-testid="stSidebar"] button[kind="primary"],
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"]{
  background:rgba(124,140,255,.14)!important;border:1px solid rgba(124,140,255,.45)!important;
}
[data-testid="stSidebar"] button[kind="primary"] p,
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] p{color:#dfe4ff!important;}

/* ---------- inputs ---------- */
.stTextInput input,.stTextArea textarea,.stNumberInput input{
  background:var(--bg2)!important;color:var(--text)!important;
  border:1px solid var(--border)!important;border-radius:10px!important;font-size:.95rem;
}
.stTextInput input:focus,.stTextArea textarea:focus{
  border-color:var(--accent)!important;box-shadow:0 0 0 3px rgba(124,140,255,.18)!important;
}
.stTextInput input:disabled{opacity:.6;}
div[data-baseweb="select"]>div,div[data-baseweb="input"]{
  background:var(--bg2)!important;border-color:var(--border)!important;border-radius:10px!important;
}
div[data-baseweb="popover"] ul,ul[role="listbox"]{background:var(--panel)!important;}
li[role="option"]:hover{background:var(--panel2)!important;}
[data-testid="stWidgetLabel"] p,.stApp label{color:var(--muted)!important;font-weight:500;font-size:.85rem;}

/* ---------- buttons ---------- */
.stButton>button,.stFormSubmitButton>button{
  background:linear-gradient(135deg,#6f7dff,#5560e8)!important;color:#fff!important;
  border:1px solid rgba(255,255,255,.12)!important;border-radius:10px!important;min-height:44px;
  font-weight:600!important;letter-spacing:.01em;
  transition:transform .15s ease,box-shadow .15s ease,filter .15s ease;
}
.stButton>button p,.stFormSubmitButton>button p{color:#fff!important;}
.stButton>button:hover,.stFormSubmitButton>button:hover{
  transform:translateY(-1px);box-shadow:0 8px 24px rgba(99,112,255,.35);filter:brightness(1.08);
}
.stDownloadButton>button{
  background:rgba(34,211,182,.08)!important;color:#7ff0da!important;
  border:1px solid rgba(34,211,182,.4)!important;border-radius:10px!important;font-weight:600;
}
.stDownloadButton>button p{color:#7ff0da!important;}
.stDownloadButton>button:hover{background:rgba(34,211,182,.16)!important;}

/* ---------- containers / widgets ---------- */
[data-testid="stVerticalBlockBorderWrapper"]{
  background:rgba(18,26,45,.78);border:1px solid var(--border);border-radius:16px;
}
[data-testid="stForm"]{
  background:rgba(18,26,45,.6);border:1px solid var(--border);border-radius:14px;padding:20px;
}
[data-testid="stMetric"]{
  background:rgba(18,26,45,.85);border:1px solid var(--border);border-radius:14px;padding:16px 18px;
}
[data-testid="stMetricLabel"] p{font:600 11px var(--mono)!important;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)!important;}
[data-testid="stMetricValue"]{font-weight:700;color:var(--text);}
button[data-baseweb="tab"]{color:var(--muted);font-weight:600;}
button[data-baseweb="tab"][aria-selected="true"]{color:var(--accent);}
[data-baseweb="tab-highlight"]{background:var(--accent)!important;}
[data-baseweb="tab-border"]{background:var(--border)!important;}
[data-testid="stExpander"]{background:rgba(18,26,45,.7);border:1px solid var(--border);border-radius:12px;}
[data-testid="stAlert"]{border-radius:12px;}

/* ---------- shared keyframes ---------- */
@keyframes pm-blink{50%{opacity:0}}
@keyframes pm-rotate{to{transform:rotate(360deg)}}
@keyframes pm-slide{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@keyframes pm-ping{
  0%{box-shadow:0 0 0 0 rgba(52,211,153,.55)}
  70%{box-shadow:0 0 0 10px rgba(52,211,153,0)}
  100%{box-shadow:0 0 0 0 rgba(52,211,153,0)}
}

/* ---------- custom components ---------- */
.pm-kicker{font:600 11.5px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--accent2);margin-bottom:10px;}
.pm-section{font:600 12px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:34px 0 14px;}
.pm-section::before{content:"// ";color:var(--accent);}
.stApp .pm-pagehead{margin:4px 0 20px;}
.stApp .pm-pagehead h1{font-size:2.1rem!important;font-weight:800!important;margin:0 0 6px!important;padding:0!important;line-height:1.15!important;}
.stApp .pm-pagehead p{margin:0;color:var(--muted);font-size:1rem;}
.pm-grad{background:linear-gradient(90deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;}

.pm-badge{display:inline-flex;align-items:center;gap:8px;padding:5px 12px;border:1px solid var(--border2);border-radius:999px;background:rgba(124,140,255,.08);font:500 12px var(--mono);color:#b7c1ff;}
.pm-pulse{width:8px;height:8px;border-radius:50%;background:var(--ok);animation:pm-ping 1.8s infinite;}

.pm-hero{display:grid;grid-template-columns:1.1fr 1fr;gap:28px;align-items:center;padding:30px;border:1px solid var(--border);border-radius:20px;background:linear-gradient(135deg,rgba(24,34,58,.85),rgba(14,20,36,.85));box-shadow:0 24px 60px rgba(0,0,0,.35);}
.stApp .pm-hero h1,.stApp .pm-auth h1{font-size:2.5rem!important;font-weight:800!important;line-height:1.1!important;margin:14px 0 12px!important;padding:0!important;}
.stApp .pm-auth h1{font-size:2.9rem!important;}
.stApp .pm-hero p.lead,.stApp .pm-auth p.lead{color:var(--muted);font-size:1.02rem;line-height:1.65;margin:0 0 22px;}
@media(max-width:860px){.pm-hero{grid-template-columns:1fr;}}

.pm-terminal{background:#070b15;border:1px solid var(--border);border-radius:14px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.45);}
.pm-term-bar{display:flex;align-items:center;gap:7px;padding:10px 14px;border-bottom:1px solid var(--border);background:#0d1424;}
.pm-term-bar u{width:10px;height:10px;border-radius:50%;background:#ff5f57;display:inline-block;text-decoration:none;}
.pm-term-bar u:nth-child(2){background:#febc2e;}
.pm-term-bar u:nth-child(3){background:#28c840;}
.pm-term-bar span{margin-left:8px;color:var(--dim);font:12px var(--mono);}
.pm-term-body{padding:16px 18px;}
.stApp .pm-term-body p{margin:0 0 7px;font:12.5px/1.5 var(--mono);color:var(--muted);white-space:pre-wrap;opacity:0;animation:pm-slide .5s ease forwards;animation-delay:calc(var(--i)*.35s);}
.pm-term-body .ok{color:var(--ok);}
.pm-term-body .cmd{color:var(--accent2);}
.pm-term-body .nm{color:#c3cce0;}
.pm-rot{display:inline-block;color:var(--accent);animation:pm-rotate 1s linear infinite;}
.pm-cur{display:inline-block;width:8px;height:15px;background:var(--accent2);vertical-align:-2px;margin-left:4px;animation:pm-blink 1s steps(1) infinite;}

.pm-grid{display:grid;gap:14px;}
.pm-grid.c4{grid-template-columns:repeat(4,1fr);}
@media(max-width:900px){.pm-grid.c4{grid-template-columns:repeat(2,1fr);}}
.pm-card{padding:18px;border:1px solid var(--border);border-radius:14px;background:rgba(18,26,45,.8);transition:transform .2s,border-color .2s,box-shadow .2s;}
.pm-card:hover{transform:translateY(-3px);border-color:var(--border2);box-shadow:0 14px 34px rgba(0,0,0,.35);}
.pm-card .no{font:700 12px var(--mono);color:var(--accent);letter-spacing:.1em;}
.pm-card b{display:block;font-size:1.02rem;color:var(--text);margin:8px 0 4px;}
.pm-card small{color:var(--muted);font-size:.88rem;line-height:1.5;}

.pm-agents{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:14px;}
.pm-agent{position:relative;padding:16px;border:1px solid var(--border);border-radius:14px;background:rgba(18,26,45,.8);overflow:hidden;transition:transform .2s,border-color .2s;}
.pm-agent::after{content:"";position:absolute;inset:0;background:linear-gradient(120deg,transparent 30%,rgba(124,140,255,.10),transparent 70%);transform:translateX(-100%);transition:transform .6s;}
.pm-agent:hover{transform:translateY(-3px);border-color:var(--accent);}
.pm-agent:hover::after{transform:translateX(100%);}
.pm-agent .ic{width:40px;height:40px;border-radius:11px;display:grid;place-items:center;font-size:20px;background:rgba(124,140,255,.12);border:1px solid var(--border2);}
.pm-agent .no{position:absolute;top:14px;right:14px;font:600 11px var(--mono);color:var(--dim);}
.pm-agent b{display:block;margin:12px 0 3px;color:var(--text);font-size:.98rem;}
.pm-agent small{color:var(--muted);font-size:.84rem;line-height:1.45;}

.pm-flow{display:flex;gap:10px;margin:2px 0 22px;flex-wrap:wrap;}
.pm-flow-item{display:flex;align-items:center;gap:9px;padding:7px 14px 7px 8px;border:1px solid var(--border);border-radius:999px;font:500 12.5px var(--mono);color:var(--dim);background:rgba(18,26,45,.6);}
.pm-flow-item i{font-style:normal;width:22px;height:22px;border-radius:50%;display:grid;place-items:center;font-size:11px;background:var(--panel2);color:var(--muted);}
.pm-flow-item.done{color:var(--ok);border-color:rgba(52,211,153,.35);}
.pm-flow-item.done i{background:rgba(52,211,153,.15);color:var(--ok);}
.pm-flow-item.active{color:var(--text);border-color:var(--accent);box-shadow:0 0 0 3px rgba(124,140,255,.15);}
.pm-flow-item.active i{background:var(--accent);color:#fff;}

.pm-chip{display:inline-block;margin:0 6px 6px 0;padding:4px 11px;border-radius:8px;border:1px solid var(--border2);background:var(--panel2);font:500 12px var(--mono);color:#b7c1ff;}
.pm-project{padding:22px 24px;border:1px solid var(--border);border-radius:16px;background:rgba(18,26,45,.85);margin-bottom:18px;}
.stApp .pm-project h2{margin:0 0 10px!important;padding:0!important;font-size:1.6rem!important;}

.pm-brand{display:flex;align-items:center;gap:11px;margin-bottom:4px;}
.pm-logo{width:36px;height:36px;border-radius:10px;display:grid;place-items:center;font-size:18px;background:linear-gradient(135deg,var(--accent),var(--accent2));}
.pm-brand b{display:block;font-size:1.08rem;letter-spacing:-.01em;color:var(--text);}
.pm-brand small{display:block;font:11px var(--mono);color:var(--dim);}
.pm-user{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--border);border-radius:12px;background:rgba(18,26,45,.8);margin-bottom:10px;}
.pm-avatar{width:34px;height:34px;flex:none;border-radius:10px;display:grid;place-items:center;font-weight:700;color:#fff;background:linear-gradient(135deg,var(--accent),var(--accent3));}
.pm-user b{display:block;font-size:.9rem;color:var(--text);}
.pm-user small{color:var(--muted);font-size:.74rem;word-break:break-all;}
</style>
"""
