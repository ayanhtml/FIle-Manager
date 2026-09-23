
"""
File Manager — a Streamlit UI for simple file CRUD operations.
 
Run with:
    pip install streamlit
    streamlit run file_manager_app.py
"""
 
from pathlib import Path
import streamlit as st
 
# ----------------------------- Page setup -----------------------------
st.set_page_config(
    page_title="File Manager",
    page_icon="🗂️",
    layout="centered",
)
 
st.markdown(
    """
    <style>
        .main { padding-top: 1.5rem; }
        .app-title {
            font-size: 2.1rem;
            font-weight: 700;
            margin-bottom: 0;
        }
        .app-subtitle { 
            color: #8a8f98;
            font-size: 1rem;
            margin-top: 0.2rem;
            margin-bottom: 1.5rem;
        }
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
            width: 100%;
        }
        .result-box {
            padding: 0.9rem 1rem;
            border-radius: 8px;
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
 
st.markdown('<p class="app-title">🗂️ File Manager</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle">Create, read, update and delete text files — from a clean UI.</p>',
    unsafe_allow_html=True,
)
 
# ----------------------------- Helpers -----------------------------
def ok(msg: str):
    st.success(msg, icon="✅")
 
def fail(msg: str):
    st.error(msg, icon="⚠️")
 
def info(msg: str):
    st.info(msg, icon="ℹ️")
 
 
# ----------------------------- Tabs -----------------------------
tab_create, tab_read, tab_update, tab_delete = st.tabs(
    ["📄 Create", "🔍 Read", "✏️ Update", "🗑️ Delete"]
)
 
# --- CREATE ---
with tab_create:
    st.subheader("Create a new file")
    filename = st.text_input("File name", placeholder="e.g. notes.txt", key="create_name")
    content = st.text_area("Content", placeholder="What do you want to write?", key="create_content", height=150)
 
    if st.button("Create file", key="create_btn"):
        try:
            if not filename.strip():
                fail("Please enter a file name.")
            else:
                path = Path(filename)
                if path.exists():
                    fail("A file with that name already exists.")
                else:
                    path.write_text(content)
                    ok(f"File **{filename}** created successfully.")
        except Exception as err:
            fail(f"An error occurred: {err}")
 
# --- READ ---
with tab_read:
    st.subheader("Read a file")
    filename = st.text_input("File name", placeholder="e.g. notes.txt", key="read_name")
 
    if st.button("Read file", key="read_btn"):
        try:
            if not filename.strip():
                fail("Please enter a file name.")
            else:
                path = Path(filename)
                if path.exists():
                    file_content = path.read_text()
                    ok(f"Showing contents of **{filename}**")
                    st.code(file_content or "(file is empty)", language=None)
                else:
                    fail("No such file exists.")
        except Exception as err:
            fail(f"An error occurred: {err}")
 
# --- UPDATE ---
with tab_update:
    st.subheader("Update a file")
    filename = st.text_input("File name", placeholder="e.g. notes.txt", key="update_name")
 
    operation = st.radio(
        "Choose an operation",
        ["Rename", "Append content", "Overwrite content"],
        horizontal=False,
        key="update_op",
    )
 
    if operation == "Rename":
        new_name = st.text_input("New file name", key="update_newname")
        if st.button("Rename file", key="rename_btn"):
            try:
                path = Path(filename)
                new_path = Path(new_name)
                if not filename.strip() or not new_name.strip():
                    fail("Please fill in both file names.")
                elif not path.exists():
                    fail("No such file exists.")
                elif new_path.exists():
                    fail("A file with the new name already exists.")
                else:
                    path.rename(new_path)
                    ok(f"Renamed **{filename}** to **{new_name}** successfully.")
            except Exception as err:
                fail(f"An error occurred: {err}")
 
    elif operation == "Append content":
        append_data = st.text_area("Content to append", key="append_data", height=120)
        if st.button("Append", key="append_btn"):
            try:
                path = Path(filename)
                if not filename.strip():
                    fail("Please enter a file name.")
                elif not path.exists():
                    fail("No such file exists.")
                else:
                    with open(path, "a") as fs:
                        fs.write("\n" + append_data)
                    ok(f"Successfully appended to **{filename}**.")
            except Exception as err:
                fail(f"An error occurred: {err}")
 
    elif operation == "Overwrite content":
        overwrite_data = st.text_area("New content (replaces the file)", key="overwrite_data", height=120)
        if st.button("Overwrite", key="overwrite_btn"):
            try:
                path = Path(filename)
                if not filename.strip():
                    fail("Please enter a file name.")
                elif not path.exists():
                    fail("No such file exists.")
                else:
                    path.write_text(overwrite_data)
                    ok(f"Successfully overwrote **{filename}**.")
            except Exception as err:
                fail(f"An error occurred: {err}")
 
# --- DELETE ---
with tab_delete:
    st.subheader("Delete a file")
    filename = st.text_input("File name", placeholder="e.g. notes.txt", key="delete_name")
 
    confirm = st.checkbox("I understand this cannot be undone", key="delete_confirm")
 
    if st.button("Delete file", key="delete_btn", disabled=not confirm):
        try:
            path = Path(filename)
            if not filename.strip():
                fail("Please enter a file name.")
            elif path.exists():
                path.unlink()
                ok(f"File **{filename}** deleted successfully.")
            else:
                fail("No such file exists.")
        except Exception as err:
            fail(f"An error occurred: {err}")
 
st.markdown("---")
st.caption("Built with Python & Streamlit · A simple file management tool")