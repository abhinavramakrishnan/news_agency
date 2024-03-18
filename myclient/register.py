import requests
import json

details_json = {
    "agency_name": "Abhinav Ramakrishnan News Agency",
    "url" : "https://sc21a2r.pythonanywhere.com",
    "agency_code" : "AR02"
}

# Send POST request to stories API endpoint with story data in JSON format
response = requests.post("https://newssites.pythonanywhere.com/api/directory/", json=details_json)

print(response.status_code)

print(response.text)