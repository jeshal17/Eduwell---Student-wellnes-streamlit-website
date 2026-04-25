import streamlit as st

st.set_page_config(page_title="Student Hub")

st.markdown("<h1 style='color: green;'>Welcome to Student Hub</h1>", unsafe_allow_html=True)
st.header("Your All in One Student Companion")
st.markdown("<h3 style='color: #808080;'>Stay Focused | Stay Healthy | Stay Ahead</h3>", unsafe_allow_html=True)
st.text("Track your goals, manage your time, and stay motivated.")
st.text("Simple tools to make your study life easier.")
 
st.markdown("---")

st.title("Smart Health Advisor - BMI Calculator")
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #e0eafc, #cfdef3);
    }
    </style>
    """,
    unsafe_allow_html=True
)


userName = st.text_input("Enter your name")
userAge = st.number_input("Enter your age", min_value=1, step=1)
userGender = st.radio("Select your gender", ["Male", "Female"])
userWeight = st.number_input("Enter your weight in kilograms", min_value=1.0)
userHeight = st.number_input("Enter your height in meters", min_value=0.5)

def calculateBmi(weight, height):
    return round(weight / (height ** 2), 2)

def getHealthAdvice(bmi, age, gender):
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

if st.button("Calculate BMI"):
    if userHeight > 0 and userWeight > 0 and userAge > 0:
        bmi = calculateBmi(userWeight, userHeight)
        category, advice, note = getHealthAdvice(bmi, userAge, userGender)
        st.success(f"{userName}, your Body Mass Index is {bmi}")
        st.info(f"Category: {category}")
        st.write(f"Health Advice: {advice}")
        if note:
            st.warning(note)
    else:
        st.error("Please ensure all fields are filled correctly.")
        
st.markdown("---")


daily_goal = st.number_input("Set your daily water intake goal (litres)", min_value=0.5, step=0.1)
water_intake = st.number_input("How much water have you consumed today? (litres)", min_value=0.0, step=0.1)

if st.button("Track Water Intake"):
    if water_intake >= daily_goal:
        st.success("Great job! You've reached your hydration goal.")
    else:
        remaining = round(daily_goal - water_intake, 2)
        st.info(f"You need {remaining} more litres to reach your goal.")
