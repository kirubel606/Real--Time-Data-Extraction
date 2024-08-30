import requests
import json

# Webhook registration details
url = "http://dev.inkomoko.com:1055/register_webhook"
payload = json.dumps({
    "url": "https://your-hosted-flask-app-url/api"
})
headers = {'Content-Type': 'application/json'}

# Register the webhook
response = requests.post(url, headers=headers, data=payload)

# Check the response
if response.status_code == 200:
    print("Webhook registered successfully.")
else:
    print(f"Failed to register webhook: {response.status_code}, {response.text}")
