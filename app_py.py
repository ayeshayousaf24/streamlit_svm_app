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
        # Get user input (replacing sliders with text input)
        Gender = st.selectbox("Gender", ['Male', 'Female'])
        
        try:
            Age = int(st.text_input("Enter Age (18-100)", ""))
            Estimated_salary = float(st.text_input("Enter Estimated Salary (0-100000)", ""))
            
            if Age < 18 or Age > 100:
                st.error("Please enter a valid Age between 18 and 100.")
                return
            if Estimated_salary < 0 or Estimated_salary > 100000:
                st.error("Please enter a valid Estimated Salary between 0 and 100000.")
                return
            
            # Proceed with prediction
            if st.button('Predict'):
                # Convert gender to binary (1 for Male, 0 for Female)
                Gender = 1 if Gender == 'Male' else 0
                
                # Make the prediction
                try:
                    prediction = model.predict([[Gender, Age, Estimated_salary]])
                    output = round(prediction[0], 2)
                    st.success(f"Prediction: {output}")
                    
                    # Display result based on prediction
                    if output == 1:
                        st.write('This user can buy the product.')
                    else:
                        st.write('This user cannot buy the product.')
                except Exception as e:
                    st.error(f"Error during prediction: {e}")
        
        except ValueError:
            st.error("Please enter valid numeric values for Age and Estimated Salary.")
    else:
        st.error("Model is not loaded. Please try again.")

if __name__ == '__main__':
    main()
