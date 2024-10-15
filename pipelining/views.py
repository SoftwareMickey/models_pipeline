from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .pipefunctions import *

# Create your views here.
@csrf_exempt
def PipeliningIntroduction(request):
    
    if request.method == 'POST':
        print("Post request has been received and It's being processed...!")
        
        if 'file' not in request.FILES:
            return JsonResponse({"error": "No file provided"}, status=400)
        
        csv_file = request.FILES['file']

        # Check if the uploaded file is a CSV
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({"error": "File is not a CSV"}, status=400)
        
        dataloading(data=csv_file)
        
    return JsonResponse({"msg" : "This is data pipelining with Vector technologies"})