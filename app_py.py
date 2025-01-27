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
            st.success("Model loaded successfully!", icon="✅")
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
    st.set_page_config(page_title="Product Purchase Prediction", page_icon="📊", layout="wide")

    # Custom styling to enhance design
    st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f5f5f5;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .header {
        color: #4CAF50;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 10px;
    }
    .subheader {
        color: #555;
        font-size: 1.4rem;
        text-align: center;
        margin-bottom: 20px;
    }
    .selectbox, .number_input {
        font-size: 1.2rem;
        margin-top: 10px;
        width: 100%;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #ddd;
        background-color: #f9f9f9;
    }
    .prediction-button {
        background-color: #4CAF50;
        color: white;
        font-size: 1.2rem;
        border: none;
        padding: 12px 25px;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .prediction-button:hover {
        background-color: #45a049;
    }
    .prediction-result {
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        margin-top: 20px;
    }
    .success {
        color: #388e3c;
    }
    .failure {
        color: #d32f2f;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load the model
    model = load_model()

    # Proceed if the model is loaded successfully
    if model:
        st.markdown('<div class="main">', unsafe_allow_html=True)
        st.markdown('<h1 class="header">Welcome to the Product Purchase Predictor</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subheader">Please provide the information below to make a prediction.</p>', unsafe_allow_html=True)
        
        # Get user input (replacing sliders with selectbox and number input)
        Gender = st.selectbox("Select Gender", ['Male', 'Female'], index=0, key="gender", help="Select the gender of the user", 
                              label_visibility="visible", format_func=lambda x: f"{x}", 
                              use_container_width=True, css_class="selectbox")

        Age = st.number_input("Enter Age", min_value=0, max_value=100, step=1, value=25, key="age", 
                              label_visibility="visible", help="Enter the user's age", 
                              format="%.0f", css_class="number_input")

        Estimated_salary = st.number_input("Enter Estimated Salary", min_value=0, max_value=100000, step=5000, value=30000, 
                                           key="salary", label_visibility="visible", help="Enter the estimated salary of the user", 
                                           format="%.2f", css_class="number_input")

        # Create a prediction button
        if st.button('Make Prediction', key="predict", help="Click here to predict the result", 
                     use_container_width=True, css_class="prediction-button"):
            
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
