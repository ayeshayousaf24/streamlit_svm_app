import pickle
import requests
import io
import streamlit as st
import numpy as np

# Function to load the model
def load_model():
    model_url = 'https://raw.githubusercontent.com/ayeshayousaf24/streamlit_svm_app/main/svm_model.pkl'
    
    # Download the model file
    response = requests.get(model_url)
    
    if response.status_code == 200:
        try:
            # Load the model from the raw content of the response
            model = pickle.load(io.BytesIO(response.content))
            st.success("Model loaded successfully!")
            
            # Debugging step: Check the type of the loaded object
            if not hasattr(model, 'predict'):
                st.error("The loaded object is not a valid model. It does not have a 'predict' method.")
                return None
            return model
        except Exception as e:
            st.error(f"Error loading model: {e}")
            return None
    else:
        st.error(f"Failed to download the model. Status code: {response.status_code}")
        return None

# Main function to run the app
def main():
    # Load the model
    model = load_model()

    if model:
        # Get user input (replace sliders with text input)
        Gender = st.selectbox("Gender", ['Male', 'Female'])
        Age = st.number_input("Age", min_value=18, max_value=100)
        Estimated_salary = st.number_input("Estimated Salary", min_value=0, max_value=100000)

        # Convert Gender to numeric value (1 for Male, 0 for Female)
        Gender = 1 if Gender == 'Male' else 0

        # Ensure Age and Estimated Salary are numeric
        Age = int(Age)
        Estimated_salary = float(Estimated_salary)

        # Prediction logic
        if st.button('Predict'):
            try:
                prediction = model.predict([[Gender, Age, Estimated_salary]])
                output = round(prediction[0], 2)
                st.success(f"Prediction: {output}")
            except Exception as e:
                st.error(f"Error during prediction: {e}")
if __name__ == '__main__':
    main()
