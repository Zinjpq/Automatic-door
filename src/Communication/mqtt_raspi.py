import requests

url = "http://192.168.3.68:5000/display"
data = {
    "message": "Chao Vinh "
}

response = requests.post(url, json=data)

print("Response:", response.json())
