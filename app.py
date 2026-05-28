import streamlit as st
import os
import time
from template import (
    call_openai, 
    call_openai_mini, 
    OPENAI_MODEL, 
    OPENAI_MINI_MODEL,
    COST_PER_1K_OUTPUT_TOKENS
)
from openai import OpenAI

st.set_page_config(page_title="LLM API Lab UI", page_icon=None, layout="wide")

st.title("LLM API Foundation Lab")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    st.info("Ensure your API key has enough quota. Using models: gpt-4o and gpt-4o-mini.")

# Tabs for different tasks
tab1, tab2 = st.tabs(["Streaming Chatbot", "Model Comparison"])

# --- Tab 1: Streaming Chatbot ---
with tab1:
    st.header("Streaming Chatbot")
    st.write("Maintains the last 3 conversation turns.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What is on your mind?"):
        if not api_key:
            st.error("Please provide an OpenAI API Key in the sidebar.")
        else:
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Keep only last 3 turns (6 messages max: user + assistant)
                # Following the logic from the lab: last 3 items in history
                history = st.session_state.messages[-3:]
                
                client = OpenAI(api_key=api_key)
                try:
                    stream = client.chat.completions.create(
                        model=OPENAI_MODEL,
                        messages=history,
                        stream=True,
                    )
                    
                    for chunk in stream:
                        content = chunk.choices[0].delta.content or ""
                        full_response += content
                        message_placeholder.markdown(full_response)
                    
                    message_placeholder.markdown(full_response)
                    # Add assistant response to history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    # Trim history again
                    st.session_state.messages = st.session_state.messages[-6:]
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- Tab 2: Model Comparison ---
with tab2:
    st.header("Compare GPT-4o vs GPT-4o-mini")
    comp_prompt = st.text_area("Enter prompt for comparison", value="Tell me a fun fact about Vietnam.")
    
    if st.button("Run Comparison"):
        if not api_key:
            st.error("Please provide an OpenAI API Key in the sidebar.")
        else:
            with st.spinner("Calling both models..."):
                try:
                    col1, col2 = st.columns(2)
                    
                    # GPT-4o
                    start_4o = time.time()
                    resp_4o, _ = call_openai(comp_prompt)
                    lat_4o = time.time() - start_4o
                    
                    # GPT-4o-mini
                    start_mini = time.time()
                    resp_mini, _ = call_openai_mini(comp_prompt)
                    lat_mini = time.time() - start_mini
                    
                    # Cost estimates
                    tokens_4o = len(resp_4o.split()) / 0.75
                    cost_4o = (tokens_4o / 1000) * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
                    
                    tokens_mini = len(resp_mini.split()) / 0.75
                    cost_mini = (tokens_mini / 1000) * COST_PER_1K_OUTPUT_TOKENS["gpt-4o-mini"]
                    
                    with col1:
                        st.subheader("GPT-4o")
                        st.success(f"Latency: **{lat_4o:.2f}s**")
                        st.info(f"Est. Cost: **${cost_4o:.6f}**")
                        st.write(resp_4o)
                        
                    with col2:
                        st.subheader("GPT-4o-mini")
                        st.success(f"Latency: **{lat_mini:.2f}s**")
                        st.info(f"Est. Cost: **${cost_mini:.6f}**")
                        st.write(resp_mini)
                        
                except Exception as e:
                    st.error(f"Error: {e}")
