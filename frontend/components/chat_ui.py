"""
Chat UI component
"""

import streamlit as st
from datetime import datetime


def render_chat_interface():
    """Render the chat interface"""

    st.title("💬 Chat with Your Fitness AI")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input(
        "Tell me what you ate, ask for a summary, or set a goal..."
    ):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.api_client.chat(
                        user_id=st.session_state.user_id, message=prompt
                    )

                    st.markdown(response["response"])

                    # Add assistant message
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response["response"]}
                    )

                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
