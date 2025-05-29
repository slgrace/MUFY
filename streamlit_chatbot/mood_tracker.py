import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json

# Configure page
st.set_page_config(
    page_title="Mood & Wellness Tracker",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS for Times New Roman font
st.markdown("""
<style>
    /* Apply Times New Roman to all text elements */
    .stApp, .stApp * {
        font-family: 'Times New Roman', Times, serif !important;
    }
    
    /* Specific styling for different elements */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Times New Roman', Times, serif !important;
    }
    
    .stSelectbox label, .stTextInput label, .stTextArea label, 
    .stSlider label, .stNumberInput label, .stMultiSelect label,
    .stRadio label, .stCheckbox label {
        font-family: 'Times New Roman', Times, serif !important;
    }
    
    .stButton button {
        font-family: 'Times New Roman', Times, serif !important;
    }
    
    .stMarkdown, .stText {
        font-family: 'Times New Roman', Times, serif !important;
    }
    
    .stSidebar * {
        font-family: 'Times New Roman', Times, serif !important;
    }
    
    /* Form elements */
    input, textarea, select {
        font-family: 'Times New Roman', Times, serif !important;
    }
    
    /* Metrics and other components */
    .metric-container, .stMetric {
        font-family: 'Times New Roman', Times, serif !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data storage
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = []
if 'wellness_data' not in st.session_state:
    st.session_state.wellness_data = []
if 'selected_mood' not in st.session_state:
    st.session_state.selected_mood = None
if 'show_form' not in st.session_state:
    st.session_state.show_form = False
if 'diary_entries' not in st.session_state:
    st.session_state.diary_entries = []

# Mood and wellness dictionaries
MOODS = {
    "😊": {"name": "Happy", "value": 5, "color": "#4CAF50"},
    "😄": {"name": "Excited", "value": 4, "color": "#FF9800"},
    "😐": {"name": "Neutral", "value": 3, "color": "#9E9E9E"},
    "😔": {"name": "Sad", "value": 2, "color": "#2196F3"},
    "😡": {"name": "Angry", "value": 1, "color": "#F44336"},
    "😰": {"name": "Anxious", "value": 1, "color": "#9C27B0"},
    "😴": {"name": "Tired", "value": 2, "color": "#607D8B"}
}

ACTIVITIES = [
    "Exercise", "Meditation", "Reading", "Social Time", "Work", 
    "Hobbies", "Nature Walk", "Music", "Cooking", "Gaming",
    "Sleep", "Studying", "Family Time", "Shopping", "Travel"
]

WELLNESS_TIPS = {
    1: [
        "Try deep breathing exercises for 5 minutes",
        "Take a short walk outside",
        "Listen to calming music",
        "Call a friend or family member",
        "Practice gratitude by writing 3 things you're thankful for"
    ],
    2: [
        "Engage in light physical activity",
        "Try a new hobby or creative activity",
        "Watch something funny or uplifting",
        "Take a warm bath or shower",
        "Practice mindfulness meditation"
    ],
    3: [
        "Set small, achievable goals for the day",
        "Try a new recipe or meal",
        "Organize your living space",
        "Connect with nature",
        "Practice a skill you want to improve"
    ],
    4: [
        "Channel your energy into a workout",
        "Share your enthusiasm with others",
        "Start a new project or challenge",
        "Celebrate your achievements",
        "Help someone else with their goals"
    ],
    5: [
        "Spread positivity to others",
        "Reflect on what's going well",
        "Plan something to look forward to",
        "Take photos of beautiful moments",
        "Practice acts of kindness"
    ]
}

SONG_RECOMMENDATIONS = {
    "😊": {  # Happy
        "genre": "Uplifting Pop",
        "songs": [
            "Happy - Pharrell Williams",
            "Good 4 U - Olivia Rodrigo",
            "Sunflower - Post Malone",
            "Can't Stop the Feeling - Justin Timberlake",
            "Walking on Sunshine - Katrina & The Waves",
            "Feel Good Inc. - Gorillaz",
            "Uptown Funk - Bruno Mars"
        ]
    },
    "😄": {  # Excited
        "genre": "High Energy",
        "songs": [
            "Thunder - Imagine Dragons",
            "Stronger - Kelly Clarkson",
            "Roar - Katy Perry",
            "Pump It - Black Eyed Peas",
            "Eye of the Tiger - Survivor",
            "Don't Stop Me Now - Queen",
            "High Hopes - Panic! At The Disco"
        ]
    },
    "😐": {  # Neutral
        "genre": "Chill Vibes",
        "songs": [
            "Blinding Lights - The Weeknd",
            "Watermelon Sugar - Harry Styles",
            "Levitating - Dua Lipa",
            "Heat Waves - Glass Animals",
            "Stay - The Kid LAROI & Justin Bieber",
            "Peaches - Justin Bieber",
            "Good Days - SZA"
        ]
    },
    "😔": {  # Sad
        "genre": "Comforting & Healing",
        "songs": [
            "Someone Like You - Adele",
            "Fix You - Coldplay",
            "The Sound of Silence - Simon & Garfunkel",
            "Mad World - Gary Jules",
            "Hurt - Johnny Cash",
            "Breathe Me - Sia",
            "Skinny Love - Bon Iver"
        ]
    },
    "😡": {  # Angry
        "genre": "Release & Rock",
        "songs": [
            "Stressed Out - Twenty One Pilots",
            "In the End - Linkin Park",
            "Somebody That I Used to Know - Gotye",
            "Counting Stars - OneRepublic",
            "Radioactive - Imagine Dragons",
            "Numb - Linkin Park",
            "Breaking the Habit - Linkin Park"
        ]
    },
    "😰": {  # Anxious
        "genre": "Calming & Peaceful",
        "songs": [
            "Weightless - Marconi Union",
            "Clair de Lune - Claude Debussy",
            "Aqueous Transmission - Incubus",
            "Spiegel im Spiegel - Arvo Pärt",
            "River - Joni Mitchell",
            "The Night We Met - Lord Huron",
            "Holocene - Bon Iver"
        ]
    },
    "😴": {  # Tired
        "genre": "Gentle & Soothing",
        "songs": [
            "Sleep Baby Sleep - Broods",
            "Dream a Little Dream - Ella Fitzgerald",  
            "La Vie En Rose - Édith Piaf",
            "Moonlight Sonata - Beethoven",
            "Sleepyhead - Passion Pit",
            "Lullaby - Brahms",
            "Weightless - Marconi Union"
        ]
    }
}

def add_diary_entry(title, content, mood=None):
    """Add a new diary entry to session state"""
    entry = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M'),
        'title': title,
        'content': content,
        'mood': mood,
        'word_count': len(content.split()) if content else 0
    }
    st.session_state.diary_entries.append(entry)

def add_mood_entry(mood, activities, notes, energy_level, sleep_hours):
    """Add a new mood entry to session state"""
    entry = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M'),
        'mood': mood,
        'mood_value': MOODS[mood]['value'],
        'activities': activities,
        'notes': notes,
        'energy_level': energy_level,
        'sleep_hours': sleep_hours
    }
    st.session_state.mood_data.append(entry)

def get_mood_insights():
    """Generate insights from mood data"""
    if not st.session_state.mood_data:
        return "No data available yet. Start tracking your mood!"
    
    df = pd.DataFrame(st.session_state.mood_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Recent mood trend
    recent_moods = df.tail(7)['mood_value'].tolist()
    if len(recent_moods) >= 2:
        if recent_moods[-1] > recent_moods[-2]:
            trend = "📈 Your mood is trending upward!"
        elif recent_moods[-1] < recent_moods[-2]:
            trend = "📉 Your mood has dipped recently. Consider some self-care."
        else:
            trend = "➡️ Your mood has been stable lately."
    else:
        trend = "Need more data to identify trends."
    
    # Most frequent mood
    most_common_mood = df['mood'].mode().iloc[0] if not df.empty else "😊"
    
    # Average mood
    avg_mood = df['mood_value'].mean() if not df.empty else 3
    
    insights = f"""
    **Recent Trend**: {trend}
    
    **Most Common Mood**: {most_common_mood} {MOODS[most_common_mood]['name']}
    
    **Average Mood Score**: {avg_mood:.1f}/5
    
    **Total Entries**: {len(df)}
    """
    
    return insights

def create_mood_chart():
    """Create mood trend chart"""
    if not st.session_state.mood_data:
        return None
    
    df = pd.DataFrame(st.session_state.mood_data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    fig = px.line(df, x='date', y='mood_value', 
                  title='Mood Trend Over Time',
                  labels={'mood_value': 'Mood Score', 'date': 'Date'},
                  line_shape='spline')
    
    fig.update_layout(
        yaxis=dict(range=[0, 6], tickmode='linear', tick0=1, dtick=1),
        showlegend=False,
        height=400
    )
    
    return fig

def create_activity_chart():
    """Create activity frequency chart"""
    if not st.session_state.mood_data:
        return None
    
    all_activities = []
    for entry in st.session_state.mood_data:
        all_activities.extend(entry['activities'])
    
    if not all_activities:
        return None
    
    activity_counts = pd.Series(all_activities).value_counts()
    
    fig = px.bar(x=activity_counts.values, y=activity_counts.index, 
                 orientation='h',
                 title='Most Frequent Activities',
                 labels={'x': 'Frequency', 'y': 'Activities'})
    
    fig.update_layout(height=400)
    return fig

def main():
    # Title and header
    st.title("🌈 Mood & Wellness Tracker")
    st.markdown("*Track your daily mood, activities, and wellness journey*")
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Choose a section:", 
                       ["📝 Daily Check-in", "📊 Analytics", "💡 Wellness Tips", "📔 Personal Diary", "🎵 Music Therapy", "📋 History"])
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        if st.session_state.mood_data:
            df = pd.DataFrame(st.session_state.mood_data)
            st.metric("Total Entries", len(df))
            st.metric("Average Mood", f"{df['mood_value'].mean():.1f}/5")
            st.metric("Days Tracked", df['date'].nunique())
        
        if st.session_state.diary_entries:
            st.metric("Diary Entries", len(st.session_state.diary_entries))
    
    # Main content based on selected page
    if page == "📝 Daily Check-in":
        st.header("How are you feeling today?")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Mood selection
            st.subheader("Select your mood:")
            mood_cols = st.columns(len(MOODS))
            
            for i, (emoji, mood_info) in enumerate(MOODS.items()):
                with mood_cols[i]:
                    if st.button(f"{emoji}\n{mood_info['name']}", key=f"mood_{i}"):
                        st.session_state.selected_mood = emoji
                        st.session_state.show_form = True
            
            # Show selected mood
            if st.session_state.selected_mood:
                st.success(f"You selected: {st.session_state.selected_mood} {MOODS[st.session_state.selected_mood]['name']}")
                
                # Reset button
                if st.button("Choose Different Mood", type="secondary"):
                    st.session_state.selected_mood = None
                    st.session_state.show_form = False
                    st.rerun()
            
            # Show form only if mood is selected
            if st.session_state.selected_mood and st.session_state.show_form:
                st.markdown("---")
                
                # Activity selection
                st.subheader("What activities did you do today?")
                selected_activities = st.multiselect("Choose activities:", ACTIVITIES, key="activities_select")
                
                # Additional inputs
                col1a, col1b = st.columns(2)
                with col1a:
                    energy_level = st.slider("Energy Level (1-10)", 1, 10, 5, key="energy_slider")
                with col1b:
                    sleep_hours = st.number_input("Hours of Sleep Last Night", 0.0, 24.0, 8.0, 0.5, key="sleep_input")
                
                # Notes
                notes = st.text_area("Additional notes (optional):", 
                                   placeholder="How was your day? Any thoughts or reflections?", 
                                   key="notes_input")
                
                # Submit button
                col_submit, col_cancel = st.columns([1, 1])
                with col_submit:
                    if st.button("Save Entry", type="primary", key="save_button"):
                        add_mood_entry(st.session_state.selected_mood, selected_activities, notes, energy_level, sleep_hours)
                        st.success("✅ Entry saved successfully!")
                        st.balloons()
                        # Reset form after saving
                        st.session_state.selected_mood = None
                        st.session_state.show_form = False
                        st.rerun()
                
                with col_cancel:
                    if st.button("Cancel", key="cancel_button"):
                        st.session_state.selected_mood = None
                        st.session_state.show_form = False
                        st.rerun()
        
        with col2:
            st.subheader("🎵 Song Recommendations")
            if st.session_state.selected_mood:
                mood_songs = SONG_RECOMMENDATIONS.get(st.session_state.selected_mood, SONG_RECOMMENDATIONS["😐"])
                st.info(f"**{mood_songs['genre']} for your mood:**")
                
                # Display 3 random songs
                displayed_songs = random.sample(mood_songs['songs'], min(3, len(mood_songs['songs'])))
                for song in displayed_songs:
                    st.write(f"🎶 {song}")
                
                if st.button("🔄 More Songs", key="more_songs"):
                    st.rerun()
            else:
                st.info("💡 Select your mood to get personalized music recommendations!")
            
            st.markdown("---")
            st.subheader("Today's Wellness Tip")
            if st.session_state.selected_mood:
                tips = WELLNESS_TIPS.get(MOODS[st.session_state.selected_mood]['value'], WELLNESS_TIPS[3])
                tip = random.choice(tips)
                st.info(f"💡 {tip}")
            else:
                st.info("💡 Select your mood to get a personalized wellness tip!")
    
    elif page == "📔 Personal Diary":
        st.header("📔 Personal Diary")
        st.markdown("Write down your thoughts and reflections")
        
        # Diary entry form
        with st.form("diary_form"):
            st.subheader("New Diary Entry")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                entry_title = st.text_input("Entry Title:", placeholder="Give your entry a title...")
            with col2:
                entry_mood = st.selectbox("Current Mood (optional):", 
                                        [""] + [f"{emoji} {info['name']}" for emoji, info in MOODS.items()])
            
            entry_content = st.text_area("Your thoughts:", 
                                       placeholder="What's on your mind today? How are you feeling? What happened?",
                                       height=200)
            
            submitted = st.form_submit_button("Save Diary Entry", type="primary")
            
            if submitted:
                if entry_title.strip() or entry_content.strip():
                    # Extract mood emoji if selected
                    mood_emoji = entry_mood.split()[0] if entry_mood else None
                    add_diary_entry(entry_title or "Untitled Entry", entry_content, mood_emoji)
                    st.success("✅ Diary entry saved!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Please write at least a title or some content for your diary entry.")
        
        st.markdown("---")
        
        # Display existing diary entries
        if st.session_state.diary_entries:
            st.subheader(f"Your Diary Entries ({len(st.session_state.diary_entries)})")
            
            # Sort entries by date (newest first)
            sorted_entries = sorted(st.session_state.diary_entries, 
                                  key=lambda x: f"{x['date']} {x['time']}", reverse=True)
            
            for i, entry in enumerate(sorted_entries):
                with st.expander(f"📝 {entry['title']} - {entry['date']}"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**Date:** {entry['date']}")
                        st.write(f"**Time:** {entry['time']}")
                    
                    with col2:   
                        if entry['mood']:
                            st.write(f"**Mood:** {entry['mood']} {MOODS[entry['mood']]['name']}")
                    
                    with col3:
                        st.write(f"**Words:** {entry['word_count']}")
                    
                    st.markdown("**Content:**")
                    st.write(entry['content'])
                    
                    # Delete button
                    if st.button(f"🗑️ Delete Entry", key=f"delete_diary_{i}"):
                        st.session_state.diary_entries.remove(entry)
                        st.success("Entry deleted!")
                        st.rerun()
        else:
            st.info("No diary entries yet. Start writing your first entry above!")
    
    elif page == "🎵 Music Therapy":
        st.header("🎵 Music Therapy")
        st.markdown("Discover music that matches and helps improve your mood")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Select Your Current Mood")
            current_mood = st.selectbox("How are you feeling right now?", 
                                      [f"{emoji} {info['name']}" for emoji, info in MOODS.items()],
                                      key="music_mood_select")
            
            if current_mood:
                mood_emoji = current_mood.split()[0]
                mood_songs = SONG_RECOMMENDATIONS[mood_emoji]
                
                st.info(f"**Genre: {mood_songs['genre']}**")
                st.markdown("### Recommended Songs:")
                
                # Display all songs for this mood
                for song in mood_songs['songs']:
                    st.write(f"🎶 {song}")
        
        with col2:
            st.subheader("Mood-Based Playlists")
            
            playlist_mood = st.radio("Browse playlists by mood:", 
                                    [f"{emoji} {info['name']}" for emoji, info in MOODS.items()],
                                    key="playlist_select")
            
            if playlist_mood:
                playlist_emoji = playlist_mood.split()[0]
                playlist_songs = SONG_RECOMMENDATIONS[playlist_emoji]
                
                st.markdown(f"### {playlist_songs['genre']} Playlist")
                
                # Create a playlist view
                for i, song in enumerate(playlist_songs['songs'], 1):
                    st.write(f"{i}. {song}")
        
        st.markdown("---")
        st.subheader("Music Mood Benefits")
        
        tab1, tab2, tab3 = st.tabs(["Mood Enhancement", "Stress Relief", "Energy Boost"])
        
        with tab1:
            st.markdown("""
            #### How Music Enhances Your Mood
            - **Happy/Upbeat Music**: Releases dopamine and serotonin
            - **Calming Music**: Reduces cortisol levels and anxiety
            - **Familiar Songs**: Trigger positive memories and emotions
            - **Rhythmic Music**: Synchronizes with brain waves for focus
            """)
        
        with tab2:
            st.markdown("""
            #### Music for Stress Relief
            - **Slow Tempo**: 60-80 BPM matches resting heart rate
            - **Classical Music**: Proven to lower blood pressure
            - **Nature Sounds**: Activate parasympathetic nervous system
            - **Instrumental**: No lyrics to process, pure emotional response
            """)
        
        with tab3:
            st.markdown("""
            #### Music for Energy & Motivation
            - **High BPM**: 120-140 BPM boosts physical performance
            - **Major Keys**: Create feelings of happiness and energy
            - **Strong Beat**: Encourages movement and activity
            - **Familiar Favorites**: Increase motivation through positive association
            """)
    
    elif page == "📊 Analytics":
        st.header("Your Mood Analytics")
        
        if not st.session_state.mood_data:
            st.warning("No data available yet. Start by logging your daily mood!")
            return
        
        # Insights
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Insights")
            st.markdown(get_mood_insights())
        
        with col2:
            st.subheader("Mood Distribution")
            df = pd.DataFrame(st.session_state.mood_data)
            mood_counts = df['mood'].value_counts()
            
            fig_pie = px.pie(values=mood_counts.values, names=[MOODS[m]['name'] for m in mood_counts.index],
                            title="Mood Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Charts
        st.subheader("Mood Trend")
        mood_chart = create_mood_chart()
        if mood_chart:
            st.plotly_chart(mood_chart, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            activity_chart = create_activity_chart()
            if activity_chart:
                st.plotly_chart(activity_chart, use_container_width=True)
        
        with col4:
            st.subheader("Energy vs Sleep Analysis")
            df = pd.DataFrame(st.session_state.mood_data)
            if len(df) > 0:
                fig_scatter = px.scatter(df, x='sleep_hours', y='energy_level', 
                                       color='mood_value', 
                                       title='Sleep vs Energy Levels',
                                       labels={'sleep_hours': 'Hours of Sleep', 'energy_level': 'Energy Level'})
                st.plotly_chart(fig_scatter, use_container_width=True)
    
    elif page == "💡 Wellness Tips":
        st.header("Wellness Tips & Resources")
        
        tab1, tab2, tab3 = st.tabs(["Daily Tips", "Mood Boosters", "Exercises"])
        
        with tab1:
            st.subheader("Daily Wellness Tips")
            st.markdown("""
            #### 🌅 Morning Routine
            - Start with 5 minutes of deep breathing
            - Set 3 intentions for the day
            - Drink a glass of water
            
            #### 🌞 Throughout the Day
            - Take breaks every hour
            - Practice gratitude
            - Stay hydrated
            
            #### 🌙 Evening Routine
            - Reflect on the day's positives
            - Limit screen time before bed
            - Practice relaxation techniques
            """)
        
        with tab2:
            st.subheader("Mood Boosting Activities")
            mood_booster = st.selectbox("Choose your current mood for personalized suggestions:",
                                      [f"{emoji} {info['name']}" for emoji, info in MOODS.items()])
            
            if mood_booster:
                emoji = mood_booster.split()[0]
                mood_value = MOODS[emoji]['value']
                tips = WELLNESS_TIPS[mood_value]
                
                st.markdown("### Suggested Activities:")
                for tip in tips:
                    st.markdown(f"• {tip}")
        
        with tab3:
            st.subheader("Quick Wellness Exercises")
            
            exercise_type = st.radio("Choose exercise type:", 
                                   ["Breathing", "Mindfulness", "Physical", "Mental"])
            
            if exercise_type == "Breathing":
                st.markdown("""
                #### 4-7-8 Breathing Technique
                1. Exhale completely
                2. Inhale through nose for 4 counts
                3. Hold breath for 7 counts
                4. Exhale through mouth for 8 counts
                5. Repeat 3-4 times
                """)
            elif exercise_type == "Mindfulness":
                st.markdown("""
                #### 5-4-3-2-1 Grounding Technique
                - **5** things you can see
                - **4** things you can touch
                - **3** things you can hear
                - **2** things you can smell
                - **1** thing you can taste
                """)
            elif exercise_type == "Physical":
                st.markdown("""
                #### Quick Desk Stretches
                1. Neck rolls (5 each direction)
                2. Shoulder shrugs (10 times)
                3. Wrist circles (10 each direction)
                4. Deep breathing with arm raises
                """)
            else:  # Mental
                st.markdown("""
                #### Mental Clarity Exercise
                1. Write down 3 things you're grateful for
                2. Set 1 small goal for today
                3. Identify 1 challenge and 1 solution
                4. Take 2 minutes to visualize success
                """)
    
    else:  # History
        st.header("Your Mood History")
        
        if not st.session_state.mood_data:
            st.warning("No mood entries yet. Start tracking to see your history!")
            return
        
        df = pd.DataFrame(st.session_state.mood_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            date_filter = st.date_input("Filter by date (optional):")
        with col2:
            mood_filter = st.multiselect("Filter by mood:", 
                                       [f"{emoji} {info['name']}" for emoji, info in MOODS.items()])
        
        # Apply filters
        filtered_df = df.copy()
        if date_filter:
            filtered_df = filtered_df[filtered_df['date'].dt.date == date_filter]
        
        if mood_filter:
            mood_emojis = [mood.split()[0] for mood in mood_filter]
            filtered_df = filtered_df[filtered_df['mood'].isin(mood_emojis)]
        
        # Display entries
        st.subheader(f"Showing {len(filtered_df)} entries")
        
        for idx, row in filtered_df.iterrows():
            with st.expander(f"{row['date'].strftime('%B %d, %Y')} - {row['mood']} {MOODS[row['mood']]['name']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Time:** {row['time']}")
                    st.write(f"**Mood:** {row['mood']} {MOODS[row['mood']]['name']}")
                
                with col2:
                    st.write(f"**Energy Level:** {row['energy_level']}/10")
                    st.write(f"**Sleep Hours:** {row['sleep_hours']}")
                
                with col3:
                    if row['activities']:
                        st.write("**Activities:**")
                        for activity in row['activities']:
                            st.write(f"• {activity}")
                
                if row['notes']:
                    st.write(f"**Notes:** {row['notes']}")
        
        # Export data
        if st.button("Export Data as CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"mood_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()