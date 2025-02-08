import os
from store_to_MongoDB import BankInfoStorage
from retrieve_from_mongoDB import BankInfoRetrieval
from fraud_detector import *
import tempfile
import streamlit as st


st.title("Intelligent Banking Data Processing & Risk Assessment")
st.subheader("Upload your Bank Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=False)

if uploaded_file:
   with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_pdf_path = temp_file.name
   storage = BankInfoStorage()
   storage.store_info(temp_pdf_path)
   retriever = BankInfoRetrieval()
   latest_data = retriever.retrieve_latest_info()
   transactions = find_transactions(json.dumps(latest_data, indent=4))
   print(transactions)
   insights=find_insights(transactions)
   st.subheader("Financial Insights:")
   st.write(insights)
   fraud_detection_result = detect_fraud_all_transactions(transactions)
   st.subheader("Fraud Detection result:")
   st.write(fraud_detection_result)


