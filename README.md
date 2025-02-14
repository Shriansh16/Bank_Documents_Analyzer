# Intelligent Bank Document Analyzer

## Overview

This project is an Intelligent Banking Assistant that processes financial data from uploaded bank documents (PDFs) and provides insights, fraud detection, and credit score assessment. Additionally, it includes a chatbot powered by LangChain and ChatGroq to assist users with their financial queries.

## Features
1. Bank Document Processing: Upload a bank document (PDF) for analysis.

2. Data Extraction & Structuring: Uses Gemini Flash 2.0 for extracting and structuring data.

3. Data Storage & Retrieval: Stores transaction data in MongoDB and retrieves insights.

4. Financial Insights: Extracts transaction insights, spending behavior, and structured data.

5. Fraud Detection: Identifies potential fraudulent transactions using Llama-3.3-70B-Versatile via Groq.

6. Credit Score Calculation: Estimates credit scores based on transaction history using Llama-3.3-70B-Versatile via Groq.

7. Interactive Chatbot: An AI-powered financial assistant for personalized guidance.

8. Email Alerts: Sends an email to the admin if a fraudulent transaction is detected.

## How It Works

1. Upload a Bank Document: The system extracts financial transactions using Gemini Flash 2.0.

2. Store & Retrieve Data: The extracted data is stored in MongoDB and later retrieved for analysis.

3. Analyze Transactions: Financial insights, fraud detection, and credit score calculations are performed using Llama-3.3-70B.

4. Chatbot Assistance: Users can interact with an AI chatbot to get insights into their finances.

5. Fraud Alert: If fraud is detected, an email alert is automatically sent to the admin.

## Tools and Libraries Used

1. Google Generative AI (Gemini Flash 2.0)
Used for extracting and structuring financial data from bank documents.

2. LangChain
Used for managing conversation chains, prompt templates, and maintaining chatbot memory.

3. Llama-3.3-70B-Versatile (via Groq)
Used for generating financial insights, fraud detection, and credit score assessment.

4. Streamlit
Used for building the web-based UI for document upload, data visualization, and chatbot interaction.

5. MongoDB
Used for storing and retrieving financial transaction data.

6. Groq API
Facilitates communication with the Llama-3.3-70B model.

7. Dotenv
Loads environment variables to securely manage API keys.

8. SMTP (smtplib)
Sends email alerts to the admin when fraudulent transactions are detected.

9. FastAPI
It is used for creating the web application, handling API requests, and serving both the medical chatbot and medical report generation functionalities.

10. Uvicorn
It is used to run the FastAPI application locally or on a server.

## Directory Structure
1. main.py – Backend implementation.
2. templates/ – Frontend interface.
3. app.py – Streamlit implementation of the project.
4. credit_score_calculator.py – Credit score calculator.
5. fraud_detector.py – Prepares insights and fraud reports.
6. pdf_extractor.py – Extracts text and data from uploaded documents.
7. store_to_mongoDB.py – Stores the extracted data in MongoDB.
8. retrieve_from_mongoDB.py – Retrieves the uploaded data from MongoDB.
9. fraud_alert.py – Sends fraud alerts to the admin if fraud is detected.

## How to run?
First, create a file named .env and add the following lines:                                        
1. GROQ_API_KEY="YOUR GROQ API KEY"
2. gemini_api_key="YOUR GEMINI API KEY"
### Follow these steps to run the project:
step 1.  Start the Backend Servers                                                     
 Run the following command in your terminal to start the backend                          service:                                                                         
 uvicorn main:app                                                                

Step 2. Open the Frontend
 Once the backend is running, open index.html in your browser.   


 ## OR directly run the streamlit app      

 streamlit run app.py                                                              