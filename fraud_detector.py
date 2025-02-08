import os
from groq import Groq
import json
from retrieve_from_mongoDB import BankInfoRetrieval
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
    You are a financial fraud detection AI. Analyze the bank statement below and identify any suspicious transactions.
    Consider risk factors such as:
    - Large or unusual amounts
    - Transactions at unrecognized locations
    - Unusual transaction times
    - Rapid withdrawals
    - Duplicate payments
    - Sudden changes in spending behavior

    Provide:
    1. A list of suspicious transactions with explanations.
    2. A summary of any unusual spending patterns.
    3. A fraud risk score (0-100) for this account.
    """
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
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
    prompt="""You are an expert financial analyst AI. Your task is to analyze user transaction data and generate structured financial insights. Your response should be well-structured and insightful.
    Objectives:
1. **Weekly Spending Trends:** Provide a summary of spending for each week.
2. **Monthly Spending Trends:** Analyze spending patterns across months.
3. **Category-wise Breakdown:** Highlight major expense categories.
4. **High-Spending Alerts:** Identify any unusually high transactions.
5. **Recurring Transactions:** Detect subscriptions, EMIs, and fixed expenses.
6. **Savings Analysis:** Compare income vs. expenses and suggest improvements.
"""
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
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

if __name__ == "__main__":
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
    else:
        print("No data found.")
