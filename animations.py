"""Agent animations, pipeline tracker and reusable HTML blocks for Innovexa AI.

Everything here is pure HTML + CSS (no JavaScript), so it keeps animating in the
browser while Python is blocked waiting for the LLM to answer.
"""

import html as _html


def compact(markup):
    """Collapse multi-line HTML into one line.

    Markdown ends an HTML block at the first blank line and treats 4-space
    indents as code, so Streamlit needs the markup on a single line.
    """
    return "".join(line.strip() for line in markup.strip().splitlines())


# ----------------------------------------------------------------------
# Agent catalogue (names match the ones saved in the database)
# ----------------------------------------------------------------------

AGENTS = [
    {
        "key": "advisor", "name": "Project Advisor Agent", "short": "Advisor", "icon": "💡",
        "tagline": "Matches project ideas to your skills and interests",
        "term": "3 ideas matched to your profile",
        "messages": ["Analysing your profile…", "Brainstorming project ideas…", "Ranking the three best fits…"],
    },
    {
        "key": "research", "name": "Research Agent", "short": "Research", "icon": "🔍",
        "tagline": "Finds the problem, existing systems and the research gap",
        "term": "problem + research gap analysis",
        "messages": ["Identifying the real-world problem…", "Reviewing existing systems…", "Looking for research gaps…"],
    },
    {
        "key": "architecture", "name": "Architecture Agent", "short": "Architecture", "icon": "🏗️",
        "tagline": "Designs components, database schema and data flow",
        "term": "components, DB schema, data flow",
        "messages": ["Sketching system components…", "Designing the database schema…", "Mapping the data flow…"],
    },
    {
        "key": "technology", "name": "Technology Recommendation Agent", "short": "Technology", "icon": "⚙️",
        "tagline": "Chooses the right stack for your skill level",
        "term": "final tech stack selected",
        "messages": ["Comparing frameworks…", "Matching tools to your skill level…", "Choosing the final stack…"],
    },
    {
        "key": "planning", "name": "Planning Agent", "short": "Planning", "icon": "🗓️",
        "tagline": "Builds phases, priorities and a week-by-week timeline",
        "term": "phases + weekly timeline",
        "messages": ["Splitting work into phases…", "Estimating the timeline…", "Setting milestones…"],
    },
    {
        "key": "coding", "name": "Coding Agent", "short": "Coding", "icon": "💻",
        "tagline": "Generates a working module with tests",
        "term": "module code + test cases",
        "messages": ["Scaffolding the module…", "Writing the implementation…", "Adding error handling and tests…"],
    },
    {
        "key": "documentation", "name": "Documentation Agent", "short": "Docs", "icon": "📝",
        "tagline": "Drafts the full academic project report",
        "term": "12-section report drafted",
        "messages": ["Drafting the abstract…", "Writing the system design…", "Polishing the report…"],
    },
    {
        "key": "evaluation", "name": "Evaluation Agent", "short": "Evaluation", "icon": "✅",
        "tagline": "Reviews feasibility, risks and project readiness",
        "term": "readiness review",
        "messages": ["Checking technical feasibility…", "Reviewing the architecture…", "Preparing improvement tips…"],
    },
]

ALL_AGENT_NAMES = [a["name"] for a in AGENTS]
PIPELINE_AGENT_NAMES = ALL_AGENT_NAMES[1:]


def get_agent(name):
    for agent in AGENTS:
        if agent["name"] == name:
            return agent
    return {"key": "generic", "name": name, "short": name, "icon": "🤖", "tagline": "", "term": "", "messages": ["Working…"]}


# ----------------------------------------------------------------------
# Animated scenes (one per agent)
# ----------------------------------------------------------------------

