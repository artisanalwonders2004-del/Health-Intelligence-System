import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.title("📊 Daily Health Input")
st.write("Log your daily health metrics here.")

# Simple form
with st.form("my_health_form"):
    name = st.text_input("Your Name")
    sleep = st.slider("Sleep hours", 0.0, 12.0, 7.0)
    water = st.slider("Water glasses", 0, 15, 8)
    mood = st.selectbox("Today's mood", ["😢 Terrible", "😞 Poor", "😐 Neutral", "🙂 Good", "😄 Excellent"])
    
    submitted = st.form_submit_button("Save Entry")
    
    if submitted:
        # Save to CSV
        try:
            df = pd.read_csv('data/daily_log.csv')
        except:
            df = pd.DataFrame(columns=['date', 'name', 'sleep', 'water', 'mood', 'timestamp'])
        
        new_entry = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'name': name,
            'sleep': sleep,
            'water': water,
            'mood': mood,
            'timestamp': datetime.now().isoformat()
        }
        
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv('data/daily_log.csv', index=False)
        
        st.success("✅ Entry saved!")
        st.balloons()
        
        # Show what was saved
        st.write("**Saved Data:**")
        st.write(f"Name: {name}")
        st.write(f"Sleep: {sleep} hours")
        st.write(f"Water: {water} glasses")
        st.write(f"Mood: {mood}")