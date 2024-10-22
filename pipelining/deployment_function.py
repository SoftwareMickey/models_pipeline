import json
import requests
import tensorflow as tf
import os
import importlib.util
import sys
import numpy as np

def deployment_json_conversion(data):
    print()
    print('------------------------------- CONVERSION TO JSON -------------------------------------------')
    
    file_data = json.loads(data)
    
    folder_name = os.path.abspath('pipelining')
    # Ensure the folder exists (create if necessary)
    os.makedirs(folder_name, exist_ok=True)
    
    for data in file_data:
        for files in data:
            
            # * Iterate over dictionary to check if a .h5 file is found
            # print(files)
            if files['name'].endswith('.h5'):
                print(f"Found .h5 file: {files['name']}")
                
                download_url = files['download_url']
                local_filename = os.path.join(folder_name,files['name'])
                
            # * Check if there is a python file for preprocessing
            if files['name'].endswith('.py'):
                print(f"Found .py file: {files['name']}")
                
                py_download_url = files['download_url']
                py_local_filename = os.path.join(folder_name,files['name'])
    
    print('Download URL: ' + str(download_url))
    print('Python File Download URL: ' + str(py_download_url))
    
    
    # Todo: After getting the download try downloading files

    # Send a GET request to the URL
    response = requests.get(download_url)
    py_response = requests.get(py_download_url)

    # # Write the file to your local system
    try:
        with open(local_filename, 'wb') as f:
            f.write(response.content)
            
        with open(py_local_filename, 'wb') as f:
            f.write(py_response.content)

        print(f"{local_filename} has been downloaded.") 
        print(f"{py_local_filename} has been downloaded.")
        
        
        # ? Try to load processing modules dynamically
        # Adding the pipelining folder to the system path so Python can find the module
        sys.path.append(folder_name)

        # Importing preprocessing_utils dynamically after downloading
        module_name = py_local_filename
        module_path = os.path.join(folder_name, f"{module_name}")

        # Load the module using importlib
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        preprocessing_utils = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(preprocessing_utils)

        # Now you can use the imported module
        print("Module preprocessing_utils imported successfully.")
        
        predicted_value = loadModel(model_file_path=local_filename, processing_file=preprocessing_utils)
        return predicted_value
    except Exception as e:
        print(e)


# Todo : After the file has been downloaded try reading it's content
def loadModel(model_file_path, processing_file):
    
    prediction_data = {
        "longitude": -122.23,
        "latitude": 37.88,
        "housing_median_age": 41,
        "total_rooms": 880,
        "total_bedrooms": 129,
        "population": 322,
        "households": 126,
        "median_income": 8.3252,
        "ocean_proximity": "NEAR BAY"
    }

    
    data = processing_file.accept_and_convert_data(prediction_data, np)
    reshaped_model_data = processing_file.reshaped_data(data, np)
    
    print('Reshaped Data: ' + str(reshaped_model_data))
    
    model = tf.keras.models.load_model(model_file_path)
    prediction = model.predict(reshaped_model_data)
    
    return prediction[0][0]