import os
from groq import Groq
import json
import re
import streamlit as st
from retrieve_from_mongoDB import BankInfoRetrieval
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

def find_transactions(message: str) -> str:
    try:
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system", 
                    "content": "Extract only the transactions from the provided JSON data. Return them as a JSON array, maintaining the original structure and values. Exclude any other details such as summaries, balances, or customer information. Output only the JSON array without any additional text or formatting."
                },
                {
                    "role": "user", 
                    "content": message
                }
            ],
            temperature=0.3,
            top_p=1
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"
    

def detect_fraud_all_transactions(transactions):

    prompt = f"""
    You are an AI fraud detection expert analyzing financial transactions. 
Identify fraudulent activities based on:
- Large or unusual transactions compared to past spending.
- Rapid withdrawals or multiple transfers in a short period.
- Transactions at unusual times or locations.
- Sudden changes in spending behavior.

### **Fraud Detection Report**  

**1. Transaction Risk Scores:**  
   - Assign a fraud risk score (0-100) to each transaction.  

**2. High-Risk Transactions (Score > 80):**  
   - List transactions that are highly suspicious.  
   - Provide a brief reason for each flagged transaction.  

**3. Unusual Spending Patterns:**  
   - Summarize any deviations from normal spending behavior.  

**4. Overall Fraud Risk Score:**  
   - Calculate an overall fraud risk score (0-100) based on detected anomalies. 
    """
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": prompt
                },
                {
                    "role": "user", 
                    "content": f"""Here is the transaction history:
                                    {transactions}"""
                }
            ],
            temperature=0.3,
            top_p=1
        )
    return completion.choices[0].message.content

def find_insights(transactions):
    prompt="""You are a financial assistant analyzing a user's bank statement. 

Provide a summary of key financial insights, including:
- Total income and total expenses.
- Unusual spending behavior.
- Key spending trends.
- Any notable financial changes.
- Recommendations for improving financial health.

Return a detailed but concise financial summary.

"""
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": prompt
                },
                {
                    "role": "user", 
                    "content": f"""Here is the transaction history:
                                    {transactions}"""
                }
            ],
            temperature=0.3,
            top_p=1
        )
    return completion.choices[0].message.content

def structured_transactions(transactions):
    prompt="""You are given a list of financial transactions in JSON format.
           Extract and structure the data as follows:
           1. Group transactions by date.
           2. For each date, calculate:
             - "money_spent": Total sum of all "money_out" values for that date.
             - "money_credited": Total sum of all "money_in" values for that date.
             - "final_balance": The last available "balance" for that date.
           Output only a valid JSON array without explanations or additional text.
           Format the date as "DD Month YYYY". If the year is missing, assume 2024.
           Example output:
           [
             {
               "date": "DD Month 2024",
               "money_spent": XX.XX,
               "money_credited": XX.XX,
               "final_balance": XX.XX
             }
           ]
           """
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": prompt
                },
                {
                    "role": "user", 
                    "content": f"""Here is the transaction history:
                                    {transactions}"""
                }
            ],
            temperature=0.3,
            top_p=1
        )
    return completion.choices[0].message.content

def plot_financial_graph(json_data):
    # Load data from JSON
    data = json.loads(json_data)
    
    # Convert dates to datetime objects
    dates = [datetime.strptime(entry["date"], "%d %B %Y") for entry in data]
    money_spent = [entry["money_spent"] for entry in data]
    money_credited = [entry["money_credited"] for entry in data]
    final_balance = [entry["final_balance"] for entry in data]
    
    # Create figure and axis
    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    # Plot money spent and credited
    ax1.bar(dates, money_spent, color='red', label="Money Spent", alpha=0.7)
    ax1.bar(dates, money_credited, color='green', label="Money Credited", alpha=0.7, bottom=money_spent)
    ax1.set_ylabel("Amount ($)")
    ax1.set_xlabel("Date")
    ax1.legend(loc="upper left")
    
    # Create second y-axis for balance
    ax2 = ax1.twinx()
    ax2.plot(dates, final_balance, color='blue', marker='o', linestyle='-', label="Final Balance")
    ax2.set_ylabel("Final Balance ($)")
    ax2.legend(loc="upper right")
    
    # Formatting
    plt.xticks(rotation=45)
    plt.title("Financial Transactions")
    plt.grid(True)
    st.pyplot(fig)
    

"""if __name__ == "__main__":
    retriever = BankInfoRetrieval()
    latest_data = retriever.retrieve_latest_info()
    latest_data=json.dumps(latest_data, indent=4)
    print(latest_data)
    if latest_data:
        transactions = find_transactions(latest_data)
        print(transactions)
        print("." * 20)
        fraud_detection_result = detect_fraud_all_transactions(transactions)
        print(fraud_detection_result)
        print("." * 20)
        insights=find_insights(transactions)
        print(insights)
        print("." * 20)
        structured=structured_transactions(transactions)
        print(structured)
    else:
        print("No data found.")"""
