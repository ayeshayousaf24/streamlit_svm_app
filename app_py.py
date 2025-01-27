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
    # Example user inputs for prediction (replace with your actual input logic)
    Gender = st.selectbox("Gender", ['Male', 'Female'])
    Age = st.slider("Age", 18, 100)
    Estimated_salary = st.slider("Estimated Salary", 0, 100000)

    #Predicted Code
    if st.button('Predict'):
        makeprediction = model.predict([[Gender, Age, Estimated_salary]])
        output = round(makeprediction[0], 2)
        if st.success(makeprediction):  # Replace 'condition' with your actual condition
            st.success('This user can buy the product', format(output))
        else:
            st.error('This user cannot buy the product', format(output))

if __name__ == '__main__':
    main()