_SCENES = {
    "advisor": """
<div class="sc-idea">
<span class="bulb">💡</span>
<div class="cards"><div style="--i:0">Idea 1</div><div style="--i:1">Idea 2</div><div style="--i:2">Idea 3</div></div>
</div>""",
    "research": """
<div class="sc-research">
<div class="doc">
<i style="--w:92%"></i><i style="--w:70%"></i><i style="--w:84%"></i><i style="--w:58%"></i><i style="--w:76%"></i>
<b class="scan"></b>
</div>
<span class="lens">🔍</span>
</div>""",
    "architecture": """
<div class="sc-arch">
<div class="node" style="--i:0">UI</div><span class="link"></span>
<div class="node" style="--i:1">API</div><span class="link"></span>
<div class="node" style="--i:2">AI</div><span class="link"></span>
<div class="node" style="--i:3">DB</div>
<span class="packet"></span>
</div>""",
    "technology": """
<div class="sc-tech">
<div class="gears"><span class="gear g1">⚙️</span><span class="gear g2">⚙️</span></div>
<div class="chips"><em style="--i:0">Python</em><em style="--i:1">SQL</em><em style="--i:2">LLM</em><em style="--i:3">UI</em></div>
</div>""",
    "planning": """
<div class="sc-plan">
<div class="row"><span>P1</span><div class="track"><b style="--i:0;--o:0%;--w:45%"></b></div></div>
<div class="row"><span>P2</span><div class="track"><b style="--i:1;--o:20%;--w:50%"></b></div></div>
<div class="row"><span>P3</span><div class="track"><b style="--i:2;--o:45%;--w:35%"></b></div></div>
<div class="row"><span>P4</span><div class="track"><b style="--i:3;--o:65%;--w:35%"></b></div></div>
</div>""",
    "coding": """
<div class="sc-code">
<div class="bar"><u></u><u></u><u></u><span>module.py</span></div>
<div class="body">
<p style="--i:0"><span class="k">def</span> <span class="f">build_module</span>():</p>
<p style="--i:1">    data = <span class="f">load</span>(spec)</p>
<p style="--i:2">    agent = <span class="f">Agent</span>(data)</p>
<p style="--i:3">    <span class="k">return</span> agent.<span class="f">run</span>()<span class="cur"></span></p>
</div>
</div>""",
    "documentation": """
<div class="sc-doc">
<div class="page">
<i class="h" style="--i:0;--w:60px"></i><i style="--i:1;--w:96px"></i><i style="--i:2;--w:82px"></i><i style="--i:3;--w:90px"></i><i style="--i:4;--w:50px"></i>
</div>
<span class="pen">✏️</span>
</div>""",
    "evaluation": """
<div class="sc-eval">
<div class="it"><span class="bx" style="--i:0"><b>✓</b></span>Feasibility</div>
<div class="it"><span class="bx" style="--i:1"><b>✓</b></span>Architecture</div>
<div class="it"><span class="bx" style="--i:2"><b>✓</b></span>Testing plan</div>
<div class="it"><span class="bx" style="--i:3"><b>✓</b></span>Readiness</div>
</div>""",
}


def agent_working_html(name, index=0, total=8):
    """Big animated 'agent is working' card for the agent called `name`."""
    agent = get_agent(name)
    scene = compact(_SCENES.get(agent["key"], '<span style="font-size:48px">🤖</span>'))
    messages = "".join(
        f'<span class="pm-msg" style="animation-delay:{i * 3}s">{_html.escape(m)}</span>'
        for i, m in enumerate(agent["messages"])
    )
    return compact(f"""
<div class="pm-stage">
<div class="pm-scene">{scene}</div>
<div class="pm-info">
<div class="pm-kicker">AGENT {index + 1:02d} / {total:02d} · RUNNING</div>
<div class="pm-title">{_html.escape(agent['name'])}<span class="pm-dots"><i></i><i></i><i></i></span></div>
<div class="pm-msgs">{messages}</div>
<div class="pm-bar"><div></div></div>
<div class="pm-sub">{_html.escape(agent['tagline'])}</div>
</div>
</div>""")


# ----------------------------------------------------------------------
# Pipeline tracker, agent cards, stage flow, terminal
# ----------------------------------------------------------------------

