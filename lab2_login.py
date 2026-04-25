import streamlit as st
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

def calculateBmi(weight, height):
    return round(weight / (height ** 2), 2)

def getHealthAdvice(bmi, age, gender):
    category = ""
    advice = ""
    if bmi < 18.5:
        category = "Underweight"
        advice = "Eat nutritious foods and increase calorie intake."
    elif 18.5 <= bmi < 24.9:
        category = "Normal"
        advice = "Maintain your healthy habits."
    elif 25 <= bmi < 29.9:
        category = "Overweight"
        advice = "Engage in physical activity and monitor your diet."
    else:
        category = "Obese"
        advice = "Consult a healthcare provider for personalized weight management."

    note = ""
    if gender == "Female" and age > 45:
        note = "Note: Women over 45 may experience hormonal weight changes."
    elif gender == "Male" and age > 50:
        note = "Note: Men over 50 should monitor heart health regularly."

    return category, advice, note

st.set_page_config(page_title="Student Hub")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #FFD1DC;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }
    [data-testid="stSidebar"] {
        background-color: #FFB6C1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='color: green;'>Welcome to Student Hub</h1>", unsafe_allow_html=True)
st.header("Your All in One Student Companion")
st.markdown("<h3 style='color: #808080;'>Stay Focused | Stay Healthy | Stay Ahead</h3>", unsafe_allow_html=True)
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
        if user not in users:
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

st.title("Smart Health Advisor - BMI Calculator")

userName = st.text_input("Enter your name", key="bmiNameInput")
userAge = st.number_input("Enter your age", min_value=1, step=1, key="bmiAgeInput")
userGender = st.radio("Select your gender", ["Male", "Female"], key="bmiGenderInput")
userWeight = st.number_input("Enter your weight in kilograms", min_value=1.0, key="bmiWeightInput")
userHeight = st.number_input("Enter your height in meters", min_value=0.5, key="bmiHeightInput")

if st.button("Calculate BMI", key="bmiButton"):
    if userHeight > 0 and userWeight > 0 and userAge > 0:
        bmi = calculateBmi(userWeight, userHeight)
        category, advice, note = getHealthAdvice(bmi, userAge, userGender)

        st.success(f"{userName}, your Body Mass Index is {bmi}")
        st.info(f"Category: {category}")
        st.write(f"Health Advice: {advice}")
        if note:
            st.warning(note)
    else:
        st.error("Please ensure all fields are filled correctly for BMI calculation.")
