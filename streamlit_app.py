import os, uuid
import streamlit as st

MODEL = "gpt-3.5-turbo"
DEBUG = True # True to overwrite files that already exist

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGCHAIN_PROJECT"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Chat with your Wardley Map")
st.title("Chat with Simon Wardley's Book")
st.sidebar.markdown("# Have a chat with your using AI")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 1.3.0")
#st.sidebar.markdown(st.session_state.session_id)
st.sidebar.markdown("Wardley Mapping is provided courtesy of Simon Wardley and licensed Creative Commons Attribution Share-Alike.")
st.sidebar.divider()

# Set styling for buttons. Full column width, primary colour border.
primaryColor = st.get_option("theme.primaryColor")
custom_css_styling = f"""
<style>
    /* Style for buttons */
    div.stButton > button:first-child, div.stDownloadButton > button:first-child {{
        border: 5px solid {primaryColor};
        border-radius: 20px;
        width: 100%;
    }}
    /* Center align button container */
    div.stButton, div.stDownloadButton {{
        text-align: center;
    }}
    .stButton, .stDownloadButton {{
        width: 100%;
        padding: 0;
    }}
</style>
"""
st.html(custom_css_styling)

def handle_file_upload(uploaded_file):
    try:
        if uploaded_file:
            bytes_data = uploaded_file.read()
            text = bytes_data.decode('utf-8')
            return text
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

uploaded_file = st.sidebar.file_uploader("Upload a text file", type=["txt", "pdf", "docx"])

for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if query := st.chat_input("What question do you have for the book?"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner():
        with st.chat_message("assistant"):
            response = st.session_state.chain(query)
            st.markdown(response['answer'])

        with st.expander("Source"):
                source_documents = response['source_documents']
                for index, document in enumerate(source_documents):
                    # Safely retrieve metadata using `get` to avoid KeyError
                    chapter_details = document.metadata.get('Chapter', 'Not provided')
                    section_details = document.metadata.get('Section', 'Not provided')
                    st.markdown(f":blue[Source {index + 1}]")
                    st.markdown(f"{chapter_details}")
                    st.markdown(f"Section: {section_details}")

        st.divider()

    st.session_state.messages.append({"role": "assistant", "content": response['answer']})