def pipeline_tracker_html(names, states, durations=None):
    """Row of chips showing every agent as queued / working / done / failed."""
    durations = durations or {}
    total = len(names)
    done = sum(1 for s in states if s == "done")
    pct = int(done / total * 100) if total else 0
    steps = []
    for i, (name, state) in enumerate(zip(names, states)):
        agent = get_agent(name)
        if state == "done":
            icon = "✓"
            meta = f"{durations[name]:.1f}s" if name in durations else "done"
        elif state == "active":
            icon = '<i class="pm-spin"></i>'
            meta = "working…"
        elif state == "error":
            icon = "!"
            meta = "failed"
        else:
            icon = f"{i + 1:02d}"
            meta = "queued"
        steps.append(
            f'<div class="pm-step {state}"><span class="pm-step-ic">{icon}</span>'
            f'<div class="pm-step-tx"><b>{agent["short"]}</b><small>{meta}</small></div></div>'
        )
    return compact(f"""
<div class="pm-track">
<div class="pm-track-head"><span>Agent pipeline</span><em>{done}/{total} complete · {pct}%</em></div>
<div class="pm-track-bar"><div style="width:{pct}%"></div></div>
<div class="pm-steps">{''.join(steps)}</div>
</div>""")


def agent_cards_html():
    cards = "".join(
        f'<div class="pm-agent"><span class="no">{i + 1:02d}</span><div class="ic">{a["icon"]}</div>'
        f'<b>{a["name"]}</b><small>{a["tagline"]}</small></div>'
        for i, a in enumerate(AGENTS)
    )
    return f'<div class="pm-agents">{cards}</div>'


def stage_flow_html(stage):
    labels = ["Profile", "Ideas", "Configure", "Build"]
    items = []
    for i, label in enumerate(labels, start=1):
        if i < stage:
            cls, mark = "done", "✓"
        elif i == stage:
            cls, mark = "active", str(i)
        else:
            cls, mark = "", str(i)
        items.append(f'<div class="pm-flow-item {cls}"><i>{mark}</i>{label}</div>')
    return f'<div class="pm-flow">{"".join(items)}</div>'


def terminal_html(title="pipeline.log", command="innovexa start --agents 8"):
    rows = [f'<p style="--i:0"><span class="cmd">&#36;</span> {_html.escape(command)}</p>']
    for i, agent in enumerate(AGENTS, start=1):
        rows.append(
            f'<p style="--i:{i}"><b class="ok">✓</b> <span class="nm">{agent["short"].lower():<13}</span>'
            f'{_html.escape(agent["term"])}</p>'
        )
    rows.append(
        f'<p style="--i:{len(AGENTS) + 1}"><span class="pm-rot">◐</span> '
        f'<span class="nm">waiting for your idea</span><span class="pm-cur"></span></p>'
    )
    return (
        '<div class="pm-terminal"><div class="pm-term-bar"><u></u><u></u><u></u>'
        f'<span>{_html.escape(title)}</span></div><div class="pm-term-body">{"".join(rows)}</div></div>'
    )


# ----------------------------------------------------------------------
# CSS for the animations above
# ----------------------------------------------------------------------

