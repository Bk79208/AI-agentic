import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Streamlit app title
st.title("Helpful Assistant - The AI Chatbot")

# System prompt for the AI
system_prompt = {
    "role": "system",
    "content": "You are a very helpful assistant. You name is K. What every user asks, you help them in helpful way."
}

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [system_prompt]

# Display chat history
# for message in st.session_state.chat_history:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: flex-end;
                margin: 10px 0;
            ">
                <div style="
                    background-color: Black;
                    padding: 10px 15px;
                    border-radius: 10px;
                    max-width: 75%;
                    word-wrap: break-word;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    {message['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])


# User input field
user_input = st.chat_input("You: ")

if user_input:
    # Append user message to chat history
    user_prompt = {
        "role": "user",
        "content": user_input
    }
    st.session_state.chat_history.append(user_prompt)
    # st.markdown(
    #     f"<div style='text-align: right; padding: 10px; border-radius: 10px; margin: 10px 0;'>{user_input}</div>",
    #     unsafe_allow_html=True
    # )
    st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: flex-end;
                margin: 10px 0;
            ">
                <div style="
                    background-color: Black;
                    padding: 10px 15px;
                    border-radius: 10px;
                    max-width: 75%;
                    word-wrap: break-word;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    {user_input}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Generate a response using Groq API
    llm_response = client.chat.completions.create(
        model="LLama3-70b-8192",
        messages=st.session_state.chat_history,
        max_tokens=500,
        temperature=1.2
    )

    # Extract AI response
    ai_response = llm_response.choices[0].message.content
    ai_response_context = {
        "role": "assistant",
        "content": ai_response
    }

    # Append AI response to chat history
    st.session_state.chat_history.append(ai_response_context)

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(ai_response)
