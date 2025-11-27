import streamlit as st
import pandas as pd

st.title("📈 Health Summary")
st.write("View your health trends over time.")

try:
    df = pd.read_csv('data/daily_log.csv')
    
    if len(df) > 0:
        st.subheader("Your Health Data")
        st.dataframe(df)
        
        # Simple stats
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_sleep = df['sleep'].mean()
            st.metric("Average Sleep", f"{avg_sleep:.1f} hrs")
        with col2:
            avg_water = df['water'].mean()
            st.metric("Average Water", f"{avg_water:.1f} glasses")
        with col3:
            total_entries = len(df)
            st.metric("Total Entries", total_entries)
        
        # Simple chart
        if len(df) > 1:
            st.subheader("Sleep Trend")
            st.line_chart(df.set_index('date')['sleep'])
        
    else:
        st.info("No data yet! Add some entries in Daily Input.")
        
except FileNotFoundError:
    st.info("No data yet! Add some entries in Daily Input.")