import requests

# Define the API endpoint
url = 'http://localhost:11434/api/generate'

# Define your payload here. Adjust this based on the API's expected input.
# For example, if the API expects JSON, you might need something like:
# payload = {"key": "value"}
payload = { 
            "model": "codellama", 
            "prompt" : "why is the sky blue?"
        }

# Make a GET request (or POST if required) and print the response
try:
    response = requests.post(url, params=payload)
    response.raise_for_status()  # Raise an error for bad responses
    print('Success!')
    print('Response:', response.text)
except requests.exceptions.HTTPError as errh:
    print("Http Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    print("OOps: Something Else", err)
