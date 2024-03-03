from django.http import HttpResponse
import requests
import json

def execute_code(request):
    source_code = 'print("Hi eyad")'
    data = {
        "source_code": source_code,
        "language_id": 71,  # Language ID for Python (3.8.1) on Judge0. Adjust as needed.
    }
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": "87fd2cc807msh7051d0b41695714p174167jsn415607492296",  # Replace with your actual RapidAPI key.
        "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
    }
    response = requests.post(
        'https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=false&wait=true',
        headers=headers,
        data=json.dumps(data)
    )
    if response.status_code == 200:
        print()
        result = response.json()
        output = result['stdout']
        return HttpResponse(f"{output}")
    else:
        return HttpResponse("Error executing code")

