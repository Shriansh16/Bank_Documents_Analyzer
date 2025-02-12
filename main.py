from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import json
from typing import Dict
import os
from pydantic import BaseModel
from store_to_MongoDB import BankInfoStorage
from retrieve_from_mongoDB import BankInfoRetrieval
from fraud_alert import *
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
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversation memory for each session
conversation_memories = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_pdf_path = temp_file.name

        # Store and retrieve data
        storage = BankInfoStorage()
        storage.store_info(temp_pdf_path)
        retriever = BankInfoRetrieval()
        latest_data = retriever.retrieve_latest_info()
        transactions = find_transactions(json.dumps(latest_data, indent=4))

        # Extract insights
        insights = find_insights(transactions)
        structured = structured_transactions(transactions)
        fraud_detection_result = detect_fraud_all_transactions(transactions)
        overall_fraud_result=fraud_result(fraud_detection_result)
        if overall_fraud_result=="Fraud":
            fraud_user_info_result=fraud_user_info(latest_data)
            send_email(fraud_user_info_result)
        info = info_related_to_transactions(transactions)
        credit_score_insights = calculate_credit_score(info)

        # Clean up temporary file
        os.unlink(temp_pdf_path)

        return {
            "insights": insights,
            "structured_data": structured,
            "fraud_detection": fraud_detection_result,
            "credit_score": credit_score_insights
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    session_id = chat_request.session_id
    user_message = chat_request.message

    # Initialize conversation memory if it doesn't exist
    if session_id not in conversation_memories:
        conversation_memories[session_id] = ConversationBufferWindowMemory(k=1, return_messages=True)

    try:
        # Initialize LLM
        llm = ChatGroq(
            groq_api_key=os.getenv('GROQ_API_KEY'),
            model_name="llama-3.3-70b-versatile",
            temperature=0.6
        )

        # Get the latest financial data
        retriever = BankInfoRetrieval()
        latest_data = retriever.retrieve_latest_info()
        transactions = find_transactions(json.dumps(latest_data, indent=4))
        insights = find_insights(transactions)
        fraud_detection_result = detect_fraud_all_transactions(transactions)
        info = info_related_to_transactions(transactions)
        credit_score_insights = calculate_credit_score(info)


        # Create system message template
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
            memory=conversation_memories[session_id],
            prompt=prompt_template,
            llm=llm,
            verbose=True
        )

        # Get response
        response = conversation.predict(input=f"Query:\n{user_message}")
        
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)