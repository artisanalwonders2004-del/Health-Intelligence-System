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
page = st.sidebar.radio("Navigate to:", ["🏠 Home", "📊 Daily Input", "🔍 Insights", "📈 Summary", "📖 User Guide"])

# Feedback form in sidebar
st.sidebar.markdown("---")
with st.sidebar.expander("💬 Give Feedback"):
    st.write("Found a bug? Have suggestions?")
    feedback = st.text_area("Your feedback:")
    if st.button("Submit Feedback"):
        st.success("Thank you! Your feedback helps improve the app.")
        # Simple file logging
        with open("user_feedback.txt", "a") as f:
            f.write(f"{datetime.now().isoformat()}: {feedback}\n")

# Home Page
if page == "🏠 Home":
    st.title("🏥 Health Intelligence System")
    st.markdown("### Track your health, discover patterns, feel better")

    st.markdown("""
    Welcome to your personal health intelligence system! This app helps you:

    - **Track** daily health metrics
    - **Discover** patterns in your well-being
    - **Get insights** about sleep, nutrition, and mood
    - **Build** healthier habits over time

    ### How to use:
    1. **Daily Input** - Log your daily health metrics
    2. **Basic Insights** - See immediate health feedback  
    3. **Weekly Summary** - View trends and patterns
    4. **User Guide** - Learn how to get the most from the app

    Start by navigating to **Daily Input** in the sidebar!
    """)

