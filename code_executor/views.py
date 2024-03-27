from django.http import HttpResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def execute_code(request):

    data = json.loads(request.body)


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

# views.py (Django Backend)
# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def execute_code(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
    
#     try:
#         data = json.loads(request.body)
#         print(data)
#         source_code = data.get('source_code', '')
#         source_code="print(')"
        
#         # IMPORTANT: Here you should execute the code in a safe, secure manner.
#         # The following line is a placeholder and should not be used in production.
#         output = "Simulated execution output: " + source_code
#         print(output)
        
#         return JsonResponse({
#             'stdout': output,
#             'stderr': '',
#             'returncode': 0
#         })
#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON'}, status=400)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)