import streamlit as st
import requests
import os

st.set_page_config(page_title="Strategy Report", layout="wide")
st.title("Strategy Report")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.2.0")
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
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Wardley Map", use_column_width=True)

            # Make an API request to the /v2/analyse_map endpoint with the file
            files = {'file': uploaded_file}
            bearer_token = st.secrets["BEARER_TOKEN"]
            headers = {'Authorization': f'Bearer {bearer_token}'}
            with st.spinner("Analysing your Wardley Map ...."):
                response = requests.post('https://api.wardleymaps.ai/v1/analyse-wardleymap-image', files=files, headers=headers, timeout=240)

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

        with st.expander("Initial"):
            st.markdown("#### Initial Analysis")
            st.write(initial_analysis)

        with st.expander("Challenge"):
            st.markdown("#### Challenged Analysis")
            st.write(challenged_analysis)

        with st.expander("Final"):
            st.markdown("#### Final Analysis")
            st.write(final_analysis)