ANIM_CSS = """
<style>
/* ---- stage card ---- */
.pm-stage{position:relative;overflow:hidden;display:grid;grid-template-columns:210px 1fr;gap:24px;align-items:center;padding:22px 26px;margin:14px 0 18px;border:1px solid var(--border2);border-radius:18px;background:linear-gradient(135deg,rgba(24,34,58,.95),rgba(12,18,33,.95));box-shadow:0 0 0 1px rgba(124,140,255,.08),0 20px 50px rgba(0,0,0,.4);}
.pm-stage::before{content:"";position:absolute;left:0;top:0;width:100%;height:2px;background:linear-gradient(90deg,transparent,var(--accent),var(--accent2),transparent);background-size:200% 100%;animation:pm-sweep 2.2s linear infinite;}
@keyframes pm-sweep{from{background-position:200% 0}to{background-position:-200% 0}}
.pm-scene{height:146px;display:grid;place-items:center;border-radius:14px;background:rgba(7,11,21,.75);border:1px solid var(--border);overflow:hidden;}
.stApp .pm-title{font-size:1.55rem;font-weight:700;color:var(--text);display:flex;align-items:center;flex-wrap:wrap;line-height:1.25;}
.pm-dots{display:inline-flex;margin-left:8px;}
.pm-dots i{display:inline-block;width:6px;height:6px;margin-left:4px;border-radius:50%;background:var(--accent2);animation:pm-dot 1.2s infinite ease-in-out;}
.pm-dots i:nth-child(2){animation-delay:.2s}
.pm-dots i:nth-child(3){animation-delay:.4s}
@keyframes pm-dot{0%,80%,100%{transform:scale(.4);opacity:.4}40%{transform:scale(1);opacity:1}}
.pm-msgs{position:relative;height:24px;margin:10px 0 14px;font:500 13.5px var(--mono);color:var(--accent2);}
.pm-msg{position:absolute;left:0;top:0;opacity:0;white-space:nowrap;animation:pm-msg 9s infinite both;}
@keyframes pm-msg{0%{opacity:0;transform:translateY(8px)}4%{opacity:1;transform:none}29%{opacity:1;transform:none}33%{opacity:0;transform:translateY(-8px)}100%{opacity:0}}
.pm-bar{height:6px;border-radius:99px;background:#1a2440;overflow:hidden;}
.pm-bar div{height:100%;width:40%;border-radius:99px;background:linear-gradient(90deg,var(--accent),var(--accent2));animation:pm-indet 1.5s ease-in-out infinite;}
@keyframes pm-indet{0%{transform:translateX(-110%)}100%{transform:translateX(260%)}}
.pm-sub{margin-top:12px;color:var(--muted);font-size:.9rem;}
@media(max-width:760px){.pm-stage{grid-template-columns:1fr}}

/* ---- tracker ---- */
.pm-track{margin:6px 0 4px;padding:16px 18px;border:1px solid var(--border);border-radius:16px;background:rgba(18,26,45,.8);}
.pm-track-head{display:flex;justify-content:space-between;align-items:center;font:600 11.5px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:10px;}
.pm-track-head em{font-style:normal;color:var(--accent2);}
.pm-track-bar{height:4px;border-radius:99px;background:#1a2440;overflow:hidden;margin-bottom:14px;}
.pm-track-bar div{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width .6s ease;}
.pm-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;}
@media(max-width:900px){.pm-steps{grid-template-columns:repeat(2,1fr)}}
.pm-step{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--border);border-radius:11px;background:rgba(10,14,26,.6);opacity:.55;}
.pm-step-ic{width:28px;height:28px;flex:none;border-radius:8px;display:grid;place-items:center;font:700 11px var(--mono);background:var(--panel2);color:var(--muted);}
.pm-step-tx b{display:block;font-size:.85rem;color:var(--text);}
.pm-step-tx small{font:11px var(--mono);color:var(--dim);}
.pm-step.done{opacity:1;border-color:rgba(52,211,153,.35);}
.pm-step.done .pm-step-ic{background:rgba(52,211,153,.15);color:var(--ok);}
.pm-step.active{opacity:1;border-color:var(--accent);box-shadow:0 0 0 3px rgba(124,140,255,.15);animation:pm-glow 1.6s ease-in-out infinite;}
.pm-step.active .pm-step-tx small{color:var(--accent2);}
.pm-step.error{opacity:1;border-color:rgba(248,113,113,.5);}
.pm-step.error .pm-step-ic{background:rgba(248,113,113,.15);color:var(--err);}
.pm-spin{display:block;width:14px;height:14px;border-radius:50%;border:2px solid rgba(124,140,255,.3);border-top-color:var(--accent);animation:pm-rotate .8s linear infinite;}
@keyframes pm-glow{50%{box-shadow:0 0 0 6px rgba(124,140,255,.06)}}

/* ---- shared pop ---- */
@keyframes pm-pop{0%{transform:scale(0);opacity:0}10%{transform:scale(1.15);opacity:1}18%{transform:scale(1)}85%{transform:scale(1);opacity:1}100%{transform:scale(.9);opacity:0}}

/* ---- advisor ---- */
.sc-idea{display:flex;flex-direction:column;align-items:center;gap:12px;}
.sc-idea .bulb{font-size:44px;line-height:1;animation:pm-bulb 1.8s ease-in-out infinite;}
@keyframes pm-bulb{0%,100%{filter:drop-shadow(0 0 4px rgba(251,191,36,.3));transform:scale(1)}50%{filter:drop-shadow(0 0 18px rgba(251,191,36,.9));transform:scale(1.08)}}
.sc-idea .cards{display:flex;gap:7px;}
.sc-idea .cards div{font:600 10px var(--mono);padding:6px 9px;border-radius:8px;background:var(--panel2);border:1px solid var(--border2);color:#b7c1ff;animation:pm-pop 4s ease-in-out infinite;animation-delay:calc(var(--i)*.5s);}

/* ---- research ---- */
.sc-research{position:relative;width:150px;height:122px;}
.sc-research .doc{position:absolute;inset:4px 20px 4px 4px;padding:14px 12px;display:flex;flex-direction:column;gap:9px;overflow:hidden;border-radius:10px;background:var(--panel2);border:1px solid var(--border2);}
.sc-research .doc i{display:block;height:6px;width:var(--w);border-radius:4px;background:#2c3a60;}
.sc-research .scan{position:absolute;left:0;right:0;top:-30px;height:30px;background:linear-gradient(180deg,transparent,rgba(34,211,182,.4),transparent);animation:pm-scan 2.4s ease-in-out infinite;}
@keyframes pm-scan{to{top:100%}}
.sc-research .lens{position:absolute;left:8px;top:8px;font-size:36px;line-height:1;filter:drop-shadow(0 5px 8px rgba(0,0,0,.55));animation:pm-lens 4.5s ease-in-out infinite;}
@keyframes pm-lens{0%,100%{transform:translate(0,0)}25%{transform:translate(78px,8px)}50%{transform:translate(24px,52px)}75%{transform:translate(84px,62px)}}

/* ---- architecture ---- */
.sc-arch{position:relative;display:flex;align-items:center;width:178px;}
.sc-arch .node{width:34px;height:34px;flex:none;display:grid;place-items:center;border-radius:9px;font:700 10px var(--mono);color:#dfe5ff;background:linear-gradient(135deg,#34408f,#27306b);border:1px solid #4b5bd0;animation:pm-pop 4s ease-in-out infinite;animation-delay:calc(var(--i)*.35s);}
.sc-arch .link{flex:none;width:15px;height:2px;background:repeating-linear-gradient(90deg,#4b5bd0 0 4px,transparent 4px 7px);}
.sc-arch .packet{position:absolute;left:0;top:50%;width:8px;height:8px;margin-top:-4px;border-radius:50%;background:var(--accent2);box-shadow:0 0 12px var(--accent2);animation:pm-packet 2.4s linear infinite;}
@keyframes pm-packet{from{left:0}to{left:calc(100% - 8px)}}

/* ---- technology ---- */
.sc-tech{display:flex;flex-direction:column;align-items:center;gap:10px;}
.sc-tech .gears{position:relative;width:110px;height:66px;}
.sc-tech .gear{position:absolute;line-height:1;}
.sc-tech .g1{left:8px;top:2px;font-size:54px;animation:pm-rotate 6s linear infinite;}
.sc-tech .g2{left:58px;top:26px;font-size:38px;animation:pm-rotate 4s linear infinite reverse;}
.sc-tech .chips{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;max-width:180px;}
.sc-tech .chips em{font:600 10px var(--mono);font-style:normal;padding:3px 8px;border-radius:6px;background:rgba(34,211,182,.12);border:1px solid rgba(34,211,182,.4);color:#7ff0da;animation:pm-chip 4s ease-in-out infinite;animation-delay:calc(var(--i)*.5s);}
@keyframes pm-chip{0%{opacity:0;transform:translateY(8px)}12%{opacity:1;transform:none}85%{opacity:1}100%{opacity:0}}

/* ---- planning ---- */
.sc-plan{width:178px;display:flex;flex-direction:column;gap:12px;}
.sc-plan .row{display:flex;align-items:center;gap:8px;}
.sc-plan .row span{width:22px;font:600 10px var(--mono);color:var(--muted);}
.sc-plan .track{flex:1;height:12px;border-radius:6px;background:#1a2440;position:relative;}
.sc-plan .track b{position:absolute;left:var(--o);top:0;height:100%;width:0;border-radius:6px;background:linear-gradient(90deg,var(--accent),var(--accent2));animation:pm-gantt 5s ease-in-out infinite;animation-delay:calc(var(--i)*.55s);}
@keyframes pm-gantt{0%{width:0;opacity:1}35%{width:var(--w)}85%{width:var(--w);opacity:1}100%{width:var(--w);opacity:0}}

/* ---- coding ---- */
.sc-code{width:192px;border-radius:10px;overflow:hidden;border:1px solid var(--border2);background:#070b15;}
.sc-code .bar{display:flex;align-items:center;gap:5px;padding:7px 9px;background:#0d1424;border-bottom:1px solid var(--border);}
.sc-code .bar u{width:7px;height:7px;border-radius:50%;background:#ff5f57;text-decoration:none;display:inline-block;}
.sc-code .bar u:nth-child(2){background:#febc2e}
.sc-code .bar u:nth-child(3){background:#28c840}
.sc-code .bar span{margin-left:6px;font:10px var(--mono);color:var(--dim);}
.sc-code .body{padding:9px 10px;height:84px;}
.sc-code .body p{margin:0 0 4px;white-space:pre;overflow:hidden;width:0;font:10.5px/1.4 var(--mono);color:#c3cce0;animation:pm-type 6s steps(22,end) infinite;animation-delay:calc(var(--i)*.9s);}
.sc-code .k{color:#c084fc}
.sc-code .f{color:#7dd3fc}
.sc-code .cur{display:inline-block;width:6px;height:11px;background:var(--accent2);vertical-align:-2px;animation:pm-blink 1s steps(1) infinite;}
@keyframes pm-type{0%{width:0}14%{width:100%}88%{width:100%}100%{width:0}}

/* ---- documentation ---- */
.sc-doc{position:relative;width:150px;height:126px;}
.sc-doc .page{position:absolute;left:10px;top:2px;width:118px;height:118px;border-radius:8px;background:#f2f5ff;box-shadow:0 10px 24px rgba(0,0,0,.45);padding:14px 11px;}
.sc-doc .page i{display:block;height:5px;margin-bottom:9px;width:0;border-radius:3px;background:#c3cbea;animation:pm-write 5s ease-out infinite;animation-delay:calc(var(--i)*1s);}
.sc-doc .page i.h{background:#7c8cff;height:7px;}
@keyframes pm-write{0%{width:0;opacity:1}16%{width:var(--w)}88%{width:var(--w);opacity:1}100%{width:var(--w);opacity:0}}
.sc-doc .pen{position:absolute;left:10px;top:10px;font-size:26px;line-height:1;filter:drop-shadow(0 3px 4px rgba(0,0,0,.5));animation:pm-pen 5s linear infinite;}
@keyframes pm-pen{
0%{transform:translate(8px,-14px)}16%{transform:translate(68px,-14px)}
20%{transform:translate(8px,2px)}36%{transform:translate(104px,2px)}
40%{transform:translate(8px,16px)}56%{transform:translate(90px,16px)}
60%{transform:translate(8px,30px)}76%{transform:translate(98px,30px)}
80%{transform:translate(8px,44px)}96%{transform:translate(58px,44px)}
100%{transform:translate(8px,-14px)}}

/* ---- evaluation ---- */
.sc-eval{width:178px;display:flex;flex-direction:column;gap:10px;}
.sc-eval .it{display:flex;align-items:center;gap:10px;font:500 11.5px var(--mono);color:var(--muted);}
.sc-eval .bx{width:18px;height:18px;flex:none;border-radius:5px;border:1.5px solid var(--border2);display:grid;place-items:center;animation:pm-box 5s infinite;animation-delay:calc(var(--i)*1s);}
.sc-eval .bx b{font-size:11px;color:var(--ok);opacity:0;animation:pm-tick 5s infinite;animation-delay:calc(var(--i)*1s);}
@keyframes pm-tick{0%{opacity:0;transform:scale(0)}8%{opacity:1;transform:scale(1.4)}14%{transform:scale(1)}88%{opacity:1}100%{opacity:0}}
@keyframes pm-box{0%{border-color:var(--border2);background:transparent}8%,88%{border-color:var(--ok);background:rgba(52,211,153,.12)}100%{border-color:var(--border2);background:transparent}}
</style>
"""
