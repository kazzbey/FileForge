"""
FileForge — a beautiful Streamlit UI for a Python file handling project.
Create, read, update (rename / append / overwrite) and delete text files.

Run with:
    pip install -r requirements.txt
    streamlit run app.py
"""

from datetime import datetime
from html import escape
from pathlib import Path

import streamlit as st

# ─────────────────────────────────────────────────────────────
# Page setup
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FileForge · Python File Manager",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# All files live inside this folder so the app never touches anything else.
WORKSPACE = Path(__file__).parent / "workspace"
WORKSPACE.mkdir(exist_ok=True)


# ─────────────────────────────────────────────────────────────
# Styling
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg: #0b1016;
  --panel: rgba(255,255,255,0.035);
  --panel-strong: rgba(255,255,255,0.06);
  --line: rgba(255,255,255,0.08);
  --text: #e8edf2;
  --muted: #8b98a8;
  --accent: #2ee6a8;
  --accent-2: #ffb547;
  --danger: #ff5d6c;
}

html, body, [class*="css"], .stMarkdown, .stTextInput, .stTextArea, button, input, textarea, select {
  font-family: 'Space Grotesk', sans-serif !important;
}

.stApp {
  background:
    radial-gradient(900px 500px at 8% -10%, rgba(46,230,168,0.16), transparent 60%),
    radial-gradient(800px 500px at 100% 0%, rgba(255,181,71,0.12), transparent 55%),
    var(--bg);
  color: var(--text);
}

header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1300px; }

/* Sidebar */
section[data-testid="stSidebar"] {
  background: rgba(8,12,17,0.85);
  border-right: 1px solid var(--line);
}
.brand { display:flex; align-items:center; gap:.7rem; margin-bottom: 1.2rem; }
.brand-logo {
  width: 42px; height: 42px; border-radius: 12px;
  display:grid; place-items:center; font-size: 1.3rem;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  box-shadow: 0 8px 24px -8px rgba(46,230,168,.6);
}
.brand-name { font-size: 1.25rem; font-weight: 700; letter-spacing: -.02em; color: var(--text); }
.brand-sub { font-size: .75rem; color: var(--muted); margin-top: -2px; }
.side-card {
  background: var(--panel); border: 1px solid var(--line);
  border-radius: 14px; padding: .9rem 1rem; margin: .6rem 0; font-size: .86rem; color: var(--muted);
}
.side-card b { color: var(--text); }
.side-card code { color: var(--accent); background: transparent; }

