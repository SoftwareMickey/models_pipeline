from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

# from django.views.decorators.csrf import csrf_exempt

from .pipefunctions import *
from .deployment_function import *

from django.conf import settings

import numpy as np
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
        df = dataloading(data=csv_file)
        
        print('----------------------------- CHECK MISSING VALUES --------------------------------------------')
        print(df.isnull().sum())
        
        # ? -> Data preprocessing
        X = df.drop(['median_house_value'], axis = 1).values
        y = df['median_house_value'].values
        
        # ? Start data processing
        X_transformed = preprocessing(X)
        
        print('Transformed completed>>>>')
        print(X_transformed) 
        
        # ? Handle missing values
        X_handled = handle_missing_values(X_transformed)
        
        print('Handling missing data completed>>>>')
        print(X_handled) 
        
        # ? Handle data split
        data_splited = split_data(X = X_handled, y = y)
        
        print('Data split completed>>>>')
        print(len(data_splited['X_train'])) 
        print(len(data_splited['X_test'])) 
        
        msg = {"msg": data_splited}
        return Response(msg, status=201)
    
    
# Todo : Create a class for model deployments
class DeploymentView(APIView):
    renderer_classes = [JSONRenderer]
    
    def get(self, request):
        data = {"msg" : "Get model deployment process parameters...!"}
        return Response(data, status=200)
    
    def post(self, request):
        
        post_data = request.body;
            
        predicted_value = deployment_json_conversion(post_data)
        
        print('Predicted Value: ' + str(predicted_value))
        
        return Response({
            "predicted_value" : predicted_value,
            "prediction_endpoint": request.build_absolute_uri('/api/predict/')
        },status=200)
    
class PredictionView(APIView):
    
    renderer_classes = [JSONRenderer]
    
    def get(self, request):
        data = {"msg" : 'Prediction has been set up and it is up and running...'}
        
        return Response(data)
    def post(self,request):
        data = request.body;
        json_data = json.loads(data)
        
        # * Load preprocessing script dynamically
        preprocessing_path = os.path.join(settings.BASE_DIR, 'pipelining', 'preprocessing_utils.py')
        spec = importlib.util.spec_from_file_location("preprocessing_utils", preprocessing_path)
        
        preprocessing_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(preprocessing_module)
        
        # Extract and preprocess the data
        model_data = preprocessing_module.accept_and_convert_data(json_data, np)
        reshaped_model_data = preprocessing_module.reshaped_data(model_data, np)

         # Load the saved model
        model_path = os.path.join('../pipelining/housing_prediction_model.h5')
        model = tf.keras.models.load_model(model_path)

        # Make predictions
        prediction = model.predict(reshaped_model_data)

        # Return the predictions
        return Response({'prediction': prediction.tolist()}, status=status.HTTP_200_OK)