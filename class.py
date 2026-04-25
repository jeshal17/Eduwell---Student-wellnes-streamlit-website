import streamlit as st

st.set_page_config(page_title="Student Wellness Set Operations", layout="centered")

st.title(" Student Wellness App – Set Operations")
st.markdown("<h4 style='color: #ff4b4b;'>Analyze Focus, Wellness, and Study Methods</h4>", unsafe_allow_html=True)

def getSetFromUser(label):
    items = st.text_area(f"Enter {label} (comma-separated)").strip()
    return set(item.strip() for item in items.split(",") if item.strip())

focusActivities = getSetFromUser("Focus Activities (e.g., Pomodoro, Deep Work, No Distractions)")
wellnessHabits = getSetFromUser("Wellness Habits (e.g., Meditation, Healthy Eating, Sleep Schedule)")
studyMethods = getSetFromUser("Study Methods (e.g., Flashcards, Group Study, Mind Mapping)")

if st.button("Analyze Wellness Data"):
    if focusActivities and wellnessHabits and studyMethods:
        unionResult = focusActivities.union(wellnessHabits).union(studyMethods)
        intersectionResult = focusActivities.intersection(wellnessHabits).intersection(studyMethods)
        differenceFocusWellness = focusActivities.difference(wellnessHabits)
        differenceStudyFocus = studyMethods.difference(focusActivities)
        symmetricDifferenceFocusWellness = focusActivities.symmetric_difference(wellnessHabits)
        isSubsetWellnessFocus = wellnessHabits.issubset(focusActivities)
        isSupersetFocusStudy = focusActivities.issuperset(studyMethods)

        st.subheader(" Results")
        col1, col2 = st.columns(2)
        col1.markdown(f"<b>All Unique Wellness Elements:</b> {', '.join(unionResult) or 'None'}", unsafe_allow_html=True)
        col1.markdown(f"<b>Common Across All Categories:</b> {', '.join(intersectionResult) or 'None'}", unsafe_allow_html=True)
        col1.markdown(f"<b>In Focus but not in Wellness:</b> {', '.join(differenceFocusWellness) or 'None'}", unsafe_allow_html=True)

        col2.markdown(f"<b>In Study but not in Focus:</b> {', '.join(differenceStudyFocus) or 'None'}", unsafe_allow_html=True)
        col2.markdown(f"<b>Unique to Focus or Wellness:</b> {', '.join(symmetricDifferenceFocusWellness) or 'None'}", unsafe_allow_html=True)
        col2.markdown(f"<b>Wellness is subset of Focus:</b> {isSubsetWellnessFocus}", unsafe_allow_html=True)
        col2.markdown(f"<b>Focus is superset of Study:</b> {isSupersetFocusStudy}", unsafe_allow_html=True)

    else:
        st.error("Please fill all three categories before analysis.")


