from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

# from django.views.decorators.csrf import csrf_exempt

from .pipefunctions import *

# Create your views here.

class MyApiView(APIView):
    renderer_classes = [JSONRenderer] 
    
    def get(self, request):
        print("GET request has been received and It's being processed...!")
        print()
        data = {"message": "Send a POST request with a CSV file to this endpoint."}
        return Response(data, status=200)

    def post(self, request):
        print("POST request has been received and It's being processed...!")
        
        if 'file' not in request.FILES:
            return JsonResponse({"error": "No file provided"}, status=400)
        
        csv_file = request.FILES['file']

        # Check if the uploaded file is a CSV
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({"error": "File is not a CSV"}, status=400)
        
        # Call the dataloading function here
        dataloading(data=csv_file)
        
        msg = {"msg": "This is data pipelining with Vector technologies"}
        return Response(msg, status=201)
    
    # def PipeliningIntroduction(request):
        
    #     if request.method == 'GET':
    #         print("GET request has been received and It's being processed...!")
            
    #         if 'file' not in request.FILES:
    #             return JsonResponse({"error": "No file provided"}, status=400)
            
    #         csv_file = request.FILES['file']

    #         # Check if the uploaded file is a CSV
    #         if not csv_file.name.endswith('.csv'):
    #             return JsonResponse({"error": "File is not a CSV"}, status=400)
            
    #         dataloading(data=csv_file)
            
    #         msg = {"msg" : "This is data pipelining with Vector technologies"}
            
    #         return Response(msg, status = status.HTTP_201_CREATED)