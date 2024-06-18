import streamlit as st
import requests
import os

if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Chat with your Wardley Map")
st.title("Chat with your Wardley Map")
st.sidebar.markdown("# Have a chat with your using AI")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 1.3.0")
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
            # Make an API request to the /v2/analyse_map endpoint with the file
            files = {'file': uploaded_file}
            bearer_token = st.secrets["BEARER_TOKEN"]
            headers = {'Authorization': f'Bearer {bearer_token}'}
            response = requests.post('https://api.wardleymaps.ai/v1/analyse-wardleymap-image', files=files, headers=headers, timeout=60)

            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error: {response.status_code}, {response.text}")
                return None
    except Exception as e:
        st.error(f"Error uploading file: {e}")
        return None

uploaded_file = st.sidebar.file_uploader("Upload a PNG or JPEG file", type=["png", "jpeg"])

if uploaded_file:
    file_analysis = handle_file_upload(uploaded_file)
    if file_analysis:
        st.markdown("### Analysis Result")

        initial_analysis = file_analysis.get("initial_analysis", "No initial analysis provided.")
        challenged_analysis = file_analysis.get("challenged_analysis", "No challenged analysis provided.")
        final_analysis = file_analysis.get("final_analysis", "No final analysis provided.")

        st.markdown("#### Initial Analysis")
        st.write(initial_analysis)

        st.markdown("#### Challenged Analysis")
        st.write(challenged_analysis)

        st.markdown("#### Final Analysis")
        st.write(final_analysis)