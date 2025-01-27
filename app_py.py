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
    # Set page title and layout
    st.set_page_config(page_title="Product Purchase Prediction", page_icon="📊", layout="centered")

    # Custom styling to enhance design with colors
    st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f1f8e9;  /* Light Green Background */
        color: #333;
    }
    .main-container {
        background-color: #ffffff; /* White Background for the card */
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        margin-top: 30px;
    }
    .header {
        color: #388e3c;  /* Green header */
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .subheader {
        color: #1b5e20;  /* Dark Green for the subheading */
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 30px;
    }
    .selectbox, .number_input {
        font-size: 1.2rem;
        margin-top: 10px;
        width: 100%;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #81c784;  /* Light Green border */
        background-color: #c8e6c9;  /* Very light green background */
    }
    .predict-btn {
        background-color: #4caf50;  /* Green button */
        color: white;
        font-size: 1.3rem;
        border: none;
        padding: 12px 25px;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-top: 20px;
    }
    .predict-btn:hover {
        background-color: #388e3c;  /* Darker green on hover */
    }
    .prediction-result {
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        margin-top: 20px;
    }
    .success {
        color: #388e3c;  /* Green for success */
    }
    .failure {
        color: #d32f2f;  /* Red for failure */
    }
    </style>
    """, unsafe_allow_html=True)

    # Load the model
    model = load_model()

    # Proceed if the model is loaded successfully
    if model:
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="header">Product Purchase Prediction</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subheader">Please enter the details to predict if a user can buy the product.</p>', unsafe_allow_html=True)
        
        # Get user input (replacing sliders with selectbox and number input)
        Gender = st.selectbox("Select Gender", ['Male', 'Female'])
        Age = st.number_input("Enter Age", min_value=0, max_value=100, step=1, value=25)
        Estimated_salary = st.number_input("Enter Estimated Salary", min_value=0, max_value=100000, step=5000, value=30000)

        # Create a prediction button
        if st.button('Make Prediction', key="predict"):
            
            # Convert 'Gender' to numeric (1 for Male, 0 for Female)
            Gender = 1 if Gender == 'Male' else 0

            # Ensure 'Age' and 'Estimated_salary' are integers or floats
            Age = int(Age)
            Estimated_salary = float(Estimated_salary)

            # Make prediction
            prediction = model.predict([[Gender, Age, Estimated_salary]])
            
            # Display results with a personalized message
            st.markdown('<p class="prediction-result">Prediction:</p>', unsafe_allow_html=True)
            if prediction == 1:
                st.markdown('<p class="prediction-result success">This user can buy the product! 🎉</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="prediction-result failure">This user cannot buy the product. 😞</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
