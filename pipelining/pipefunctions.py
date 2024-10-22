from django.http import JsonResponse
import sklearn

import pandas as pd
import numpy as np

# * Data loading and csv handling
def dataloading(data):
    print()
    print('----------------------------- FILE PROCESSING ----------------------------------------')
    
    try:
           df = pd.read_csv(data)
           return df
    except Exception as e:
        # Handle any errors that occur during processing
        return JsonResponse({"error": str(e)}, status=500)
       
    
# * Function to do data preprocessing
def preprocessing(X):
    
    print()
    print('-------------------------------- DATA PREPROCESSING -------------------------------------------')
    
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder
    
    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [-1])], remainder='passthrough')
    ct = ct.fit(X)
    
    X_transformed = ct.transform(X)   
    return X_transformed

# * handling missing data function
def handle_missing_values(X):
    
    from sklearn.impute import SimpleImputer
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    
    imputer = imputer.fit(X)
    X_handled = imputer.transform(X)
    return X_handled

# * handling training and testing data splitation
def split_data(X, y):
    
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Return the data in a dictionary
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test
    }