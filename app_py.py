import pickle
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
            # Load the model from the raw content of the response
            model = pickle.load(io.BytesIO(response.content))
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
        # Example user inputs for prediction (replace with your actual input logic)
        Gender = st.selectbox("Gender", ['Male', 'Female'])
        Age = st.slider("Age", 18, 100)
        Estimated_salary = st.slider("Estimated Salary", 0, 100000)

        # Make prediction if all inputs are valid
        if Gender and Age and Estimated_salary:
            if Gender == 'Male':
                Gender = 1  # Assuming Male = 1 and Female = 0 for the model input
            else:
                Gender = 0  # Female = 0
            
            # Make prediction with the model
            prediction = model.predict([[Gender, Age, Estimated_salary]])
            
            st.write(f"Prediction: {prediction}")
        else:
            st.error("Please provide all inputs.")
    else:
        st.error("Model is not loaded. Please try again.")

# Run the Streamlit app
if __name__ == '__main__':
    main()
