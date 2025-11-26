import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Health Intelligence System",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Health Intelligence System")
st.markdown("### Your personal health tracking assistant")

st.success("🎉 **App loaded successfully!** Use the sidebar to navigate.")

# Initialize data file
if not os.path.exists('data/daily_log.csv'):
    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(columns=[
        'date', 'foods', 'water', 'sleep', 'mood', 
        'symptoms', 'energy', 'timestamp'
    ])
    df.to_csv('data/daily_log.csv', index=False)
    st.info("📁 Data file created successfully!")