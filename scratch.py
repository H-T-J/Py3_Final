import requests as req

url = "http://10.6.21.76:8000"

email = "1"
password = "1"

response = req.get(f"{url}/tasks?auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaWQiOjcsImV4cCI6MTcwNTAyOTEwOX0.L74TOwqBq7EP3zIkSO0kxrB-UqP54xnnSRBRx_xgO44",
                    headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaWQiOjcsImV4cCI6MTcwNTAyOTEwOX0.L74TOwqBq7EP3zIkSO0kxrB-UqP54xnnSRBRx_xgO44',
                            'Content-Type': 'application/json'}
                   ).json()
print(response)
