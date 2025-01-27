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
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    .header {
        color: #4a90e2;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .subheader {
        color: #555;
        font-size: 1.3rem;
    }
    .prediction-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ff5722;
    }
    .prediction-result {
        font-size: 1.5rem;
        font-weight: bold;
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
        
        # Get user input (replacing sliders with text input)
        Gender = st.selectbox("Select Gender", ['Male', 'Female'], index=0)
        Age = st.number_input("Enter Age", min_value=0, max_value=100, step=1, value=25)
        Estimated_salary = st.number_input("Enter Estimated Salary", min_value=0, max_value=100000, step=5000, value=30000)
        
        # Create a prediction button
        if st.button('Make Prediction'):
            # Convert 'Gender' to numeric (1 for Male, 0 for Female)
            Gender = 1 if Gender == 'Male' else 0

            # Ensure 'Age' and 'Estimated_salary' are integers or floats
            Age = int(Age)
            Estimated_salary = float(Estimated_salary)

            # Make prediction
            prediction = model.predict([[Gender, Age, Estimated_salary]])
            
            # Display results with a personalized message
            st.markdown('<p class="prediction-text">Prediction:</p>', unsafe_allow_html=True)
            if prediction == 1:
                st.markdown('<p class="prediction-result" style="color: green;">This user can buy the product! 🎉</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="prediction-result" style="color: red;">This user cannot buy the product. 😞</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
