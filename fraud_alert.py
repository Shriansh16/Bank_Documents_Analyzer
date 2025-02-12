import smtplib
from groq import Groq
import os

def fraud_result(fraud_report):
    prompt="""You are an expert fraud analyst. Your task is to determine whether the given fraud report indicates fraud or not.  
Analyze the fraud report carefully and return only one of the following responses:  
- "Fraud" if the overall fraud score is greater than 80.  
- "Not fraud" if the fraud score is 80 or less.  

**Instructions:**  
- Do not explain your answer, just return the result as "Fraud" or "Not fraud".  
- Consider only the fraud percentage provided in the report.  
- Do not make assumptions beyond the given data.  

### Example Outputs:  
Fraud  
Not fraud 

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
                    "content": f"""Here is the Fraud Report:
                                    {fraud_report}"""
                }
            ],
            temperature=0.3,
            top_p=1
        )
    return completion.choices[0].message.content

def fraud_user_info(records):
    prompt="""Extract all user-related information, including name, account details, and contact details, from the given JSON file. 
Return the extracted information in a structured format 

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
                    "content": f"""Here is the record:
                                    {records}"""
                }
            ],
            temperature=0.3,
            top_p=1
        )
    return completion.choices[0].message.content

def send_email(user_info):
    email = "sheenusingh02122002@gmail.com"
    receiver_email = "shrianshsingh16@gmail.com"
    subject = "Fraud Transaction Alert"
    message = f"This user has been involved in a fraud transaction: {user_info}"
    text = f"Subject: {subject} \n\n{message}"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, "otnlthgqcxlznbqm")
    server. sendmail(email, receiver_email, text)