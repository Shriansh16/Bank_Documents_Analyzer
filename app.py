import os
import json
import tempfile
import streamlit as st
from store_to_MongoDB import BankInfoStorage
from retrieve_from_mongoDB import BankInfoRetrieval
from credit_score_calculator import *
from fraud_detector import *
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from fraud_alert import *
from streamlit_chat import message
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

# Title and File Upload
st.title("Intelligent Banking Data Processing & Risk Assessment")
st.subheader("Upload your Bank Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=False)

# Process File Only Once
if uploaded_file and "file_processed" not in st.session_state:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_pdf_path = temp_file.name

    # Store and Retrieve Data
    storage = BankInfoStorage()
    storage.store_info(temp_pdf_path)  # Store in MongoDB once
    retriever = BankInfoRetrieval()
    latest_data = retriever.retrieve_latest_info()
    transactions = find_transactions(json.dumps(latest_data, indent=4))

    # Extract Insights
    st.session_state["insights"] = find_insights(transactions)
    st.session_state["structured"] = structured_transactions(transactions)
    st.session_state["fraud_detection_result"] = detect_fraud_all_transactions(transactions)
    overall_fraud_result=fraud_result(st.session_state["fraud_detection_result"])
    if overall_fraud_result=="Fraud":
            fraud_user_info_result=fraud_user_info(latest_data)
            send_email(fraud_user_info_result)
    st.session_state["info"] = info_related_to_transactions(transactions)
    st.session_state["credit_score_insights"] = calculate_credit_score(st.session_state["info"])

    # Mark file as processed
    st.session_state["file_processed"] = True

# Display Results if Data is Available
if "file_processed" in st.session_state:
    st.subheader("Financial Insights:")
    st.write(st.session_state["insights"])
    plot_financial_graph(st.session_state["structured"])

    st.subheader("Fraud Detection Result:")
    st.write(st.session_state["fraud_detection_result"])

    st.subheader("Credit Score Calculation:")
    st.write(st.session_state["credit_score_insights"])

# Initialize Chatbot Once
if "chat_active" not in st.session_state:
    st.session_state.chat_active = False
if "responses" not in st.session_state:
    st.session_state.responses = [
        "Hi there! Welcome to the Intelligent Banking Assistant. What can I help you with today?"
    ]
if "requests" not in st.session_state:
    st.session_state.requests = []
if "buffer_memory" not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=1, return_messages=True)

# Chatbot Section
if st.button("Have a Question? Click to Chat"):
    st.session_state.chat_active = True

if st.session_state.chat_active:
    # Ensure financial data is available
    insights = st.session_state.get("insights", "No insights available.")
    fraud_detection_result = st.session_state.get("fraud_detection_result", "No fraud data available.")
    credit_score_insights = st.session_state.get("credit_score_insights", "No credit score data available.")

    # Initialize LLM
    llm = ChatGroq(
        groq_api_key=os.getenv('GROQ_API_KEY'),
        model_name="llama-3.3-70b-versatile",
        temperature=0.6
    )

    # Define prompt templates
    system_msg_template = SystemMessagePromptTemplate.from_template(
        template=f"""You are an intelligent financial assistant that analyzes transaction history, spending behavior, and financial patterns to provide insights, savings suggestions, investment opportunities, and financial planning tips. Your responses should be clear, concise, and personalized to the user's financial situation.
        Here is the financial information to analyze: 
        - **Insights:** {insights}
        - **Fraud Detection:** {fraud_detection_result}
        - **Credit Score:** {credit_score_insights}
        """
    )
    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
    prompt_template = ChatPromptTemplate.from_messages(
        [system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template]
    )

    # Create conversation chain
    conversation = ConversationChain(
        memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True
    )

    # Chat Interface
    response_container = st.container()
    text_container = st.container()

    with text_container:
        user_query = st.chat_input("Enter your query")
        if user_query:
            with st.spinner("Typing..."):
                response = conversation.predict(input=f"Query:\n{user_query}")
                st.session_state.requests.append(user_query)
                st.session_state.responses.append(response)

    # Display Chat History
    with response_container:
        for i in range(len(st.session_state.responses)):
            with st.chat_message("Assistant"):
                st.write(st.session_state.responses[i])
            if i < len(st.session_state.requests):
                message(st.session_state.requests[i], is_user=True, key=str(i) + "_user")
