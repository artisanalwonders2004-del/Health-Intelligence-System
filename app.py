import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(page_title="Health Intelligence", layout="wide")

# Initialize data
if not os.path.exists('data/daily_log.csv'):
    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(columns=['date', 'foods', 'water', 'sleep', 'mood', 'symptoms', 'energy', 'timestamp'])
    df.to_csv('data/daily_log.csv', index=False)

# Navigation
page = st.sidebar.radio("Navigate to:", ["🏠 Home", "📊 Daily Input", "🔍 Insights", "📈 Summary"])

# 👇 ADD THIS NEW FEEDBACK SECTION 👇
st.sidebar.markdown("---")
with st.sidebar.expander("💬 Give Feedback"):
    st.write("Found a bug? Have suggestions?")
    feedback = st.text_area("Your feedback:")
    if st.button("Submit Feedback"):
        st.success("Thank you! Your feedback helps improve the app.")
        # Simple file logging
        with open("user_feedback.txt", "a") as f:
            f.write(f"{datetime.now().isoformat()}: {feedback}\n")

# 👇 MAKE SURE this line is properly aligned with the navigation code
if page == "🏠 Home":
    st.title("🏥 Health Intelligence System")
    st.write("Track your health patterns and discover insights.")
    
elif page == "📊 Daily Input":
    st.title("📊 Daily Health Input")
    
    with st.form("daily_form"):
        col1, col2 = st.columns(2)
        with col1:
            foods = st.text_area("Foods eaten")
            water = st.slider("Water glasses", 0, 15, 8)
            sleep = st.slider("Sleep hours", 0.0, 12.0, 7.0)
        with col2:
            mood = st.select_slider("Mood", options=["😢 Terrible", "😞 Poor", "😐 Neutral", "🙂 Good", "😄 Excellent"])
            symptoms = st.text_input("Symptoms")
            energy = st.select_slider("Energy", options=["😴 Very Low", "😩 Low", "😐 Moderate", "💪 High", "🚀 Very High"])
        
        if st.form_submit_button("Save Entry"):
            df = pd.read_csv('data/daily_log.csv')
            new_entry = {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'foods': foods, 'water': water, 'sleep': sleep,
                'mood': mood, 'symptoms': symptoms, 'energy': energy,
                'timestamp': datetime.now().isoformat()
            }
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv('data/daily_log.csv', index=False)
            st.success("✅ Entry saved!")
            st.balloons()

elif page == "🔍 Insights":
    st.title("🔍 Health Insights")
    
    try:
        df = pd.read_csv('data/daily_log.csv')
        if len(df) > 0:
            latest = df.iloc[-1]
            st.subheader("Latest Entry Analysis")
            
            # Simple insights
            if latest['sleep'] < 6:
                st.warning("⚠️ Low sleep detected")
            if latest['water'] < 5:
                st.warning("⚠️ Drink more water")
            if latest['sleep'] >= 7 and latest['water'] >= 8:
                st.success("✅ Great balance today!")
                
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Sleep", f"{latest['sleep']} hrs")
                st.metric("Water", f"{latest['water']} glasses")
            with col2:
                st.metric("Mood", latest['mood'])
                st.metric("Energy", latest['energy'])
        else:
            st.info("No data yet! Add entries in Daily Input.")
    except:
        st.info("No data yet! Add entries in Daily Input.")

elif page == "📈 Summary":
    st.title("📈 Health Summary")
    
    try:
        df = pd.read_csv('data/daily_log.csv')
        if len(df) > 0:
            st.subheader("Your Data")
            st.dataframe(df)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avg Sleep", f"{df['sleep'].mean():.1f} hrs")
            with col2:
                st.metric("Avg Water", f"{df['water'].mean():.1f} glasses")
            with col3:
                st.metric("Total Entries", len(df))
            
            if len(df) > 1:
                st.subheader("Sleep Trend")
                st.line_chart(df.set_index('date')['sleep'])
        else:
            st.info("No data yet! Add entries in Daily Input.")
    except:
        st.info("No data yet! Add entries in Daily Input.")