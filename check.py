import requests
import json

MISTRAL_API_KEY = "jZ1CYYXmueeHFl1yMWjfaWQNV0P2TaWH"  # Replace with your key

def test_mistral_small():
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mistral-small",  # Change this if needed
        "messages": [{"role": "user", "content": "Hello! Can you summarize what Mistral AI does?"}]
    }

    response = requests.post(url, headers=headers, json=data)
    
    try:
        response_json = response.json()        
        print("\nMistral AI says:", response_json["choices"][0]["message"]["content"])
    except Exception as e:
        print("Error:", e)
        print("Raw Response:", response.text)

# Run the test
test_mistral_small()
