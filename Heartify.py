import streamlit as st
import pandas as pd
from PIL import Image

# Load a smaller image
image = Image.open("logo.png")  # Replace with the path to your smaller logo

# Title and description
st.title("💓 Heart Disease AI Project")
st.image(image, use_column_width=True)
st.write(
    "Welcome to our project blog! We've developed an AI solution to address heart disease and improve healthcare. 🌐🚀"
)

# Introduction
st.header("Introduction")
st.write(
    "Heart disease is a leading cause of mortality globally. Our project leverages generative AI models to predict the severity of heart disease, "
    "provide personalized treatment plans, and enhance the telemedicine experience. 🤖💉"
)

# Key Features
st.header("Key Features")
st.write(
    "1. **Severity Prediction**: Our model uses past and current patient data, comparing it with a healthy dataset, to predict disease severity. 📉💊"
)
st.write(
    "2. **Personalized Treatment Plans**: Based on predictive modeling results, we offer personalized treatment plans to patients. 🏥💡"
)
st.write(
    "3. **Telemedicine Enhancement**: Chatbots assist in summarizing patient reports, predicting diseases based on symptoms, and providing medical information. 💬📄🤒"
)

# About the Team
st.header("About the Team")
st.write("Our team consists of dedicated professionals passionate about leveraging AI for healthcare improvements.   🤝👩‍⚕️👨‍💻"
)
st.write("~ made by Aayush, Nimish , Pranjal and Sylan")

# Conclusion
st.header("Conclusion")
st.write(
    "We believe our project will contribute to a healthier future by providing accurate predictions and personalized healthcare solutions. 🌍💪"
)

if st.button("Login"):
    # You can add any action you want when the button is clicked
    st.write("loading...")