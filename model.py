import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
import pickle

df = pd.read_csv('room_prices_dataset.csv')

df['Sea Facing'] = df['Sea Facing'].fillna('No View')

X = df[['Room Type', 'Sea Facing', 'Jacuzzi', 'Balcony', 'Bed Type', 'In-Room Technology', 'Season', 'Floor Level']]
y = df['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

categorical_features = ['Room Type', 'Sea Facing', 'Jacuzzi', 'Balcony', 'Bed Type', 'In-Room Technology', 'Season']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', LinearRegression())
])

pipeline.fit(X_train, y_train)

with open('price_prediction_model.pkl', 'wb') as model_file:
    pickle.dump(pipeline, model_file)

print("Model saved as 'price_prediction_model.pkl'")


import pickle

# Load the saved model
with open('price_prediction_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define a function to prepare input data
def prepare_input(input_data):
    df = pd.DataFrame([input_data])
    return df

# Hardcoded input data for prediction
input_data = {
    'Room Type': 'Suite',
    'Sea Facing': 'Yes',
    'Jacuzzi': 'No',
    'Balcony': 'Yes',
    'Bed Type': 'King',
    'In-Room Technology': 'Smart TV',
    'Season': 'Peak',
    'Floor Level': 5
}

try:
    # Prepare the input data
    input_df = prepare_input(input_data)
    
    # Predict price
    predicted_price = model.predict(input_df)[0]
    
    print(f"Predicted Price: ${round(predicted_price, 2)}")
    
except Exception as e:
    print(f"An error occurred: {e}")