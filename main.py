import streamlit as st
from langchain_processing import few_shot_chain
import pandas as pd
from decimal import Decimal
import datetime

st.title("The Avocado Forecast")
question = st.text_input("Question: ")

def output_processing(op):
    return pd.DataFrame(eval(op, {'Decimal': Decimal, 'datetime': datetime}))

if question:
    response = few_shot_chain(question)
    post_proc_response = output_processing(response)

    st.header("Answer")
    st.write(post_proc_response)