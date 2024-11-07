# streamlit run main.py
import os
import streamlit as st
from vertexai.preview.generative_models import GenerativeModel, Tool
import vertexai
from vertexai.preview.generative_models import grounding as preview_grounding

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)
PROJECT_ID = "janison"  # @param {type:"string"}
REGION = "us-central1"  # @param {type: "string"}

DATA_STORE_PROJECT_ID = PROJECT_ID  # @param {type:"string"}
DATA_STORE_REGION = "global"  # @param {type:"string"}
# Replace this with your data store ID from Vertex AI Search
DATA_STORE_ID = "janison-com_1730988913673"  # @param {type:"string"}


# Set up Google Gemini-Pro AI model
vertexai.init(project=PROJECT_ID, location="us-central1")

tool = Tool.from_retrieval(
    preview_grounding.Retrieval(
        preview_grounding.VertexAISearch(
            datastore=DATA_STORE_ID,
            project=DATA_STORE_PROJECT_ID,
            location=DATA_STORE_REGION,
        )
    )
)

# System instructions https://cloud.google.com/vertex-ai/generative-ai/docs/reference/python/latest#system-instructions
model = GenerativeModel(model_name='gemini-pro', tools=[tool])


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("🤖 Janison chatbot")
st.caption("Start by asking 'what was the challenge that Transport for NSW was facing?' and compare the answer with the 'The challenge' on https://www.janison.com/customer-stories/transport-for-nsw")

from vertexai.preview.generative_models import grounding as preview_grounding

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Talk to chatbot...")

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)# , tools=[tool])

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
        