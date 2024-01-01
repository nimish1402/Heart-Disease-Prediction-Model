import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Function to preprocess input data (same as in your original code)
def preprocess_input_data(input_data, reference_columns):
    input_data = pd.get_dummies(input_data)
    missing_cols = set(reference_columns) - set(input_data.columns)
    for col in missing_cols:
        input_data[col] = 0
    input_data = input_data[reference_columns]
    return input_data

# Function to predict patient outcome
def predict_patient(patient_data, patient_id):
    selected_patient = patient_data.loc[patient_data['Id'] == int(patient_id)]

    if not selected_patient.empty:
        # Extract features from the selected patient
        features = selected_patient.drop(['Id', 'Name'], axis=1)

        # Ensure that the columns match the ones used during training
        features = preprocess_input_data(features, X.columns)

        # Make predictions for the selected patient
        prediction = clf.predict(features)
        patient_name = selected_patient['Name'].values[0]
        return prediction, patient_name, features
    else:
        return None

# Function to compare and write disease progression
def compare_and_write_progression(patient_row, past_report_data):
   
    result = {}

    for column in patient_row.columns:
        if column not in ['Id', 'Name']:  # Exclude non-relevant columns
            current_value = patient_row[column].values[0]
            past_value = past_report_data[column].values[0] if column in past_report_data.columns else None

            if current_value != past_value:
                comparison = f'Different values (Current: {current_value}, Past: {past_value})'
                percentage_change = None  # You can calculate percentage change if applicable
            else:
                comparison = f'Same values (Current: {current_value}, Past: {past_value})'
                percentage_change = 0  # Placeholder, you can calculate this based on your specific metrics

            result[column] = {'Comparison': comparison, 'Percentage': percentage_change}

    return result


# Load the dataset
heart_data = pd.read_csv('heart1.csv')

# Prepare the data
X = heart_data.drop('HeartDisease', axis=1)
y = heart_data['HeartDisease']

# Convert categorical variables into dummy/indicator variables
X = pd.get_dummies(X)

# Split the dataset into training and testing sets
_, X_test, _, _ = train_test_split(X, y, test_size=0.8, random_state=42)

# Initialize the Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
clf.fit(X, y)

st.title("🏥 Heart Disease Prediction Chatbot")

# Initialize variables
patient_data = None
prediction_result = None

# Main chatbot loop

user_input = st.text_input("👩‍⚕️ Your command:", key="command_input")

if user_input == 'my patients':
        uploaded_file = st.file_uploader("📂 Upload patients' data (Excel file):", type=["xlsx", "xls"], key="patients_file")
        if uploaded_file:
            try:
                patient_data = pd.read_excel(uploaded_file)
                st.success("🎉 Patients' data loaded successfully.")
            except Exception as e:
                st.error(f"❌ Error loading patients' data: {e}")

elif user_input == 'predict':
        if patient_data is None:
            st.warning("🚨 Please load your patients' data first using the 'my patients' command.")
        else:
            patient_id = st.number_input("🔍 Enter the patient's ID for prediction:", value=1, step=1, key="patient_id_input")
            prediction_result = predict_patient(patient_data, patient_id)
            prediction = None

            if prediction_result:
                prediction, patient_name, selected_patient_processed = prediction_result
                st.success(f"🎉 Prediction for Patient {patient_id} ({patient_name}) is processed. To see the details, type 'show results'.")
                next_question = st.text_input("🤔 What is your next question?", key="next_question_input")
                st.success(f"🎉 Your next question: {next_question}")
                
elif user_input == 'show results':
        if prediction_result:
            if prediction[0] == 1:
                st.error(f"❗ The patient ({patient_name}) with ID {patient_id} may have heart disease. Further evaluation is recommended.")

                # Continue with the rest of your code for generating the personalized report
                # ...

            elif prediction[0] == 0:
                st.success(f"✅ The patient ({patient_name}) with ID {patient_id} seems to be healthy. However, consult a healthcare professional for confirmation.")
            else:
                st.warning("🚨 No prediction available. Please run 'predict' first.")
        else:
            st.warning("🚨 No prediction available. Please run 'predict' first.")

elif "progress" in user_input.lower():
        uploaded_patient_file = st.file_uploader("📂 Upload patient data (Excel file):", type=["xlsx", "xls"], key="progress_patient_file")
        uploaded_past_report_file = st.file_uploader("📂 Upload past report data (Excel file):", type=["xlsx", "xls"], key="progress_past_report_file")

        if uploaded_patient_file and uploaded_past_report_file:
            try:
                patient_data = pd.read_excel(uploaded_patient_file)
                past_report_data = pd.read_excel(uploaded_past_report_file)

                patient_id = st.number_input("🔍 Which patient ID do you want to see the disease progression of?", value=1, step=1, key="progress_patient_id_input")

                patient_row = patient_data.loc[patient_data['Id'] == int(patient_id)]

                if not patient_row.empty:
                    patient_name = patient_row['Name'].values[0]
                    past_report_data = past_report_data.loc[past_report_data['Id'] == int(patient_id)]
                    result = compare_and_write_progression(patient_row, past_report_data)

                    show_results = st.radio(f"📊 The results for {patient_name} (ID: {patient_id}) are ready. Would you like to see them?", ('Yes', 'No'), key="progress_show_results_input")

                    if show_results == "Yes":
                        st.success("🎉 Showing the results.")
                        for key, value in result.items():
                            st.write(f'{key}: {value["Comparison"]}, Percentage Change: {value["Percentage"]}%')
                    else:
                        st.info("🤔 How else can I assist you, doc?")
                else:
                    st.warning(f"❌ Patient with ID {patient_id} not found.")
                    st.info("🤔 How else can I assist you, doc?")
            except Exception as e:
                st.error(f"❌ Error processing progression data: {e}")
        else:
            st.warning("🚨 Please upload both patient and past report data files.")

elif user_input == 'exit':
        st.warning("🚪 Exiting the chatbot. Goodbye!")
      

else:
        st.warning(f"🚨 Invalid command: {user_input}. Please type 'my patients' to load patients' data, 'predict' to make predictions, 'show results' to see the details, 'progress' to check disease progression, or 'exit' to exit.")
