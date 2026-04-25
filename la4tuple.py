import streamlit as st

st.set_page_config(page_title="EduWell - Student & Wellness Manager", layout="centered")
st.title(" EduWell - Student & Wellness Manager")

st.markdown("""
    <style>
        .stApp {
            background-color: #ffe6f0;
        }
        .student-card {
            background-color: white;
            padding: 12px 16px;
            margin: 10px 0;
            border-radius: 12px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s ease-in-out;
        }
        .student-card:hover {
            transform: scale(1.01);
            background-color: #fff0f5;
        }
    </style>
""", unsafe_allow_html=True)

if "entities" not in st.session_state:
    st.session_state.entities = [
        ("S001", "Anson", "CS", "2nd Year", "B"),
        ("S002", "Chrisel", "IT", "1st Year", "B"),
        ("S003", "Sharwari", "CS", "2nd Year", "A"),
        ("S004", "Ujwal", "BHM", "3rd Year", "C")
    ]

if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

entities = st.session_state.entities

st.header(" All Student Entities")
for i, e in enumerate(entities):
    st.markdown(f"""
    <div class="student-card">
        <strong>{i}. ID:</strong> {e[0]}<br>
        <strong>Name:</strong> {e[1]}<br>
        <strong>Branch:</strong> {e[2]}<br>
        <strong>Year:</strong> {e[3]}<br>
        <strong>Grade:</strong> {e[4]}
    </div>
    """, unsafe_allow_html=True)

st.sidebar.title(" Choose Operation")
operation = st.sidebar.radio("What do you want to do?", [
    "Indexing", "Slicing", "Concatenation", "Nesting",
    "Length Calculation", "Searching", "Counting",
    "Unpacking", "Update Grade", "Wellness: Mood Tracker"
])

if operation == "Indexing":
    st.subheader("Indexing: Access Specific Attribute")
    index = st.number_input("Choose entity index", 0, len(entities) - 1)
    attribute_index = st.selectbox("Select attribute", ["ID", "Name", "Branch", "Year", "Grade"])
    attr_idx = ["ID", "Name", "Branch", "Year", "Grade"].index(attribute_index)
    st.success(f"Value: {entities[index][attr_idx]}")

elif operation == "Slicing":
    st.subheader("Slicing: Subset of Attributes")
    index = st.number_input("Choose entity index", 0, len(entities) - 1)
    st.info(f"Sliced (ID, Name, Branch): {entities[index][:3]}")

elif operation == "Concatenation":
    st.subheader("Concatenation: Add New Entity")
    new_id = st.text_input("ID")
    new_name = st.text_input("Name")
    new_branch = st.selectbox("Branch", ["CS", "IT", "BCA", "BHM"])
    new_year = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "Final Year"])
    new_grade = st.selectbox("Grade", ["A", "B", "C", "D", "F"])
    if st.button("Add Entity"):
        if not new_id or not new_name:
            st.error("ID and Name required.")
        elif any(e[0] == new_id for e in entities):
            st.error("ID already exists. Choose a unique one.")
        else:
            new_entity = (new_id, new_name, new_branch, new_year, new_grade)
            st.session_state.entities = entities + [new_entity]
            st.success(f"Entity {new_name} added successfully.")

elif operation == "Nesting":
    st.subheader("Nesting: Group Entities by Branch")
    nested = {}
    for e in entities:
        branch = e[2]
        nested.setdefault(branch, []).append(e)
    for branch, group in nested.items():
        st.write(f"**{branch}** → {group}")

elif operation == "Length Calculation":
    st.subheader("Length Calculation")
    st.write("Total Entities:", len(entities))
    st.write("Attributes per Entity:", len(entities[0]))

elif operation == "Searching":
    st.subheader("Searching by Name")
    search_query = st.text_input("Enter name to search")
    if st.button("Search"):
        found = [e for e in entities if e[1].lower() == search_query.lower()]
        if found:
            st.success(f"Found: {found[0]}")
        else:
            st.error("Entity not found.")

elif operation == "Counting":
    st.subheader("Counting Occurrences of Grade 'A'")
    count_a = sum(1 for e in entities if e[4] == "A")
    st.write("Number of 'A' Grades:", count_a)

elif operation == "Unpacking":
    st.subheader("Unpacking Entity Fields")
    entity_to_unpack = st.selectbox("Select entity", entities)
    student_id, name, branch, year, grade = entity_to_unpack
    st.write("ID:", student_id)
    st.write("Name:", name)
    st.write("Branch:", branch)
    st.write("Year:", year)
    st.write("Grade:", grade)

elif operation == "Update Grade":
    st.subheader("Update using New Tuple (Immutability)")
    selected_entity_index = st.selectbox("Select entity to update", list(range(len(entities))))
    new_grade_value = st.selectbox("New Grade", ["A", "B", "C", "D", "F"], key="immut_update")
    if st.button("Update Grade"):
        updated = list(entities[selected_entity_index])
        updated[4] = new_grade_value
        updated_entity = tuple(updated)
        st.session_state.entities[selected_entity_index] = updated_entity
        st.success(f"Updated Entity: {updated_entity}")

elif operation == "Wellness: Mood Tracker":
    st.subheader("Wellness Feature: Mood Tracker")
    mood = st.selectbox("How are you feeling today?", ["Happy", "Sad", "Angry", "Tired", "Grateful"])
    if st.button("Log Mood"):
        st.session_state.mood_log.append(mood)
        st.success(f"Mood '{mood}' logged successfully.")
    if st.session_state.mood_log:
        st.markdown("### Mood Log Summary")
        mood_counts = {}
        for m in st.session_state.mood_log:
            mood_counts[m] = mood_counts.get(m, 0) + 1
        for mood, count in mood_counts.items():
            st.write(f"{mood}: {count} time(s)")
