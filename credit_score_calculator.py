import os
from groq import Groq
import json
from dotenv import load_dotenv
load_dotenv()

def info_related_to_transactions(transactions):

    prompt = """
Using the provided financial data, calculate the following metrics and return the result **only** in the specified JSON format, without any additional text or explanations.

{
    "total_income": <numeric_value>,
    "total_expenses": <numeric_value>,
    "savings_rate": <numeric_value>,
    "largest_expense": <numeric_value>,
    "num_transactions": <integer>,
    "avg_expense_per_txn": <numeric_value>,
    "stable_income": true or false,
    "irregular_expenses": ["<expense_category_1>", "<expense_category_2>", ...],
    "credit_limit": <numeric_value>,
    "credit_used": <numeric_value>,
    "credit_utilization_rate": <numeric_value>,
    "on_time_payments_ratio": <numeric_value>,
    "missed_payments_last_12_months": <integer>,
    "active_loans": <integer>,
    "total_loan_amount": <numeric_value>,
    "monthly_loan_payment": <numeric_value>,
    "debt_to_income_ratio": <numeric_value>,
    "oldest_credit_account_age": <numeric_value>,
    "average_credit_account_age": <numeric_value>,
    "high_risk_spending_percentage": <numeric_value>,
    "frequent_cash_withdrawals": true or false,
    "recent_large_purchases": ["<purchase_category_1>", "<purchase_category_2>", ...],
    "frequent_bill_payments": true or false,
    "employment_status": "<string>",
    "years_at_current_job": <numeric_value>,
    "income_stability": "Stable" or "Unstable"
}
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


def calculate_credit_score(info):

    prompt = """You are a financial assistant specializing in credit score evaluation.  
                Calculate the credit score based on the following financial data.  
                Additionally, provide an explanation of the credit score reasoning, highlighting key factors that influenced the score.  
                Explain in a clear and concise manner, identifying strengths, weaknesses, and possible improvements based on the financial data.  
                Do not mention any missing information or data gaps.
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
                    "content": f"""{info}"""
                }
            ],
            temperature=0.3,
            top_p=1
        )
    return completion.choices[0].message.content

