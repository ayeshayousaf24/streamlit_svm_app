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

    # Custom background color using markdown
    st.markdown("""
    <style>
    body {
        background-color: #D1E8E2;  /* Soft Blue background */
    }
    </style>
    """, unsafe_allow_html=True)

    # Load the model
    model = load_model()

    # Proceed if the model is loaded successfully
    if model:
        st.title("Product Purchase Prediction")
        
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
            if prediction == 1:
                st.success("This user can buy the product! 🎉")
            else:
                st.error("This user cannot buy the product. 😞")

if __name__ == '__main__':
    main()
