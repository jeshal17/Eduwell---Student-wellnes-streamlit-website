import streamlit as st
import random
import json
import os
from datetime import datetime, timedelta

userFile = "users.json"

def loadUsers():
    if os.path.exists(userFile):
        with open(userFile, "r") as f:
            return json.load(f)
    return {}

def saveUsers(usersData):
    with open(userFile, "w") as f:
        json.dump(usersData, f, indent=4)

DB_FILE = "JSON2.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({
            "Morning Walk": "30 mins",
            "Meditation": "20 mins",
            "Reading": "1 hour"
        }, f)

with open(DB_FILE, "r") as f:
    activity_db = json.load(f)

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(activity_db, f, indent=4)

st.set_page_config(page_title="Student Hub", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #ffe6f0;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }
    [data-testid="stSidebar"] {
        background-color: #ffb6c1;
    }
    h1, h2, h3 {
        color: #cc0066;
    }
    .stButton > button {
        background-color: #ff66b2;
        color: white;
        border-radius: 10px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    .stTextInput > div > input {
        background-color: #ffccdd;
        color: #660033;
        border-radius: 5px;
    }
    .stSelectbox > div > div {
        background-color: #ffccdd;
        color: #660033;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Welcome to Student Hub</h1>", unsafe_allow_html=True)
st.header("Your All in One Student Companion")
st.markdown("<h3>Stay Focused | Stay Healthy | Stay Ahead</h3>", unsafe_allow_html=True)
st.text("Track your goals, manage your time, and stay motivated.")
st.text("Simple tools to make your study life easier.")
st.markdown("---")

if "attempts" not in st.session_state:
    st.session_state.attempts = {}
if "lockedUntil" not in st.session_state:
    st.session_state.lockedUntil = {}

users = loadUsers()

st.title("Student Hub Login")

mode = st.radio("Select Mode", ["Sign Up", "Login"])

if mode == "Sign Up":
    st.subheader("Create Account")
    newUser = st.text_input("Username ")
    newPass = st.text_input("Password ", type="password")
    q1 = st.text_input("What is your favorite subject?")
    q2 = st.text_input("What is the name of your first school?")

    if st.button("Sign Up"):
        if not newUser or not newPass or not q1 or not q2:
            st.warning("All fields are required.")
        elif len(newUser) < 4:
            st.error("Username must be at least 4 characters.")
        elif len(newPass) < 6:
            st.error("Password must be at least 6 characters.")
        elif newUser in users:
            st.error("Username already exists.")
        else:
            users[newUser] = {
                "password": newPass,
                "kba1": q1.lower(),
                "kba2": q2.lower()
            }
            saveUsers(users)
            st.success("Sign up successful")

elif mode == "Login":
    st.subheader("Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    ans1 = st.text_input("Favorite subject?")
    ans2 = st.text_input("First school name?")

    now = datetime.now()

    if user not in st.session_state.attempts:
        st.session_state.attempts[user] = 0
    if user not in st.session_state.lockedUntil:
        st.session_state.lockedUntil[user] = None

    if st.session_state.lockedUntil[user] and now < st.session_state.lockedUntil[user]:
        remaining = (st.session_state.lockedUntil[user] - now).seconds
        st.warning(f"Login locked. Try again in {remaining} seconds.")
        st.stop()

    if st.button("Login"):
        if not user or not pwd or not ans1 or not ans2:
            st.error("Please fill in all fields.")
        elif user not in users:
            st.error("User not found.")
        else:
            data = users[user]
            if (
                pwd == data["password"]
                and ans1.lower() == data["kba1"]
                and ans2.lower() == data["kba2"]
            ):
                st.success("Login successful")
                st.session_state.attempts[user] = 0
                st.session_state.lockedUntil[user] = None
            else:
                st.session_state.attempts[user] += 1
                attemptsLeft = 3 - st.session_state.attempts[user]

                if attemptsLeft > 0:
                    st.warning(f"Incorrect details. Attempts left: {attemptsLeft}")
                else:
                    st.error("3 failed attempts. Login locked for 30 seconds.")
                    st.session_state.lockedUntil[user] = datetime.now() + timedelta(seconds=30)

st.markdown("---")

st.title("🌸 EduWell Activity Manager")

st.header("📂 Current Activities")
if activity_db:
    for activity, duration in activity_db.items():
        st.markdown(f"**{activity}**: {duration}")
else:
    st.info("No activities available. Add some!")

st.header("➕ Add a New Activity")
new_activity = st.text_input("Activity Name", key="activityName")
new_duration = st.text_input("Duration (e.g. 30 mins)", key="activityDuration")
if st.button("Add Activity"):
    if not new_activity or not new_duration:
        st.error("Please fill in both fields.")
    elif new_activity in activity_db:
        st.error("This activity already exists.")
    else:
        activity_db[new_activity] = new_duration
        save_db()
        st.success(f"Added {new_activity} with duration {new_duration}")

st.header("✏️ Update an Existing Activity")
if activity_db:
    activity_to_update = st.selectbox("Select Activity", list(activity_db.keys()), key="updateSelect")
    updated_duration = st.text_input("New Duration", "", key="updateDuration")
    if st.button("Update Activity"):
        if not updated_duration:
            st.error("Please enter a new duration.")
        else:
            activity_db[activity_to_update] = updated_duration
            save_db()
            st.success(f"Updated {activity_to_update} to {updated_duration}")
else:
    st.info("No activities to update.")

st.header("🗑 Delete an Activity")
if activity_db:
    activity_to_delete = st.selectbox("Select Activity to Delete", list(activity_db.keys()), key="deleteSelect")
    if st.button("Delete Activity"):
        del activity_db[activity_to_delete]
        save_db()
        st.success(f"Deleted {activity_to_delete}")
else:
    st.info("No activities to delete.")

st.header("🎲 Random Activity Suggestion")
if activity_db:
    if st.button("Suggest an Activity"):
        activity, duration = random.choice(list(activity_db.items()))
        st.info(f"Why not try **{activity}** for {duration}?")
else:
    st.info("Add some activities to get suggestions!")

st.markdown("---")
st.markdown("Made with 💖 for students by EduWell")
