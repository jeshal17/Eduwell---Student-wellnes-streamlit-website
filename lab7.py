import streamlit as st
import matplotlib.pyplot as plt
from custom_recursive import recursive_avg, wellness_streak  

st.set_page_config(page_title="EduWell Wellness Tracker", layout="centered")

st.markdown("""
    <style>
    body {
        background-color: #fff0f5;
        color: #660033;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #cc0066;
    }
    .stButton > button {
        background-color: #ff99cc;
        color: white;
        border-radius: 10px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    .stSlider > div {
        color: #cc0066;
    }
    .stMarkdown {
        color: #660033;
    }
    .stTextInput > div > input {
        background-color: #ffe6f0;
        color: #660033;
        border-radius: 5px;
    }
    .stCheckbox > div {
        color: #cc0066;
    }
    </style>
""", unsafe_allow_html=True)

def wellness_return(prev, curr):
    if prev == 0:
        return 0
    return round(((curr - prev) / prev) * 100, 2)

def habit_score(habits):
    return sum(habits.values()) / len(habits) if habits else 0

st.title("EduWell: Student Wellness & Habit Tracker")
st.markdown("Track your wellness and build habits consistently.")

if 'mood' not in st.session_state or 'energy' not in st.session_state or 'productivity' not in st.session_state:
    st.session_state.mood = []
    st.session_state.energy = []
    st.session_state.productivity = []

st.header(" Daily Wellness Check-In")
days = st.slider("Track for how many days?", 5, 15, 10)

if st.button("Reset Data"):
    st.session_state.mood = []
    st.session_state.energy = []
    st.session_state.productivity = []

mood = [st.slider(f"Day {i+1} Mood", 1, 10, 5, key=f"mood_{i}") for i in range(days)]
energy = [st.slider(f"Day {i+1} Energy", 1, 10, 5, key=f"energy_{i}") for i in range(days)]
productivity = [st.slider(f"Day {i+1} Productivity", 1, 10, 5, key=f"productivity_{i}") for i in range(days)]

st.session_state.mood = mood
st.session_state.energy = energy
st.session_state.productivity = productivity

st.header(" Habit Tracker")
st.markdown("Check off the habits you followed today:")

habit_list = [" Studied", " Slept 7+ hrs", " Exercised", " Journaled"]
habits = {habit: st.checkbox(habit) for habit in habit_list}
habit_avg = habit_score(habits)

st.header(" Wellness Trend")

fig, ax = plt.subplots()
ax.plot(range(1, days+1), mood, label="Mood", color="#ff66b2", marker='o')
ax.plot(range(1, days+1), energy, label="Energy", color="#ff99cc", marker='o')
ax.plot(range(1, days+1), productivity, label="Productivity", color="#ffb3d9", marker='o')
ax.set_xlabel("Day")
ax.set_ylabel("Score")
ax.set_title("Your Wellness Over Time")
ax.legend()
st.pyplot(fig)

st.header(" Feedback")

mood_avg = recursive_avg(mood)
prod_avg = recursive_avg(productivity)

threshold = st.slider("Set you r wellness streak )", 5, 9, 7)
streak = wellness_streak(mood, threshold=threshold)

if habit_avg < 2:
    st.warning("Try building consistency in your habits. Even small wins count!")
if mood_avg < 5:
    st.info("Low mood trend detected. Consider journaling or talking to a friend.")
if prod_avg > 7:
    st.success("Great productivity! Don’t forget to rest and recharge.")
if habit_avg >= 2 and mood_avg >= 5 and prod_avg <= 7:
    st.write("You're doing well! Keep tracking and reflecting.")

if streak > 0:
    st.success(f" You’re on a {streak}-day wellness streak (threshold ≥ {threshold})! Keep it up!")
else:
    st.warning("No current streak. Aim for consistent good days to build one!")

st.markdown("---")
st.markdown("Made with ❤️ for students by EduWell")
