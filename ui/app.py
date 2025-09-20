import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG Chat", page_icon="🤖", layout="centered")

# --- Header ---
st.markdown("<h1 style='text-align: center;'>🤖 RAG Chat</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Ask questions directly about your uploaded documents</p>", unsafe_allow_html=True)

# --- Chat state ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Display chat history (no sources shown) ---
for role, content, _ in st.session_state["messages"]:
    with st.chat_message(role):
        st.markdown(content)

# --- Chat input with placeholder ---
query = st.text_input(
    label="",
    placeholder="💬 Write your question here...",
    key="chatbox"
)

# --- Upload icon just below input ---
uploaded_file = st.file_uploader("📂", type=["txt", "pdf"], label_visibility="collapsed")
if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    resp = requests.post(f"{API_URL}/api/v1/upload/", files=files)
    if resp.status_code == 200:
        ingest_resp = requests.post(f"{API_URL}/api/v1/ingest/", json={"folder_path": "data/uploads"})
        if ingest_resp.status_code == 200:
            data = ingest_resp.json()
            st.toast(f"✅ {uploaded_file.name} uploaded & ingested")
        else:
            st.toast("⚠️ Upload ok, ingest failed")
    else:
        st.toast("❌ Upload failed")

# --- Process user query ---
if query:
    st.chat_message("user").markdown(query)
    st.session_state["messages"].append(("user", query, None))

    resp = requests.post(f"{API_URL}/api/v1/ask/", json={"query": query})
    if resp.status_code == 200:
        data = resp.json()
        answer = data["answer"]
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state["messages"].append(("assistant", answer, None))
    else:
        with st.chat_message("assistant"):
            st.error("⚠️ Error from backend")
