import openai
import streamlit as st
from langchain_processing import few_shot_chain
import pandas as pd
from decimal import Decimal
import datetime

def output_processing(op):
    return pd.DataFrame(eval(op, {'Decimal': Decimal, 'datetime': datetime}))


def check_openai_api_key(api_key):
    client = openai.OpenAI(api_key=api_key)
    try:
        client.models.list()
    except openai.AuthenticationError:
        return False
    else:
        return True

# Entry Screen
st.title("The Avocado Forecast")

# If API key not yet submitted
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

# Show the API input screen if no key submitted yet
if st.session_state.api_key is None:
    st.subheader("Enter your OpenAI API Key")
    api_input = st.text_input("API Key", type="password")
    if st.button("Submit"):
        if api_input.strip() == "":
            st.warning("Please enter a valid API key.")
        else:
            st.session_state.api_key = api_input.strip()
            # Test if OpenAI key works
            if check_openai_api_key(st.session_state.api_key):
                print("Valid OpenAI API key.")
                st.rerun()  # Refresh the app to move to the next screen
            else:
                st.warning("Invalid OpenAI API key. Please re-enter your key.")
            
else:
    # Next screen after API is submitted
    st.success("API Key received successfully!")
    
    # You can now add whatever you want here
    st.write("Please enter your query for the database below.")
    
    # Example follow-up UI
    st.write(f"Your API key (securely stored): `{st.session_state.api_key[:4]}...`")

    question = st.text_input("Question: ")
    
    if question:
        response = few_shot_chain(question, st.session_state.api_key)
        if not response:
            st.write("Couldn't process question. Please try another one!")
        else:
            post_proc_response = output_processing(response)
    
            st.header("Answer")
            st.write(post_proc_response)

# Remove API key
if st.button("Reset API Key"):
    st.session_state.api_key = None
    st.rerun()