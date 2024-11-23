import streamlit as st
from streamlit.components.v1 import html
from huggingface_hub import InferenceClient, HfApi
from huggingface_hub.errors import HfHubHTTPError

DEFAULT_HUGGING_FACE_TOKEN = "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"

# Constants for model configurations
MODELS_ID = {
    "Mistral - 7B - Instruct - Version 0.3": "mistralai/Mistral-7B-Instruct-v0.3",
    "Llama 3.1 - 70B - Instruct": "mistralai/Mistral-7B-Instruct-v0.3",
}

MODEL_CHOICES = list(MODELS_ID.keys())

# Custom CSS for styling Streamlit components
CUSTOM_CSS = """
<style>
.stButton button[kind="primary"] {
    width: 100%;
    border: none;
    border-radius: 0;
    border-bottom: 2px solid gray;
    background-color: transparent;
    color: inherit;
    padding: 0;
    margin: 0;
    box-shadow: none;
}
.stButton button[kind="primary"]:focus {
    border-bottom: 2px solid rgb(255, 153, 154);
    border-radius: 0;
    background-color: transparent;
    color: rgb(255, 153, 154);
}
.element-container:has(#full-width-button) + div button {
    width: 100%;
    border: none;
}
</style>
"""

MARKDOWN_DIVIDER = "---"

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize the session state for the app."""
    if "model_choice" not in st.session_state:
        st.session_state.model_choice = MODEL_CHOICES[0]
    if "conversation" not in st.session_state:
        st.session_state.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    if "queyllm" not in st.session_state:
        st.session_state.queyllm = False

def home():
    """Home page for the Streamlit app."""
    # Set up page configuration
    st.title("LLM Chat Interface")
    st.sidebar.header("Choose Model")

    # Model Selection
    model_choice_select = st.sidebar.selectbox(
        "Choose an LLM model:",
        MODEL_CHOICES,
        index=MODEL_CHOICES.index(st.session_state.model_choice),
    )

    st.sidebar.markdown('<span id="full-width-button"></span>', unsafe_allow_html=True)
    if st.sidebar.button("Apply"):
        st.session_state.model_choice = model_choice_select

    st.sidebar.markdown(MARKDOWN_DIVIDER)

    st.sidebar.markdown('<span id="full-width-button"></span>', unsafe_allow_html=True)
    if st.sidebar.button("Reset Hugging Face Token?"):
        if "hf_token" in st.session_state:
            del st.session_state["hf_token"]
        st.rerun()

    st.sidebar.markdown(MARKDOWN_DIVIDER)

    st.sidebar.markdown('<span id="full-width-button"></span>', unsafe_allow_html=True)
    if st.sidebar.button("Reset Application"):
        del st.session_state["hf_token"]
        del st.session_state["model_choice"]
        del st.session_state["conversation"]
        del st.session_state["queyllm"]
        st.rerun()

    # Validate API Token
    try:
        client = InferenceClient(api_key=st.session_state.hf_token)
    except KeyError:
        st.error("Hugging Face token not found. Please enter it below.")
        return
    except HfHubHTTPError as e:
        st.error(f"Error connecting to Hugging Face Hub: {e}")
        return

    # Chat Functionality
    html_content = generate_conversation_html(st.session_state.conversation)
    html(html_content, height=500, scrolling=True)

    # User Input
    user_input = st.text_input("You:", value="")
    if st.button("Send") and user_input:
        st.session_state.conversation.append({'role': 'user', 'content': user_input})
        st.session_state.queyllm = True
        st.rerun()

    if st.session_state.queyllm:
        role, response = query_llm(client, st.session_state['conversation'])
        st.session_state.conversation.append({'role': role, 'content': response, "model": st.session_state.model_choice})
        st.session_state.queyllm = False
        st.rerun()

def query_llm(client, chat_history):
    """Query the LLM model with the current chat history."""
    try:
        output = client.chat_completion(
            model=MODELS_ID[st.session_state.model_choice],
            messages=chat_history,
            max_tokens=500,
            stream=False,
        )
        return output.choices[0].message['role'], output.choices[0].message['content']
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "assistant", "Sorry, I couldn't process that request."

def generate_conversation_html(conversation):
    """Generate HTML to display the conversation in a chat-like format."""
    html_content = """
    <style>
        .conversation-container {
            font-family: Arial, sans-serif;
            background-color: transparent;
            overflow-y: auto;
            width: 100%;
            height: 400px;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 10px;
        }
        .user {
            background-color: #f0f0f0;
            color: #000;
        }
        .assistant {
            background-color: transparent;
            color: #f0f0f0;
            border: 1px solid #f0f0f0;
        }
        .role {
            font-weight: bold;
        }
    </style>
    <div class="conversation-container" id="conversation-container">
    """

    for message in conversation:
        if message['role'] == 'system':
            continue
        role_class = 'user' if message['role'] == 'user' else 'assistant'
        html_content += f"<div class='message {role_class}'>"
        if role_class == "assistant":
            html_content += f"<span class='role'>{role_class.capitalize()} ({message['model']}):</span><br>{message['content']}"
        else:
            html_content += f"<span class='role'>{role_class.capitalize()}:</span><br>{message['content']}"
        html_content += "</div>\n\n"

    html_content += """
    </div>
    <script>
        var conversationContainer = document.getElementById('conversation-container');
        conversationContainer.scrollTop = conversationContainer.scrollHeight;
    </script>
    """
    return html_content

def validate_hf_token():
    """Prompt the user to input the Hugging Face API token."""
    hf_token = st.text_input("Please enter your Hugging Face token.", value=DEFAULT_HUGGING_FACE_TOKEN)
    if st.button("Validate"):
        if not hf_token:
            st.error("The token cannot be blank")
        else:
            try:
                HfApi().whoami(token=hf_token)
                st.session_state.hf_token = hf_token
                st.rerun()
            except HfHubHTTPError as e:
                st.error(f"Invalid token: {e}")

if __name__ == "__main__":
    initialize_session_state()
    if "hf_token" in st.session_state:
        home()
    else:
        validate_hf_token()
