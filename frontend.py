import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/query"


st.set_page_config(
    page_title="Personal Email Assistant",
    layout="centered"
)


st.markdown(
    """
    <h1 style="margin-bottom:0.2rem;">📧 Personal Email Assistant</h1>
    <p style="color:#6b7280; margin-top:0;">
        Ask questions about your personal emails using a local RAG system
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


st.markdown("### Query")

user_id = st.text_input(
    "User ID",
    value="user1",
    help="Used for strict per-user data isolation"
)

question = st.text_area(
    "Your question",
    placeholder="e.g. What interviews or deadlines do I have coming up?",
    height=90
)

top_k = st.slider(
    "Emails to retrieve",
    min_value=1,
    max_value=10,
    value=5
)


ask_clicked = st.button("Ask", type="primary")


if ask_clicked:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching your emails…"):
            try:
                response = requests.post(
                    API_URL,
                    headers={"X-User-Id": user_id},
                    json={
                        "question": question,
                        "top_k": top_k
                    },
                    timeout=180
                )
            except requests.exceptions.RequestException as e:
                st.error("Could not connect to the backend service.")
                st.code(str(e))
                st.stop()

        if response.status_code != 200:
            st.error("The backend returned an error.")
            st.code(response.text)
            st.stop()

        data = response.json()

        
        st.divider()
        st.markdown("### Answer")

        answer_text = data.get("answer", "")
        if answer_text:
            st.write(answer_text)
        else:
            st.info("No answer was generated.")

       
        sources = data.get("sources", [])

        st.divider()
        st.markdown(
            "<span style='color:#6b7280; font-weight:600;'>Retrieved emails</span>",
            unsafe_allow_html=True
        )

        if not sources:
            st.markdown(
                "<p style='color:#6b7280;'>No source emails were used.</p>",
                unsafe_allow_html=True
            )
        else:
            for i, src in enumerate(sources, 1):
                header = (
                    f"{i}. {src['subject']} "
                    f"<span style='color:#6b7280;'>"
                    f"(similarity: {round(src.get('similarity', 0), 3)})"
                    f"</span>"
                )

                with st.expander(header, expanded=False):
                    st.markdown(
                        f"""
                        <div style="line-height:1.6;">
                            <strong>From:</strong> {src['sender']}<br/>
                            <strong>Date:</strong> {src['timestamp']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
