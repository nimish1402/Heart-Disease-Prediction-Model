import streamlit as st
import pandas as pd
import os

# Function to preprocess input data
def preprocess_input_data(data):
    # Your preprocessing logic here
    # For simplicity, let's assume it just returns the input data for now
    return data

# Function to compare patient reports
def compare_reports(new_patient_data_processed, healthy_patient_data):
    # Your comparison logic here
    # This function will compare each feature of the new patient with a healthy patient
    mismatch_columns = ['ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']

    for col in mismatch_columns:
        value_new_patient = new_patient_data_processed[col].values[0]
        value_healthy_patient = healthy_patient_data[col].values[0]

        if value_new_patient != value_healthy_patient:
            st.write(f'Mismatch in {col}: Different values')
            st.write(f'  New Patient: {value_new_patient}, Healthy Patient: {value_healthy_patient}')
        else:
            st.write(f'Match in {col}: Same values')

# Function to clear input fields
def clear_input_fields(patient_counter):
    st.text_input(f"👤 Name of the patient {patient_counter}:")
    st.number_input(f"🎂 Age {patient_counter}:", value=0)
    st.selectbox(f"🚻 Sex {patient_counter}", ['Male', 'Female'])
    st.number_input(f"🫀 Chest Pain Type {patient_counter}:", value=0)
    st.number_input(f"🩸 Resting Blood Pressure {patient_counter}:", value=0)
    st.number_input(f"📈 Cholesterol {patient_counter}:", value=0)
    st.number_input(f"🍬 Fasting Blood Sugar {patient_counter}:", value=0)
    st.number_input(f"📊 Resting Electrocardiographic Results {patient_counter}:", value=0)
    st.number_input(f"💓 Maximum Heart Rate Achieved {patient_counter}:", value=0)
    st.selectbox(f"🏃 Exercise-Induced Angina {patient_counter}", ['No', 'Yes'])
    st.number_input(f"📉 ST Depression Induced by Exercise Relative to Rest {patient_counter}:", value=0.0)
    st.number_input(f"📈 Slope of the Peak Exercise ST Segment {patient_counter}:", value=0)

# Initialize patient counter
patient_counter = 1

# Load existing patient data from the file if it exists
existing_patient_data = pd.DataFrame()
file_path = 'manual_patients.xlsx'

if os.path.exists(file_path):
    existing_patient_data = pd.read_excel(file_path)

# Streamlit introduction
st.title("🏥 Patient Data Assistant")

# Streamlit Sidebar
user_choice = st.sidebar.radio("🚀 Select an option", ("Add patient data", "Exit"))

# Main Content
if user_choice == 'Add patient data':
    st.header(f"Enter Information for Patient {patient_counter}:")

    # Use st.columns to create two columns
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(f"👤 Name of the patient {patient_counter}:", key=f"name_{patient_counter}")
        age = st.number_input(f"🎂 Age {patient_counter}:", value=0)
        sex = st.selectbox(f"🚻 Sex {patient_counter}", ['Male', 'Female'])
        chest_pain_type = st.number_input(f"🫀 Chest Pain Type {patient_counter}:", value=0)
        resting_bp = st.number_input(f"🩸 Resting Blood Pressure {patient_counter}:", value=0)
        cholesterol = st.number_input(f"📈 Cholesterol {patient_counter}:", value=0)

    with col2:
        fasting_bs = st.number_input(f"🍬 Fasting Blood Sugar {patient_counter}:", value=0)
        resting_ecg = st.number_input(f"📊 Resting Electrocardiographic Results {patient_counter}:", value=0)
        max_hr = st.number_input(f"💓 Maximum Heart Rate Achieved {patient_counter}:", value=0)
        exercise_angina = st.selectbox(f"🏃 Exercise-Induced Angina {patient_counter}", ['No', 'Yes'])
        oldpeak = st.number_input(f"📉 ST Depression Induced by Exercise Relative to Rest {patient_counter}:", value=0.0)
        st_slope = st.number_input(f"📈 Slope of the Peak Exercise ST Segment {patient_counter}:", value=0)

    if st.button("💾 Save"):
        new_patient_df = pd.DataFrame({
            'ID': [patient_counter],
            'Name': [name],
            'Age': [age],
            'Sex': [sex],
            'ChestPainType': [chest_pain_type],
            'RestingBP': [resting_bp],
            'Cholesterol': [cholesterol],
            'FastingBS': [fasting_bs],
            'RestingECG': [resting_ecg],
            'MaxHR': [max_hr],
            'ExerciseAngina': [1 if exercise_angina == 'Yes' else 0],
            'Oldpeak': [oldpeak],
            'ST_Slope': [st_slope]
        })

        existing_patient_data = pd.concat([existing_patient_data, new_patient_df], ignore_index=True)
        existing_patient_data.to_excel(file_path, index=False)
        st.success(f"🎉 Patient {patient_counter}'s information saved.")
        patient_counter += 1

    if st.button("➕ Add Another Patient"):
        st.header(f"Enter Information for Patient {patient_counter + 1}:")
        clear_input_fields(patient_counter + 1)
        patient_counter += 1

# Open the Excel file with the default system application
open_file = st.sidebar.checkbox("📂 Open the saved patient data file")
if open_file:
    try:
        os.system(f'start excel.exe {file_path}')
    except Exception as e:
        st.error(f"❌ Error opening the file: {e}")
