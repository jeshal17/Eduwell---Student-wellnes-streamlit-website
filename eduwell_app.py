import streamlit as st
from datetime import date, time, datetime, timedelta
import matplotlib.pyplot as plt
import collections

st.set_page_config(page_title="EduWell - Your Student Companion", layout="centered")

st.markdown("""
<style>
    .reportview-container { background: #f7e8f0; }
    .sidebar .sidebar-content { background: #f2d8e4; }
    h1, h2, h3, h4, h5, h6 { color: #d08fa0; }
    .stButton>button {
        background-color: #d08fa0;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #e0a3b0;
        color: white;
    }
    .stRadio div[role="radiogroup"] label,
    .stSelectbox div[role="listbox"],
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background-color: #fcecf4;
        color: #6a6a6a;
    }
    .stMetric > div > div > div { color: #d08fa0; }
    .stMetric > div > div:nth-child(2) { color: #6a6a6a; }
    .stPlotlyChart {
        background-color: #fcecf4;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    }
    code {
        background-color: #fcecf4;
        color: #6a6a6a;
        padding: 2px 4px;
        border-radius: 3px;
    }
    pre {
        background-color: #fcecf4;
        color: #6a6a6a;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        overflow-x: auto;
    }
    .home-banner {
        background-color: #e0a3b0;
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

def homeDashboard():
    st.markdown("<h2 style='color:#d08fa0;'>Welcome to EduWell!</h2>", unsafe_allow_html=True)
    st.write("Your personal companion for academic success and well-being.")
    st.markdown("""
    <div class="home-banner">
        <h3 style="color:white; margin-bottom: 5px;">Your Journey to Success Starts Here!</h3>
        <p style="color:white; font-size: 16px;">Empowering students with tools for well-being and academic planning.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### Quick Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.info("Track your mood daily to understand your emotional patterns.")
        st.info("Build a personalized routine that fits your unique schedule.")
    with col2:
        st.info("Stay hydrated and keep your energy levels up.")
        st.info("Plan your study sessions effectively for better focus.")
    st.markdown("---")
    st.markdown("Ready to start? Select a feature from the sidebar!")

def moodTracker():
    st.markdown("<h2 style='color:#d08fa0;'>Mood Tracker</h2>", unsafe_allow_html=True)
    if "moodEntries" not in st.session_state:
        st.session_state.moodEntries = []
    st.markdown("#### How are you feeling today?")
    moodOptions = ["Happy 😊", "Stressed 😫", "Anxious 😟", "Motivated 💪", "Tired 😴", "Excited 🤩"]
    mood = st.radio("Choose one:", moodOptions, key="moodRadio")
    st.markdown("#### What contributed most to your mood?")
    causeOptions = ["Exams", "Sleep", "Family", "Friends", "Workload", "Health", "Social Life", "Hobbies", "Other"]
    cause = st.selectbox("Select one:", causeOptions, key="moodCause")
    note = st.text_area("Any notes you'd like to add?", key="moodNote")
    if st.button("Save Mood Entry"):
        entry = {
            "date": str(date.today()),
            "mood": mood,
            "cause": cause,
            "note": note
        }
        st.session_state.moodEntries.append(entry)
        st.success(f"Mood saved for {date.today()} – {mood} due to {cause}.")
    st.markdown("---")
    st.markdown("#### Your Mood History")
    if st.session_state.moodEntries:
        for i, entry in enumerate(reversed(st.session_state.moodEntries)):
            st.write(f"**{entry['date']}**: Felt **{entry['mood']}** because of **{entry['cause']}**.")
            if entry['note']:
                st.write(f"_Notes: {entry['note']}_")
            if i < len(st.session_state.moodEntries) - 1:
                st.markdown("---")
    else:
        st.info("No mood entries yet. Start tracking how you feel!")
    st.markdown("---")
    st.markdown("#### Mood Trends (Last 7 Days)")
    if st.session_state.moodEntries:
        sevenDaysAgo = date.today() - timedelta(days=7)
        recentMoods = [entry["mood"] for entry in st.session_state.moodEntries if datetime.strptime(entry["date"], "%Y-%m-%d").date() >= sevenDaysAgo]
        if recentMoods:
            moodCounts = collections.Counter(recentMoods)
            moodLabels = list(moodCounts.keys())
            moodValues = list(moodCounts.values())
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(moodLabels, moodValues, color="#d08fa0")
            ax.set_title("Mood Frequency in Last 7 Days", color="#d08fa0")
            ax.set_ylabel("Number of Entries", color="#6a6a6a")
            ax.tick_params(axis="x", colors="#6a6a6a")
            ax.tick_params(axis="y", colors="#6a6a6a")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.patch.set_facecolor("#fcecf4")
            fig.set_facecolor("#f7e8f0")
            st.pyplot(fig)
        else:
            st.info("Not enough mood entries in the last 7 days to show trends.")
    else:
        st.info("Track your mood to see trends here!")

def dailyRoutineBuilder():
    st.markdown("<h2 style='color:#d08fa0;'>Daily Routine Builder</h2>", unsafe_allow_html=True)
    if "routine" not in st.session_state:
        st.session_state.routine = {}
    st.markdown("#### Plan your ideal day by setting times for each activity.")
    blocks = ["Wake Up", "Morning Prep", "Study Block 1", "Break/Snack", "Lunch", "Study Block 2", "Exercise", "Dinner", "Relaxation", "Sleep"]
    newRoutine = {}
    for i, block in enumerate(blocks):
        keyName = f"routine{i}{block.replace(' ', '')}"
        currentTime = st.session_state.routine.get(block, time(8, 0) if "Wake Up" in block else time(9, 0))
        newTime = st.time_input(f"{block} Time", value=currentTime, key=keyName)
        newRoutine[block] = newTime
    if st.button("Save Daily Routine"):
        st.session_state.routine = newRoutine
        st.success("Routine Saved Successfully!")
    st.markdown("---")
    st.markdown("#### Your Current Routine")
    if st.session_state.routine:
        sortedRoutine = sorted(st.session_state.routine.items(), key=lambda item: item[1])
        for k, v in sortedRoutine:
            st.write(f"**{k}:** {v.strftime('%I:%M %p')}")
    else:
        st.info("No routine set yet. Build your daily plan!")

def waterHydrationReminder():
    st.markdown("<h2 style='color:#d08fa0;'>Hydration Tracker</h2>", unsafe_allow_html=True)
    if "glasses" not in st.session_state:
        st.session_state.glasses = 0
    st.markdown("#### Keep track of your daily water intake!")
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Add 1 Glass 💧"):
            st.session_state.glasses += 1
            st.toast("Stay hydrated!")
    with col2:
        if st.button("Reset Daily"):
            st.session_state.glasses = 0
            st.toast("Hydration progress reset for today.")
    with col3:
        st.metric("Glasses of Water Drank Today", st.session_state.glasses)
    st.markdown("---")
    st.write("Aim for 8 glasses a day for optimal health and focus!")
    st.markdown("<h3 style='color:#d08fa0;'>Hydration Tips</h3>", unsafe_allow_html=True)
    with st.expander("Click here for quick hydration tips!"):
        st.markdown("""
        <ul>
            <li style="color:#6a6a6a;">Carry a reusable water bottle and refill it throughout the day.</li>
            <li style="color:#6a6a6a;">Set reminders on your phone or use this tracker!</li>
            <li style="color:#6a6a6a;">Drink a glass of water before each meal.</li>
            <li style="color:#6a6a6a;">Eat water-rich foods like watermelon, cucumber, oranges.</li>
        </ul>
        """, unsafe_allow_html=True)

def studyPlanner():
    st.markdown("<h2 style='color:#d08fa0;'>Study Planner</h2>", unsafe_allow_html=True)
    if "studySlots" not in st.session_state:
        st.session_state.studySlots = []
    with st.form("studySlotForm"):
        subject = st.text_input("Subject", key="studySubject")
        start = st.time_input("Start Time", key="studyStart")
        end = st.time_input("End Time", key="studyEnd")
        submitted = st.form_submit_button("Add Study Slot")
        if submitted:
            if subject and start and end:
                if end > start:
                    st.session_state.studySlots.append({"subject": subject, "start": str(start), "end": str(end)})
                    st.success(f"{subject}: {start.strftime('%I:%M %p')} to {end.strftime('%I:%M %p')}")
                else:
                    st.error("End time must be after start time.")
            else:
                st.error("Please fill in all fields.")
    st.markdown("---")
    if st.session_state.studySlots:
        sortedSlots = sorted(st.session_state.studySlots, key=lambda x: time.fromisoformat(x["start"]))
        for slot in sortedSlots:
            st.write(f"**{slot['subject']}**: {time.fromisoformat(slot['start']).strftime('%I:%M %p')} - {time.fromisoformat(slot['end']).strftime('%I:%M %p')}")
            st.markdown("---")
    else:
        st.info("No study sessions planned yet.")

def notesVault():
    st.markdown("<h2 style='color:#d08fa0;'>Notes Vault</h2>", unsafe_allow_html=True)
    if "notes" not in st.session_state:
        st.session_state.notes = []
    with st.form("noteForm"):
        subject = st.text_input("Subject / Topic", key="noteSubject")
        noteContent = st.text_area("Write your notes here:", height=200, key="noteContent")
        submitted = st.form_submit_button("Save Note")
        if submitted:
            if subject and noteContent:
                st.session_state.notes.append({"subject": subject, "content": noteContent, "date": str(date.today())})
                st.success(f"Note for '{subject}' saved!")
            else:
                st.error("Please provide both subject and content.")
    st.markdown("---")
    for note in reversed(st.session_state.notes):
        with st.expander(f"**{note['subject']}** - ({note['date']})"):
            st.write(note["content"])

def expenseSplitter():
    st.markdown("<h2 style='color:#d08fa0;'>Expense Splitter</h2>", unsafe_allow_html=True)
    totalBill = st.number_input("Total Bill Amount (₹)", min_value=0.0, format="%.2f", key="totalBill")
    numPeople = st.number_input("Number of People", min_value=1, value=1, step=1, key="numPeople")
    equalShare = totalBill / numPeople if numPeople > 0 else 0.0
    st.markdown(f"**Equal Share Per Person:** <span style='color:#d08fa0;'>₹{equalShare:.2f}</span>", unsafe_allow_html=True)
    if "payments" not in st.session_state:
        st.session_state.payments = []
    with st.form("addPersonPaymentForm", clear_on_submit=True):
        personName = st.text_input("Person's Name", key="personNameInput")
        amountPaid = st.number_input("Amount Paid by Them (₹)", min_value=0.0, format="%.2f", key="amountPaidInput")
        if st.form_submit_button("Add Person & Payment") and personName:
            st.session_state.payments.append({"name": personName, "paid": amountPaid})
            st.success(f"Added {personName} who paid ₹{amountPaid:.2f}.")
    if st.session_state.payments:
        totalPaid = sum(p["paid"] for p in st.session_state.payments)
        for p in st.session_state.payments:
            st.write(f"- **{p['name']}**: Paid ₹{p['paid']:.2f}")
        st.markdown(f"**Total Amount Paid:** <span style='color:#d08fa0;'>₹{totalPaid:.2f}</span>", unsafe_allow_html=True)
        st.markdown("#### What Everyone Owes/Is Owed")
        for p in st.session_state.payments:
            diff = p["paid"] - equalShare
            if diff < 0:
                st.write(f"**{p['name']}** owes: <span style='color:#FF4B4B;'>₹{-diff:.2f}</span>", unsafe_allow_html=True)
            elif diff > 0:
                st.write(f"**{p['name']}** is owed: <span style='color:#008000;'>₹{diff:.2f}</span>", unsafe_allow_html=True)
            else:
                st.write(f"**{p['name']}**: Paid exactly their share.")
        if st.button("Clear All Payments", key="clearPayments"):
            st.session_state.payments = []
            st.success("All payments cleared!")
            st.experimental_rerun()

st.sidebar.markdown("<h1 style='color:#d08fa0;'>EduWell</h1>", unsafe_allow_html=True)
st.sidebar.markdown("Your companion for well-being & studies.")
appMode = st.sidebar.radio("Go to", ["Home", "Mood Tracker", "Daily Routine", "Hydration", "Study Planner", "Notes Vault", "Expense Splitter"])

if appMode == "Home":
    homeDashboard()
elif appMode == "Mood Tracker":
    moodTracker()
elif appMode == "Daily Routine":
    dailyRoutineBuilder()
elif appMode == "Hydration":
    waterHydrationReminder()
elif appMode == "Study Planner":
    studyPlanner()
elif appMode == "Notes Vault":
    notesVault()
elif appMode == "Expense Splitter":
    expenseSplitter()

st.sidebar.markdown("---")
st.sidebar.info("Designed with care for students.")
