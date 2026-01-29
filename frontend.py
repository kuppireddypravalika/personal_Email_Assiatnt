import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="Personal Email RAG", layout="centered")
st.title("📧 Personal Email Assistant")

user_id = st.text_input("User ID", value="user1")
question = st.text_area("Ask a question about your emails")

top_k = st.slider("Number of emails to retrieve", 1, 10, 5)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            resp = requests.post(
                API_URL,
                headers={"X-User-Id": user_id},
                json={
                    "question": question,
                    "top_k": top_k
                },
                timeout=180
            )

            data = resp.json()

            if "answer" in data:
                st.subheader("Answer")
                st.write(data["answer"])

                st.subheader("Sources")
                for s in data.get("sources", []):
                    st.write(
                        f"- **{s['subject']}** from {s['sender']} ({s['timestamp']})"
                    )
            else:
                st.error("Error")
                st.code(data)
