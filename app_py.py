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
        # Get user input for prediction (Text inputs for a more intuitive experience)
        st.title("Product Purchase Prediction")
        
        Gender = st.selectbox("Select Gender", ['Male', 'Female'])
        Age = st.text_input("Enter Age", "")
        Estimated_salary = st.text_input("Enter Estimated Salary", "")
        
        if Age and Estimated_salary:
            # Convert the inputs to the appropriate types
            try:
                Age = int(Age)
                Estimated_salary = float(Estimated_salary)
            except ValueError:
                st.error("Please enter valid numerical values for Age and Estimated Salary.")
                return

            # Make prediction when the button is pressed
            if st.button('Predict'):
                try:
                    # Ensure the gender input is converted to a numerical value
                    gender_value = 0 if Gender == 'Male' else 1
                    prediction = model.predict([[gender_value, Age, Estimated_salary]])
                    
                    # Display results with a more user-friendly output
                    if prediction == 1:
                        st.success("This user can buy the product!")
                    else:
                        st.error("This user cannot buy the product.")
                except Exception as e:
                    st.error(f"Error during prediction: {e}")
        else:
            st.warning("Please enter both Age and Estimated Salary.")

if __name__ == '__main__':
    main()
