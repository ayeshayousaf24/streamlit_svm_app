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

    if model:
        # Get user input for prediction
        st.title("Product Purchase Prediction")
        
        Gender = st.selectbox("Select Gender", ['Male', 'Female'])
        
        # Creating selectboxes for age and salary ranges instead of sliders
        Age = st.selectbox("Select Age Range", ['18-30', '31-40', '41-50', '51-60', '61+'])
        Estimated_salary = st.selectbox("Select Estimated Salary Range", ['0-20K', '20K-40K', '40K-60K', '60K-80K', '80K+'])
        
        # Convert gender to numerical values
        gender_value = 0 if Gender == 'Male' else 1

        # Converting Age and Salary to numeric values for the model
        age_mapping = {'18-30': 25, '31-40': 35, '41-50': 45, '51-60': 55, '61+': 65}
        salary_mapping = {'0-20K': 10000, '20K-40K': 30000, '40K-60K': 50000, '60K-80K': 70000, '80K+': 90000}
        
        # Convert selected ranges to numeric
        Age = age_mapping[Age]
        Estimated_salary = salary_mapping[Estimated_salary]

        # Make prediction when the button is pressed
        if st.button('Predict'):
            try:
                prediction = model.predict([[gender_value, Age, Estimated_salary]])
                
                # Display results with a more user-friendly output
                if prediction == 1:
                    st.success("This user can buy the product!")
                else:
                    st.error("This user cannot buy the product.")
            except Exception as e:
                st.error(f"Error during prediction: {e}")

if __name__ == '__main__':
    main()
