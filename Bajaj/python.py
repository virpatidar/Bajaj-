import requests

# Step 1: Define user details
user_data = {
    "name": "Virendra Patidar",          
    "regNo": "REG12347",           
    "email": "virendrapatidar041@gmail.com"   
}

# Step 2: Generate webhook and token
generate_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
response = requests.post(generate_url, json=user_data)

if response.status_code != 200:
    print("Error generating webhook:", response.status_code, response.text)
    exit()

data = response.json()
webhook_url = data.get("webhook")
access_token = data.get("accessToken")

print("Webhook URL:", webhook_url)
print("Access Token:", access_token)

# Step 3: Prepare final SQL query
final_sql_query = """
SELECT
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    FLOOR(DATEDIFF(CURRENT_DATE, e.DOB) / 365.25) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE DAY(p.PAYMENT_TIME) != 1
ORDER BY p.AMOUNT DESC
LIMIT 1;
"""

# Step 4: Submit the final query
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}
payload = {
    "finalQuery": final_sql_query.strip()
}

submit_response = requests.post(webhook_url, headers=headers, json=payload)

# Step 5: Output submission result
if submit_response.status_code == 200:
    print("SQL query submitted successfully!")
else:
    print("Failed to submit SQL query:", submit_response.status_code, submit_response.text)
