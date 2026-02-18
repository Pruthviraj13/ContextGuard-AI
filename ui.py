import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/api/v1"


# ---- JWT TOKEN ----
st.set_page_config(page_title="RAG Tester", layout="centered")
st.title("🔐 RAG System Login")
if "token" not in st.session_state:
    st.session_state.token = None

username = st.text_input("Username")

if st.button("Login"):
    if not username:
        st.error("Username required")
    else:
        resp = requests.post(
            f"{BACKEND_URL}/auth/login",
            params={"username": username}
        )

        if resp.status_code == 200:
            st.session_state.token = resp.json()["access_token"]
            st.success("Logged in successfully")
        else:
            st.error("Login failed")

def auth_headers():
    if st.session_state.token:
        return {
            "Authorization": f"Bearer {st.session_state.token}"
        }
    return {}

# ---- INGEST ----
st.subheader("📄 Upload Document")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
if not st.session_state.token:
    st.warning("Please login to continue")
    st.stop()
if st.button("Ingest Document"):
    if not uploaded_file:
        st.error("Please upload a file")
    else:
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue())
        }
        resp = requests.post(
            f"{BACKEND_URL}/ingest",
            files=files,
            headers=auth_headers()
        )

        if resp.status_code == 200:
            st.success(f"Ingested {resp.json()['chunks_ingested']} chunks")
        else:
            st.error(resp.text)

# ---- QUERY ----
st.subheader("❓ Ask a Question")

question = st.text_area("Enter your question")

if st.button("Ask"):

    if not question:
        st.error("Please enter a question")
    else:
        payload = {"question": question}
        resp = requests.post(
            f"{BACKEND_URL}/query",
            json=payload,
            headers=auth_headers()
        )

        if resp.status_code == 200:
            data = resp.json()
            st.markdown("### ✅ Answer")
            st.write(data["answer"])

            st.markdown("### 📊 Confidence")
            st.progress(data["confidence"])

            st.markdown("### 📚 Sources")
            st.write(data["sources"])
        else:
            st.error(resp.text)