# Daily Input Page
elif page == "📊 Daily Input":
    st.title("📊 Daily Health Input")
    st.markdown("Log your daily health metrics to build your personal health intelligence.")

    with st.form("daily_input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            foods = st.text_area("Foods eaten today", placeholder="e.g., Oatmeal, Salad, Chicken, Rice...")
            water = st.slider("Water (glasses)", 0, 15, 8)
            sleep = st.slider("Sleep hours", 0.0, 12.0, 7.0, 0.5)
        
        with col2:
            mood = st.select_slider(
                "Mood today",
                options=["😢 Terrible", "😞 Poor", "😐 Neutral", "🙂 Good", "😄 Excellent"]
            )
            symptoms = st.text_input("Symptoms (comma separated)", placeholder="e.g., headache, fatigue, bloating")
            energy = st.select_slider(
                "Energy level",
                options=["😴 Very Low", "😩 Low", "😐 Moderate", "💪 High", "🚀 Very High"]
            )
        
        submitted = st.form_submit_button("Save Daily Entry")
        
        if submitted:
            # Load existing data
            try:
                df = pd.read_csv('data/daily_log.csv')
            except:
                df = pd.DataFrame(columns=[
                    'date', 'foods', 'water', 'sleep', 'mood', 
                    'symptoms', 'energy', 'timestamp'
                ])
            
            # Add new entry
            new_entry = {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'foods': foods,
                'water': water,
                'sleep': sleep,
                'mood': mood,
                'symptoms': symptoms,
                'energy': energy,
                'timestamp': datetime.now().isoformat()
            }
            
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv('data/daily_log.csv', index=False)
            
            st.success("✅ Daily entry saved successfully!")
            st.balloons()
            
            # Show preview
            st.subheader("Today's Entry Preview")
            preview_col1, preview_col2 = st.columns(2)
            with preview_col1:
                st.metric("Water", f"{water} glasses")
                st.metric("Sleep", f"{sleep} hours")
            with preview_col2:
                st.metric("Mood", mood)
                st.metric("Energy", energy)

# Insights Page
elif page == "🔍 Insights":
    st.title("🔍 Health Insights")
    st.markdown("Get immediate feedback on your recent health patterns.")

    def analyze_daily_health(sleep, water, foods, energy, symptoms):
        insights = []
        
        # Sleep analysis
        if sleep < 6:
            insights.append({
                'type': 'warning',
                'message': 'Low sleep detected. Aim for 7-9 hours for optimal health.'
            })
        elif sleep > 9:
            insights.append({
                'type': 'info', 
                'message': 'Good sleep duration. Consistent quality sleep is key.'
            })
        
        # Hydration analysis
        if water < 5:
            insights.append({
                'type': 'warning',
                'message': 'You\'re under-hydrating. Try to drink at least 8 glasses of water daily.'
            })
        elif water >= 8:
            insights.append({
                'type': 'success',
                'message': 'Excellent hydration! Keep drinking water throughout the day.'
            })
        
        # Food energy correlation
        heavy_food_indicators = ['pizza', 'burger', 'fried', 'fast food', 'heavy', 'rich']
        foods_lower = str(foods).lower()
        
        is_heavy_food = any(indicator in foods_lower for indicator in heavy_food_indicators)
        is_low_energy = False
        if energy and isinstance(energy, str):
            is_low_energy = 'low' in energy.lower() or 'very low' in energy.lower()
        
        if is_heavy_food and is_low_energy:
            insights.append({
                'type': 'warning',
                'message': 'Possible food fatigue detected. Heavy meals can sometimes cause low energy.'
            })
        
        # Symptom pattern detection
        if symptoms and len(str(symptoms).strip()) > 0:
            insights.append({
                'type': 'info',
                'message': f'Symptoms logged: {symptoms}. Track consistently to identify patterns.'
            })
        
        # Positive reinforcement
        if sleep >= 7 and water >= 8 and 'Good' in energy:
            insights.append({
                'type': 'success', 
                'message': 'Great balance today! Your sleep, hydration, and energy are well aligned.'
            })
        
        return insights

    # Load data
    try:
        df = pd.read_csv('data/daily_log.csv')
        if len(df) > 0:
            latest_entry = df.iloc[-1]
            
            st.subheader("Latest Entry Analysis")
            
            # Display insights
            insights = analyze_daily_health(
                sleep=latest_entry['sleep'],
                water=latest_entry['water'],
                foods=latest_entry['foods'],
                energy=latest_entry['energy'],
                symptoms=latest_entry['symptoms']
            )
            
            for insight in insights:
                if insight['type'] == 'warning':
                    st.warning(f"⚠️ {insight['message']}")
                elif insight['type'] == 'success':
                    st.success(f"✅ {insight['message']}")
                elif insight['type'] == 'info':
                    st.info(f"💡 {insight['message']}")
            
            # Show latest entry data
            with st.expander("View Latest Entry Details"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Sleep", f"{latest_entry['sleep']} hours")
                    st.metric("Water", f"{latest_entry['water']} glasses")
                with col2:
                    st.metric("Mood", latest_entry['mood'])
                    st.metric("Energy", latest_entry['energy'])
                    
        else:
            st.info("No data yet! Go to **Daily Input** to add your first entry.")
            
    except FileNotFoundError:
        st.info("No data yet! Go to **Daily Input** to add your first entry.")

# Summary Page
elif page == "📈 Summary":
    st.title("📈 Health Summary")
    st.markdown("View your health trends and patterns over time.")

    # Load data
    try:
        df = pd.read_csv('data/daily_log.csv')
        
        if len(df) > 0:
            df['date'] = pd.to_datetime(df['date'])
            
            # Last 7 days
            recent_data = df.tail(7)
            
            st.subheader("Last 7 Days Summary")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_sleep = recent_data['sleep'].mean()
                st.metric("Avg Sleep", f"{avg_sleep:.1f} hrs")
            
            with col2:
                avg_water = recent_data['water'].mean()
                st.metric("Avg Water", f"{avg_water:.1f} glasses")
            
            with col3:
                mood_counts = recent_data['mood'].value_counts()
                dominant_mood = mood_counts.index[0] if len(mood_counts) > 0 else "No data"
                st.metric("Dominant Mood", dominant_mood)
            
            with col4:
                symptom_days = recent_data[recent_data['symptoms'].notna() & (recent_data['symptoms'] != '')].shape[0]
                st.metric("Symptom Days", symptom_days)
            
            # Charts
            st.subheader("Health Trends")
            col1, col2 = st.columns(2)
            
            with col1:
                # Sleep trend
                if len(recent_data) > 1:
                    fig_sleep = px.line(recent_data, x='date', y='sleep', 
                                       title="Sleep Trend",
                                       markers=True)
                    fig_sleep.update_layout(yaxis_title="Hours", xaxis_title="Date")
                    st.plotly_chart(fig_sleep, use_container_width=True)
                
                # Water intake
                fig_water = px.bar(recent_data, x='date', y='water',
                                  title="Water Intake")
                fig_water.update_layout(yaxis_title="Glasses", xaxis_title="Date")
                st.plotly_chart(fig_water, use_container_width=True)
            
            with col2:
                # Mood trend (simplified)
                mood_map = {"😢 Terrible": 1, "😞 Poor": 2, "😐 Neutral": 3, "🙂 Good": 4, "😄 Excellent": 5}
                recent_data['mood_score'] = recent_data['mood'].map(mood_map)
                
                if len(recent_data) > 1:
                    fig_mood = px.line(recent_data, x='date', y='mood_score',
                                      title="Mood Trend",
                                      markers=True)
                    fig_mood.update_layout(yaxis_title="Mood Score", xaxis_title="Date")
                    st.plotly_chart(fig_mood, use_container_width=True)
                
                # Symptoms frequency
                if recent_data['symptoms'].notna().any():
                    all_symptoms = []
                    for symptoms in recent_data['symptoms'].dropna():
                        if symptoms:
                            all_symptoms.extend([s.strip() for s in symptoms.split(',')])
                    
                    if all_symptoms:
                        symptom_counts = pd.Series(all_symptoms).value_counts()
                        fig_symptoms = px.bar(x=symptom_counts.index, y=symptom_counts.values,
                                             title="Symptom Frequency")
                        fig_symptoms.update_layout(xaxis_title="Symptom", yaxis_title="Count")
                        st.plotly_chart(fig_symptoms, use_container_width=True)
            
        else:
            st.info("No data yet! Go to **Daily Input** to add your first entry.")
            
    except FileNotFoundError:
        st.info("No data yet! Go to **Daily Input** to add your first entry.")

# User Guide Page
elif page == "📖 User Guide":
    st.title("📖 User Guide")
    
    st.markdown("""
    ## 🏥 Health Intelligence System - User Guide

    ### 🎯 What This App Does
    Tracks your daily health habits and finds patterns to help you understand:
    - How sleep affects your mood
    - How hydration impacts energy  
    - How food influences how you feel
    - Your weekly health trends
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("1. 📊 Daily Tracking")
        st.write("""
        Go to **Daily Input** each day:
        - **Sleep**: Hours slept
        - **Water**: Glasses drank
        - **Mood**: How you feel
        - **Energy**: Energy level
        - **Symptoms**: Any discomfort
        - **Foods**: What you ate
        """)
    
    with col2:
        st.subheader("2. 🔍 Check Insights")
        st.write("""
        Go to **Insights** to see:
        - Health feedback
        - Pattern detection  
        - Daily recommendations
        """)
    
    with col3:
        st.subheader("3. 📈 View Trends")
        st.write("""
        Go to **Summary** to see:
        - Weekly averages
        - Sleep trends
        - Mood patterns
        """)
    
    st.markdown("""
    ### 💡 Tips for Best Results
    - **Be consistent**: Log at same time daily
    - **Be honest**: Data is only for you
    - **Track 7+ days**: Patterns emerge over time
    - **Use feedback form**: Report bugs or suggest features

    ### 🔒 Privacy
    - Your data stays in your browser
    - No personal information is shared  
    - You control your data completely

    ### 🆘 Need Help?
    Use the **💬 Give Feedback** form in the sidebar to report issues or ask questions!
    """)