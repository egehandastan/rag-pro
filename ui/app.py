import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG Pro", layout="centered")
st.title("📚 RAG Pro — Simple UI")

# --- Upload section ---
st.header("0. Upload a TXT File")
uploaded_file = st.file_uploader("Choose a TXT file", type=["txt"])

uploaded_filename = None
if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    try:
        resp = requests.post(f"{API_URL}/api/v1/upload/", files=files)
        if resp.status_code == 200:
            data = resp.json()
            uploaded_filename = data["filename"]
            st.success(f"Uploaded file: {data['filename']}")
            st.info(f"Saved to server: {data['path']}")
        else:
            st.error(f"Error: {resp.text}")
    except Exception as e:
        st.error(f"Upload failed: {e}")

# --- Ingest section ---
#st.header("1. Ingest Uploaded File(s)")
if st.button("Ingest Uploaded Files"):
    try:
        resp = requests.post(f"{API_URL}/api/v1/ingest/", json={"folder_path": "data/uploads"})
        if resp.status_code == 200:
            data = resp.json()
            st.success(f"Ingested {data['processed_docs']} docs, {data['chunks_indexed']} chunks indexed.")
        else:
            st.error(f"Error: {resp.text}")
    except Exception as e:
        st.error(f"Ingest failed: {e}")

# --- Ask section ---
st.header("2. Ask a Question")
query = st.text_input("Enter your question:")

if st.button("Ask"):
    if not query:
        st.warning("Please enter a question.")
    else:
        try:
            resp = requests.post(f"{API_URL}/api/v1/ask/", json={"query": query})
            if resp.status_code == 200:
                data = resp.json()
                st.subheader("Answer")
                st.write(data["answer"])
                st.subheader("Sources")
                st.write(", ".join(data["sources"]))
            else:
                st.error(f"Error: {resp.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
