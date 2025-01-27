import joblib
import requests
import io
import streamlit as st

# Function to load the model
def load_model():
    model_url = 'https://raw.githubusercontent.com/ayeshayousaf24/streamlit_svm_app/main/svm_model.pkl'
    
    # Download the model file
    response = requests.get(model_url)
    
    if response.status_code == 200:
        try:
            # Load the model using joblib from the raw content of the response
            model = joblib.load(io.BytesIO(response.content))
            st.success("Model loaded successfully!")
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
    
    # Proceed if the model is loaded successfully
    if model:
        # Get user input (replacing sliders with text input)
        Gender = st.selectbox("Gender", ['Male', 'Female'])
        Age = st.number_input("Age", 18, 100)
        Estimated_salary = st.number_input("Estimated Salary", 0, 100000)

        # Predicted Code
        if st.button('Predict'):
            # Make prediction
            # Convert 'Gender' to numeric (1 for Male, 0 for Female)
            Gender = 1 if Gender == 'Male' else 0

            # Ensure 'Age' and 'Estimated_salary' are integers or floats
            Age = int(Age)
            Estimated_salary = float(Estimated_salary)

            # Make prediction
            prediction = model.predict([[Gender, Age, Estimated_salary]])

            output = round(prediction[0], 2)
            if st.success(prediction):
                st.write(f"Prediction: This user can buy the product")
            else:
                st.write(f"Prediction: This user cannot buy the product")
        else:
            st.error("Model failed to load.")

if __name__ == '__main__':
    main()
