import streamlit as st
import pandas as pd

st.title("🔍 Health Insights")
st.write("See your health patterns and get feedback.")

try:
    df = pd.read_csv('data/daily_log.csv')
    
    if len(df) > 0:
        st.success(f"📈 You have {len(df)} health entries!")
        
        # Show latest entry
        latest = df.iloc[-1]
        st.subheader("Latest Entry")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sleep", f"{latest['sleep']} hrs")
            st.metric("Water", f"{latest['water']} glasses")
        with col2:
            st.metric("Mood", latest['mood'])
            if 'name' in latest:
                st.metric("Name", latest['name'])
        
        # Simple insights
        st.subheader("Health Tips")
        if latest['sleep'] < 6:
            st.warning("⚠️ Get more sleep! Aim for 7-9 hours.")
        else:
            st.success("✅ Good sleep duration!")
            
        if latest['water'] < 5:
            st.warning("⚠️ Drink more water! Aim for 8+ glasses.")
        else:
            st.success("✅ Good hydration!")
            
    else:
        st.info("No data yet! Go to Daily Input to add your first entry.")
        
except FileNotFoundError:
    st.info("No data yet! Go to Daily Input to add your first entry.")