/* Hero */
.hero {
  position: relative; overflow: hidden;
  border: 1px solid var(--line); border-radius: 22px;
  padding: 2rem 2.2rem; margin-bottom: 1.4rem;
  background: linear-gradient(135deg, rgba(46,230,168,0.08), rgba(255,181,71,0.05) 60%, rgba(255,255,255,0.02));
}
.hero::after {
  content: ""; position: absolute; right: -60px; top: -60px; width: 260px; height: 260px;
  border-radius: 50%; border: 1px dashed rgba(46,230,168,.35);
}
.pill {
  display:inline-flex; align-items:center; gap:.4rem;
  font-size:.72rem; letter-spacing:.12em; text-transform:uppercase; font-weight:600;
  color: var(--accent); border: 1px solid rgba(46,230,168,.35); background: rgba(46,230,168,.08);
  padding: .3rem .7rem; border-radius: 999px;
}
.hero h1 {
  font-size: 2.7rem; line-height: 1.05; font-weight: 700; letter-spacing: -.035em;
  margin: .8rem 0 .4rem; color: var(--text);
}
.hero h1 span {
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.hero p { color: var(--muted); font-size: 1.02rem; max-width: 620px; margin: 0; }
.ops { display:flex; gap:.5rem; margin-top: 1.1rem; flex-wrap: wrap; }
.op {
  font-family: 'JetBrains Mono', monospace; font-size: .78rem; color: var(--text);
  background: var(--panel-strong); border: 1px solid var(--line); padding: .35rem .7rem; border-radius: 8px;
}

/* Stat cards */
.stat {
  background: var(--panel); border: 1px solid var(--line); border-radius: 18px;
  padding: 1.1rem 1.2rem; height: 100%;
}
.stat-label { color: var(--muted); font-size: .78rem; text-transform: uppercase; letter-spacing: .1em; }
.stat-value { font-size: 1.9rem; font-weight: 700; letter-spacing: -.03em; margin-top: .25rem; color: var(--text); }
.stat-hint { color: var(--muted); font-size: .8rem; margin-top: .1rem; }
.stat-accent .stat-value { color: var(--accent); }
.stat-amber .stat-value { color: var(--accent-2); }

/* Panels */
.panel-title { font-size: 1.15rem; font-weight: 600; margin: 0 0 .2rem; color: var(--text); }
.panel-sub { color: var(--muted); font-size: .88rem; margin-bottom: .8rem; }

div[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--panel); border-color: var(--line) !important; border-radius: 20px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  gap: .4rem; background: rgba(255,255,255,.03); padding: .35rem; border-radius: 14px; border: 1px solid var(--line);
}
.stTabs [data-baseweb="tab"] {
  height: 42px; padding: 0 1.1rem; border-radius: 10px; color: var(--muted); font-weight: 600;
}
.stTabs [aria-selected="true"] { background: rgba(46,230,168,.12) !important; color: var(--accent) !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

/* Inputs */
.stTextInput input, .stTextArea textarea, div[data-baseweb="select"] > div {
  background: rgba(0,0,0,.25) !important; border: 1px solid var(--line) !important;
  border-radius: 12px !important; color: var(--text) !important;
}
.stTextArea textarea { font-family: 'JetBrains Mono', monospace !important; font-size: .9rem; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color: var(--accent) !important; }
label, .stMarkdown p { color: var(--text); }

/* Buttons */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
  border-radius: 12px; font-weight: 600; padding: .55rem 1.2rem; border: 1px solid var(--line);
  background: var(--panel-strong); color: var(--text); transition: all .18s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
  border-color: var(--accent); color: var(--accent); transform: translateY(-1px);
}
.stButton > button[kind^="primary"], .stFormSubmitButton > button[kind^="primary"] {
  background: linear-gradient(135deg, var(--accent), #1fc48d) !important; border: none !important;
  box-shadow: 0 10px 24px -10px rgba(46,230,168,.7);
}
.stButton > button[kind^="primary"] *, .stFormSubmitButton > button[kind^="primary"] *,
.stButton > button[kind^="primary"], .stFormSubmitButton > button[kind^="primary"] { color: #04140e !important; }
.stButton > button[kind^="primary"]:hover, .stFormSubmitButton > button[kind^="primary"]:hover { filter: brightness(1.08); }
.st-key-danger_zone .stButton > button[kind^="primary"] {
  background: linear-gradient(135deg, var(--danger), #e0404f) !important; box-shadow: 0 10px 24px -10px rgba(255,93,108,.7);
}
.st-key-danger_zone .stButton > button[kind^="primary"], .st-key-danger_zone .stButton > button[kind^="primary"] * { color: #fff !important; }
.stButton > button:disabled { opacity: .45; }

/* File explorer */
.file-row {
  display:flex; align-items:center; gap:.85rem; padding:.75rem .85rem; margin-bottom:.5rem;
  border-radius: 14px; border: 1px solid var(--line); background: rgba(0,0,0,.18);
  transition: all .15s ease;
}
.file-row:hover { border-color: rgba(46,230,168,.4); background: rgba(46,230,168,.05); }
.file-icon {
  width: 38px; height: 38px; border-radius: 10px; display:grid; place-items:center;
  font-family: 'JetBrains Mono', monospace; font-size: .62rem; font-weight: 600; letter-spacing: .04em;
  color: #04140e; background: var(--accent); flex-shrink: 0;
}
.file-icon.amber { background: var(--accent-2); }
.file-icon.gray { background: #9aa7b6; }
.file-name { font-weight: 600; color: var(--text); font-size: .93rem; word-break: break-all; }
.file-meta { color: var(--muted); font-size: .76rem; font-family: 'JetBrains Mono', monospace; }
.empty {
  text-align:center; padding: 2.2rem 1rem; color: var(--muted);
  border: 1px dashed var(--line); border-radius: 16px;
}
.empty .big { font-size: 2rem; }

/* Code viewer */
.stCode, pre { border-radius: 14px !important; }
.viewer-head {
  display:flex; justify-content:space-between; align-items:center;
  font-family:'JetBrains Mono', monospace; font-size:.8rem; color: var(--muted); margin: .6rem 0 .3rem;
}
.footer { text-align:center; color: var(--muted); font-size:.8rem; margin-top: 2.5rem; }
.footer b { color: var(--accent); }
</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────
# File handling logic (same operations as the original script)
# ─────────────────────────────────────────────────────────────
def resolve(filename: str) -> Path:
    name = (filename or "").strip()
    if not name:
        raise ValueError("Please enter a file name.")
    path = (WORKSPACE / name).resolve()
    if WORKSPACE.resolve() not in path.parents:
        raise ValueError("The file must stay inside the workspace folder.")
    return path


def create_file(filename: str, data: str):
    path = resolve(filename)
    if path.exists():
        return False, f"File '{filename}' already exists."
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    return True, f"File '{filename}' created successfully."


def read_file(filename: str) -> str:
    path = resolve(filename)
    if not path.exists():
        raise FileNotFoundError(f"File '{filename}' does not exist.")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def rename_file(filename: str, new_name: str):
    path, new_path = resolve(filename), resolve(new_name)
    if not path.exists():
        return False, f"File '{filename}' does not exist."
    if new_path.exists():
        return False, f"File '{new_name}' already exists. Please choose a different name."
    path.rename(new_path)
    return True, f"File renamed to '{new_name}'."


def append_file(filename: str, data: str):
    path = resolve(filename)
    if not path.exists():
        return False, f"File '{filename}' does not exist."
    with open(path, "a", encoding="utf-8") as f:
        f.write(data)
    return True, f"Data appended to '{filename}'."


def overwrite_file(filename: str, data: str):
    path = resolve(filename)
    if not path.exists():
        return False, f"File '{filename}' does not exist."
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    return True, f"File '{filename}' overwritten successfully."


def delete_file(filename: str):
    path = resolve(filename)
    if not path.exists():
        return False, f"File '{filename}' does not exist."
    path.unlink()
    return True, f"File '{filename}' deleted successfully."


def list_files():
    files = [p for p in WORKSPACE.rglob("*") if p.is_file()]
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)


def human_size(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def time_ago(ts: float) -> str:
    secs = int(datetime.now().timestamp() - ts)
    if secs < 60:
        return "just now"
    if secs < 3600:
        return f"{secs // 60} min ago"
    if secs < 86400:
        return f"{secs // 3600} h ago"
    return datetime.fromtimestamp(ts).strftime("%d %b %Y")


def run(action, *args):
    """Run an action, show a toast, and refresh the page on success."""
    try:
        ok, msg = action(*args)
    except Exception as e:  # mirrors the try/except in the original script
        ok, msg = False, f"An error occurred: {e}"
    if ok:
        st.session_state["flash"] = ("success", msg)
        st.rerun()
    else:
        st.error(msg, icon="⚠️")


def rel(p: Path) -> str:
    return str(p.relative_to(WORKSPACE))


# Show messages from the previous action
if "flash" in st.session_state:
    kind, msg = st.session_state.pop("flash")
    st.toast(msg, icon="✅" if kind == "success" else "⚠️")


# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
<div class="brand">
  <div class="brand-logo">🗂️</div>
  <div><div class="brand-name">FileForge</div><div class="brand-sub">Python file handling, visualised</div></div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="side-card"><b>How it works</b><br/>
Every operation from the original CLI script — <code>create</code>, <code>read</code>,
<code>update</code> and <code>delete</code> — now has its own screen.</div>
<div class="side-card"><b>Built with</b><br/>
<code>pathlib.Path</code> · <code>open()</code> · <code>Path.rename()</code> · <code>Path.unlink()</code> · Streamlit</div>
""",
        unsafe_allow_html=True,
    )
    if st.button("✨ Load sample files", use_container_width=True):
        samples = {
            "notes.txt": "Learning Python file handling 🐍\n- open() modes: r, w, a\n- pathlib makes paths easy\n",
            "todo.md": "# Today\n- [x] Build CLI file manager\n- [x] Give it a Streamlit UI\n- [ ] Post it on LinkedIn\n",
            "config.json": '{\n  "app": "FileForge",\n  "version": "1.0",\n  "theme": "dark"\n}\n',
            "hello.py": 'print("Hello from FileForge!")\n',
        }
        for name, body in samples.items():
            p = WORKSPACE / name
            if not p.exists():
                p.write_text(body, encoding="utf-8")
        st.session_state["flash"] = ("success", "Sample files added to your workspace.")
        st.rerun()
    st.markdown(
        f'<div class="side-card">📁 Workspace<br/><code>{escape(WORKSPACE.name)}/</code></div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
# Hero + stats
# ─────────────────────────────────────────────────────────────
files = list_files()
names = [rel(p) for p in files]
total_size = sum(p.stat().st_size for p in files)
total_lines = 0
for p in files:
    try:
        total_lines += p.read_text(encoding="utf-8", errors="ignore").count("\n") + 1
    except Exception:
        pass
last_edit = time_ago(files[0].stat().st_mtime) if files else "—"

st.markdown(
    """
<div class="hero">
  <span class="pill">● Python · pathlib · Streamlit</span>
  <h1>Manage files with <span>pure Python</span>.</h1>
  <p>A clean dashboard on top of a classic CLI file handler. Create, read, rename, append,
  overwrite and delete files — all in one place.</p>
  <div class="ops">
    <span class="op">open(path, 'w')</span><span class="op">open(path, 'r')</span>
    <span class="op">open(path, 'a')</span><span class="op">path.rename()</span><span class="op">path.unlink()</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
stats = [
    (c1, "stat-accent", "Files", str(len(files)), "in your workspace"),
    (c2, "", "Total size", human_size(total_size), "on disk"),
    (c3, "stat-amber", "Lines", f"{total_lines:,}", "of text written"),
    (c4, "", "Last edit", last_edit, files[0].name if files else "no files yet"),
]
for col, cls, label, value, hint in stats:
    col.markdown(
        f'<div class="stat {cls}"><div class="stat-label">{label}</div>'
        f'<div class="stat-value">{escape(value)}</div><div class="stat-hint">{escape(hint)}</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# ─────────────────────────────────────────────────────────────
# Main area: operations + explorer
# ─────────────────────────────────────────────────────────────
left, right = st.columns([1.6, 1], gap="large")

with left:
    with st.container(border=True):
        tab_create, tab_read, tab_update, tab_delete = st.tabs(
            ["＋  Create", "👁  Read", "✎  Update", "🗑  Delete"]
        )

        # CREATE
        with tab_create:
            st.markdown('<div class="panel-title">Create a new file</div>'
                        '<div class="panel-sub">Give it a name and write something inside.</div>',
                        unsafe_allow_html=True)
            with st.form("create_form", clear_on_submit=True, border=False):
                filename = st.text_input("File name", placeholder="e.g. notes.txt")
                data = st.text_area("What do you want to write in the file?", height=180,
                                    placeholder="Start typing…")
                if st.form_submit_button("Create file", type="primary"):
                    run(create_file, filename, data)

        # READ
        with tab_read:
            st.markdown('<div class="panel-title">Read a file</div>'
                        '<div class="panel-sub">Preview the contents of any file in your workspace.</div>',
                        unsafe_allow_html=True)
            if not names:
                st.info("No files yet — create one first or load the sample files.", icon="📭")
            else:
                choice = st.selectbox("Choose a file", names, key="read_choice")
                try:
                    content = read_file(choice)
                    p = resolve(choice)
                    st.markdown(
                        f'<div class="viewer-head"><span>📄 {escape(choice)}</span>'
                        f'<span>{human_size(p.stat().st_size)} · {content.count(chr(10)) + 1} lines</span></div>',
                        unsafe_allow_html=True,
                    )
                    ext = p.suffix.lstrip(".").lower()
                    lang = {"py": "python", "md": "markdown", "json": "json", "js": "javascript",
                            "html": "html", "css": "css", "csv": "text"}.get(ext, "text")
                    st.code(content or "(empty file)", language=lang)
                    st.download_button("⬇ Download", content, file_name=p.name)
                except Exception as e:
                    st.error(f"An error occurred while reading the file: {e}")

        # UPDATE
        with tab_update:
            st.markdown('<div class="panel-title">Update a file</div>'
                        '<div class="panel-sub">Rename it, append new data, or overwrite everything.</div>',
                        unsafe_allow_html=True)
            if not names:
                st.info("No files to update yet.", icon="📭")
            else:
                target = st.selectbox("Choose a file", names, key="update_choice")
                op = st.segmented_control(
                    "Operation",
                    ["✏️ Rename", "➕ Append", "♻️ Overwrite"],
                    default="➕ Append",
                    key="update_op",
                ) or "➕ Append"

                with st.form("update_form", clear_on_submit=True, border=False):
                    if op.endswith("Rename"):
                        new_name = st.text_input("New name for the file", placeholder="e.g. renamed.txt")
                        if st.form_submit_button("Rename file", type="primary"):
                            run(rename_file, target, new_name)
                    elif op.endswith("Append"):
                        data = st.text_area("Data to append", height=150, placeholder="This goes at the end…")
                        if st.form_submit_button("Append data", type="primary"):
                            run(append_file, target, data)
                    else:
                        current = ""
                        try:
                            current = read_file(target)
                        except Exception:
                            pass
                        data = st.text_area("New content (replaces everything)", value=current, height=180)
                        if st.form_submit_button("Overwrite file", type="primary"):
                            run(overwrite_file, target, data)

        # DELETE
        with tab_delete:
            st.markdown('<div class="panel-title">Delete a file</div>'
                        '<div class="panel-sub">This permanently removes the file from disk.</div>',
                        unsafe_allow_html=True)
            if not names:
                st.info("Nothing to delete — your workspace is empty.", icon="🧹")
            else:
                target = st.selectbox("Choose a file", names, key="delete_choice")
                sure = st.checkbox(f"Yes, I want to delete **{target}**")
                with st.container(key="danger_zone"):
                    if st.button("Delete file", type="primary", disabled=not sure):
                        run(delete_file, target)

with right:
    with st.container(border=True):
        st.markdown('<div class="panel-title">📁 File explorer</div>'
                    f'<div class="panel-sub">{len(files)} file{"s" if len(files) != 1 else ""} · sorted by last modified</div>',
                    unsafe_allow_html=True)
        if not files:
            st.markdown(
                '<div class="empty"><div class="big">🗂️</div>Your workspace is empty.<br/>'
                'Create a file or load the samples from the sidebar.</div>',
                unsafe_allow_html=True,
            )
        else:
            rows = []
            for p in files[:12]:
                ext = (p.suffix.lstrip(".") or "file")[:4].upper()
                color = "" if ext in {"TXT", "MD"} else "amber" if ext in {"PY", "JSON", "JS"} else "gray"
                s = p.stat()
                rows.append(
                    f'<div class="file-row"><div class="file-icon {color}">{escape(ext)}</div>'
                    f'<div><div class="file-name">{escape(rel(p))}</div>'
                    f'<div class="file-meta">{human_size(s.st_size)} · {time_ago(s.st_mtime)}</div></div></div>'
                )
            st.markdown("".join(rows), unsafe_allow_html=True)
            if len(files) > 12:
                st.caption(f"+ {len(files) - 12} more files")

st.markdown(
    '<div class="footer">Built with <b>Python</b> & <b>Streamlit</b> · FileForge</div>',
    unsafe_allow_html=True,
)
