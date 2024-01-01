import pandas as pd
import streamlit as st
import os
from datetime import datetime

# Function to calculate severity score
def calculate_severity(row):
    severity_score = 0
    if row['ChestPainType'] == 'Typical Angina':
        severity_score += 2
    if row['RestingBP'] > 130:
        severity_score += 1
    if row['Cholesterol'] > 220:
        severity_score += 1
    if row['ST_Slope'] == 0:
        severity_score += 1
    if row['ST_Slope'] == 2:
        severity_score += 2
    if row["HeartDisease"] == 1:
        severity_score += 5
    if row["Oldpeak"] == 1.5:
        severity_score += 2
    # Add more conditions here 
    return severity_score

# Function to display help message
def help_message():
    return "👨‍⚕️ Hello Doctor! I am here to assist you with managing heart patient data. You can ask me about the number of patients, arrange files, show reports, and more!"


# Function to read the Excel file and get the number of patients
def get_number_of_patients():
    try:
        df = pd.read_excel('heartpatients.xlsx')
        return len(df)
    except FileNotFoundError:
        return "❌ Error: Excel file not found."

# Function to arrange patients, add token numbers, and save the sorted file
def arrange_and_save_file():
    try:
        df = pd.read_excel('heartpatients.xlsx')
        df['SeverityScore'] = df.apply(calculate_severity, axis=1)
        df_sorted = df.sort_values(by='SeverityScore', ascending=False)

        # Add a new column 'TokenNumber' with token numbers from 1 to 100
        df_sorted['TokenNumber'] = range(1, min(101, len(df_sorted) + 1))

        df_sorted.to_excel('heart_conditions_sorted_with_tokens.xlsx', index=False)
        st.text("File arranged and saved successfully with token numbers.")

        # Ask if the user wants to see the arranged file
        user_input = st.selectbox("Do you want to see the arranged file?", ["Select", "Yes", "No"])
        if user_input == 'Yes':
            show_arranged_file_with_tokens()
        elif user_input == 'No':
            st.text("No problem.")
        else:
            st.text("Invalid input. No problem.")

    except FileNotFoundError:
        st.error("Error: Excel file not found.")

# Function to display patient report
def show_patient_report():
    try:
        os.startfile('heartpatients.xlsx', 'open')
        st.text("Patient report displayed.")
    except FileNotFoundError:
        st.error("Error: Excel file not found.")

# Function to display arranged file with token numbers
def show_arranged_file_with_tokens():
    try:
        file_path = 'heart_conditions_sorted_with_tokens.xlsx'
        os.startfile(file_path, 'open')
        st.text("Arranged file with token numbers displayed.")
    except FileNotFoundError:
        st.error("Error: Arranged file with token numbers not found.")

# Function to send token number
def send_token_number():
    try:
        df_sorted = pd.read_excel('heart_conditions_sorted_with_tokens.xlsx')
        # Fetch the ID and TokenNumber from the first row of the arranged file
        fetched_id = df_sorted.iloc[0]['Id']
        fetched_token_number = df_sorted.iloc[0]['TokenNumber']

        # Get the current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.text(f"Token number {fetched_token_number} sent to ID {fetched_id} for {current_datetime}")
    except FileNotFoundError:
        st.error("Error: Arranged file with token numbers not found.")

# Streamlit UI
def main():
    
    st.title("❤️ Heart Patient Chatbot")
    st.write("""
    👩‍⚕️ **Little About the Bot:**
    This chatbot is designed to assist healthcare professionals in managing heart patient data. 
    It can perform various tasks such as providing help messages, displaying the number of patients, 
    arranging files, showing patient reports, and sending token numbers for specific IDs.

    📂 **Usage:**
    - To get assistance, type 'help'.
    - To inquire about the number of patients, type 'how many patients'.
    - To arrange and save patient data, type 'arrange'.
    - To display patient reports, type 'show patients report'.
    - To view the arranged file with token numbers, type 'show arranged file'.
    - To send token numbers for specific IDs, type 'send the token number'.

    🗣️ **Conversation History:**
    The conversation history is displayed below, documenting interactions with the chatbot.
    """)
    conversation_history = []
    
    user_input = st.text_input("👨‍⚕️ Hello Doc! How can I help you today?").lower()
    conversation_history.append(("Bot", "👨‍⚕️ Hello Doc! How can I help you today?"))

    if 'help' in user_input:
        st.text(help_message())
        conversation_history.append(("Bot", help_message()))
    elif 'how many patients' in user_input:
        st.text(f"👩‍⚕️ You currently have {get_number_of_patients()} patients.")
        conversation_history.append(("Bot", f"👩‍⚕️ You currently have {get_number_of_patients()} patients."))
    elif 'arrange' in user_input:
        arrange_and_save_file()
        conversation_history.append(("Bot", "📂 File arranged and saved successfully with token numbers."))
    elif 'show patients report' in user_input:
        show_patient_report()
        conversation_history.append(("Bot", "📊 Patient report displayed."))
    elif 'show arranged file' in user_input:
        show_arranged_file_with_tokens()
        conversation_history.append(("Bot", "📂 Arranged file with token numbers displayed."))
    elif 'send the token number' in user_input:
        send_token_number()
        conversation_history.append(("Bot", "📬 Token number sent to a specific ID."))

    # Display conversation history
    st.text("🗣️ Conversation History:")
    for sender, message in conversation_history:
        st.text(f"{sender}: {message}")

if __name__ == "__main__":
    main()
