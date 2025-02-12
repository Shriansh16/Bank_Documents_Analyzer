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


"""if __name__=="__main__":
    transactions= """[
    {
        "date": "1 February",
        "description": "Cardpayment - High St Petrol Station",
        "money_out": "24.50",
        "money_in": null,
        "balance": "39975.50",
        "category": "Expenses"
    },
    {
        "date": "1 February",
        "description": "Direct debit - Green Mobile Phone Bill",
        "money_out": "20.00",
        "money_in": null,
        "balance": "39955.50",
        "category": "Expenses"
    },
    {
        "date": "3 February",
        "description": "Cash Withdrawal - YourBank, Anytown High Street, timed 17:30 31 Jan",
        "money_out": "30.00",
        "money_in": null,
        "balance": "39925.50",
        "category": "Expenses"
    },
    {
        "date": "4 February",
        "description": "YourJob BiWeekly Payment",
        "money_out": null,
        "money_in": "2575.00",
        "balance": "42500.50",
        "category": "Income"
    },
    {
        "date": "11 February",
        "description": "Direct Deposit - YourBank, Anytown High Street, timed 17:30 31 Jan",
        "money_out": null,
        "money_in": "300.00",
        "balance": "42800.50",
        "category": "Income"
    },
    {
        "date": "16 February",
        "description": "Cash Withdrawal - RandomBank, Randomford, timed 9.52 14 Feb",
        "money_out": "50.00",
        "money_in": null,
        "balance": "42750.50",
        "category": "Expenses"
    },
    {
        "date": "17 February",
        "description": "Card payment - High St Petrol Station",
        "money_out": "40.00",
        "money_in": null,
        "balance": "42710.50",
        "category": "Expenses"
    },
    {
        "date": "17 February",
        "description": "Direct Debit - Home Insurance",
        "money_out": "78.34",
        "money_in": null,
        "balance": "42632.16",
        "category": "Expenses"
    },
    {
        "date": "18 February",
        "description": "YourJob BiWeekly Payment",
        "money_out": null,
        "money_in": "2575.00",
        "balance": "45207.16",
        "category": "Income"
    },
    {
        "date": "18 February",
        "description": "Randomford's Deli",
        "money_out": "15.00",
        "money_in": null,
        "balance": "45195.16",
        "category": "Expenses"
    },
    {
        "date": "24 February",
        "description": "Anytown's Jewelers",
        "money_out": "150.00",
        "money_in": null,
        "balance": "45042.16",
        "category": "Expenses"
    },
    {
        "date": "24 February",
        "description": "Direct Deposit",
        "money_out": null,
        "money_in": "25.00",
        "balance": "45067.16",
        "category": "Income"
    },
    {
        "date": "28 February",
        "description": "Monthly Apartment Rent",
        "money_out": "987.33",
        "money_in": null,
        "balance": "44079.83",
        "category": "Expenses"
    }
]"""
    info=info_related_to_transactions(transactions)
    print(info)
    credit_score_insights=calculate_credit_score(info)
    print(credit_score_insights)"""