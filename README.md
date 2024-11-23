# LLM Chat Interface with Streamlit

This repository provides a Streamlit web application for interacting with large language models (LLMs) from the Hugging Face Hub. It allows users to have real-time conversations with LLMs, switch between different models, and manage API tokens.

## Features

- **Model Selection**: Choose between different LLMs available on Hugging Face.
- **User-friendly Chat Interface**: A simple web interface to chat with LLMs.
- **Hugging Face API Integration**: Uses `InferenceClient` to communicate with LLMs.
- **Session Management**: Keeps track of conversations and model selection.

## Installation

To run the application locally:

1. Clone the repository:

   ```sh
   git clone <repository-url>
   ```

2. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:

   ```sh
   streamlit run app.py
   ```

## Requirements

- **Python 3.11+**
- **Streamlit**: For the user interface.
- **Hugging Face Hub**: For interacting with the LLMs.

Ensure that `requirements.txt` includes the following:

```
streamlit
huggingface_hub
```

## Usage

- **Launch the App**: Run the command above to start the app.
- **Enter Your Hugging Face Token**: When first launching the app, you will be prompted to enter your Hugging Face API token.
- **Don't Have a Token?**: Use the test token `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` to try out the app.
- **Select a Model**: Use the sidebar to choose a model.
- **Interact with the Model**: Type your questions in the input box and click "Send".
- **Reset Options**: You can reset the model, API token, or the entire application state using the sidebar buttons.

## Code Overview

- **`initialize_session_state()`**: Initializes the session state to keep track of user settings.
- **`home()`**: Renders the main chat interface, allowing users to select a model, reset the app, and chat with the model.
- **`query_llm()`**: Sends the user's input to the selected LLM and returns the response.
- **`generate_conversation_html()`**: Creates the chat history in a user-friendly format.
- **`validate_hf_token()`**: Prompts users for the Hugging Face API token and validates it.

## Error Handling

- The application handles invalid tokens and API connection errors gracefully, providing user-friendly error messages.

## Future Improvements

- **User Accounts with Firebase**: Implement user accounts for personalized experiences.
- **RAG Setup with No Code Tools**: Integrate no-code Retrieval-Augmented Generation (RAG) using Unstructured.io and Pinecone.
- **Additional Models**: Add open-source models as well as OpenAI models.
- **LangChain for Interaction Handling**: Use LangChain to streamline interactions and manage conversation flow.

## License

This project is open source and available under the MIT License.

---

**Note**: You need a valid Hugging Face API token to use this application. You can get one by creating an account on [Hugging Face](https://huggingface.co/) or use the test token provided above.
