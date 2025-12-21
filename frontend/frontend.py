import streamlit as st
import requests
from PIL import Image
import json

st.set_page_config(page_title="AI Research Assistant", layout="wide")

st.markdown("""
<style>
    /* Fix alignment for the upload column and chat input */
    [data-testid="column"] {
        display: flex;
        align-items: center;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    /* Style the sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("📚 Knowledge Base")
    st.markdown("---")
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_pdf:
        st.success(f"Attached: {uploaded_pdf.name}")
    if st.button("Clear PDF Context"):
        st.rerun()

st.markdown("<h1 style='text-align: center;'>💬 DocuBot</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image" in message:
                st.image(message["image"], width=300)

input_placeholder = st.container()

with input_placeholder:
    col1, col2 = st.columns([1, 12])
    
    with col1:
        with st.popover("📷"):
            uploaded_img = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    with col2:
        prompt = st.chat_input("Ask a question...")

if prompt:
    user_msg = {"role": "user", "content": prompt}
    if uploaded_img:
        user_msg["image"] = uploaded_img
    st.session_state.messages.append(user_msg)
    

    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)
            if uploaded_img:
                st.image(uploaded_img, width=300)

    files = {}
    if uploaded_pdf: files["pdf"] = (uploaded_pdf.name, uploaded_pdf, "application/pdf")
    if uploaded_img: files["image"] = (uploaded_img.name, uploaded_img, uploaded_img.type)
    
    try:
        response = requests.post("http://127.0.0.1:8000/process", data={"text": prompt}, files=files)
        if response.status_code != 200:
            backend_response = f"Error {response.status_code}: {response.text}"
        else:
            resp_json = response.json()
            final = resp_json.get("final_answer")
            if isinstance(final, list):
                formatted_items = []
                for idx, item in enumerate(final, start=1):
                    text = item.strip()
                    if not text:
                        continue
                    
                    first_line = text.splitlines()[0]
                    if len(first_line) > 80:
                        parts = text.split('. ', 1)
                        heading = parts[0].strip() + ('.' if parts and not parts[0].endswith('.') else '')
                        body = parts[1].strip() if len(parts) > 1 else ''
                    else:
                        heading = first_line
                        body = '\n'.join(text.splitlines()[1:]).strip() or text[len(first_line):].strip()

                    if body:
                        formatted = f"**{idx}. {heading}**\n\n{body}"
                    else:
                        formatted = f"**{idx}. {heading}**"
                    formatted_items.append(formatted)

                backend_response = "\n\n---\n\n".join(formatted_items) if formatted_items else "No response content."
            elif isinstance(final, dict):
                backend_response = json.dumps(final, indent=2)
            else:
                backend_response = final or "No response content."
    except Exception as e:
        backend_response = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": backend_response})
    with chat_container:
        with st.chat_message("assistant"):
            st.markdown(backend_response)
    
    st.rerun()