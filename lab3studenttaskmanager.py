import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="Student Task Manager", layout="wide")

st.markdown("""
    <style>
        html, body {
            background-color: #ffe6f0;
            font-family: 'Segoe UI', sans-serif;
        }
        .main {
            background: linear-gradient(to bottom, #fff0f5, #ffe6f0);
            padding: 30px;
            border-radius: 12px;
            margin: 0 auto;
            box-shadow: 0px 0px 25px rgba(0,0,0,0.05);
            max-width: 900px;
        }
        .stButton>button {
            background-color: #cc3366;
            color: white;
            font-weight: 600;
            padding: 0.5em 1.5em;
            border-radius: 6px;
        }
        .stButton>button:hover {
            background-color: #b82f5e;
            color: white;
        }
        .highlight {
            background-color: #ffe6f0;
            padding: 12px 20px;
            border-left: 6px solid #cc3366;
            margin-bottom: 10px;
            border-radius: 8px;
        }
        .quote {
            font-style: italic;
            color: #8b3a62;
            text-align: center;
            font-size: 17px;
        }
        .task-title {
            font-weight: bold;
            font-size: 18px;
            color: #b03060;
        }
        .info-label {
            color: #cc3366;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main'>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #b03060;'>Student Task Manager</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

quotes = [
    "Success is the sum of small efforts repeated day in and day out.",
    "Don't watch the clock; do what it does. Keep going.",
    "The secret of getting ahead is getting started.",
    "Discipline is the bridge between goals and accomplishment.",
    "Your future is created by what you do today, not tomorrow.",
    "It always seems impossible until it's done.",
    "Start where you are. Use what you have. Do what you can."
]
quote = random.choice(quotes)

menu = st.sidebar.selectbox(
    "Choose Operation",
    [
        "Dashboard",
        "Add Task",
        "View Tasks",
        "Update Task",
        "Remove Task",
        "Search Task",
        "Task Count"
    ]
)

st.sidebar.markdown("---")


if menu == "Dashboard":
    st.subheader("Overview")
    st.success(f"Total Tasks: {len(st.session_state.tasks)}")
    st.markdown(f"<p class='quote'>\"{quote}\"</p>", unsafe_allow_html=True)
    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks, 1):
            st.markdown(f"""
                <div class="highlight">
                    <div class="task-title">{i}. {task['name']}</div>
                    <div>Deadline: <span class="info-label">{task['deadline']}</span></div>
                    <div>Priority: <span class="info-label">{task['priority']}</span></div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No tasks added yet.")

elif menu == "Add Task":
    st.subheader("Add a New Task")
    task_name = st.text_input("Task Name")
    deadline = st.date_input("Deadline", value=date.today())
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    if st.button("Add"):
        if not task_name.strip():
            st.warning("Please enter a task name.")
        elif deadline < date.today():
            st.warning("Deadline cannot be in the past.")
        else:
            st.session_state.tasks.append({
                "name": task_name.strip(),
                "deadline": str(deadline),
                "priority": priority
            })
            st.success("Task added successfully.")

elif menu == "View Tasks":
    st.subheader("All Tasks")
    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks, 1):
            st.markdown(f"""
                <div class="highlight">
                    <div class="task-title">{i}. {task['name']}</div>
                    <div>Deadline: <span class="info-label">{task['deadline']}</span></div>
                    <div>Priority: <span class="info-label">{task['priority']}</span></div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No tasks available.")

elif menu == "Update Task":
    st.subheader("Update Task")
    if st.session_state.tasks:
        index = st.number_input("Task number to update", 1, len(st.session_state.tasks), step=1)
        task = st.session_state.tasks[index - 1]
        new_name = st.text_input("New Task Name", value=task['name'])
        new_deadline = st.date_input("New Deadline", value=date.fromisoformat(task['deadline']))
        new_priority = st.selectbox("New Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(task['priority']))
        if st.button("Update"):
            if not new_name.strip():
                st.warning("Task name cannot be empty.")
            elif new_deadline < date.today():
                st.warning("Deadline cannot be in the past.")
            else:
                st.session_state.tasks[index - 1] = {
                    "name": new_name.strip(),
                    "deadline": str(new_deadline),
                    "priority": new_priority
                }
                st.success("Task updated successfully.")
    else:
        st.info("No tasks to update.")

elif menu == "Remove Task":
    st.subheader("Remove Task")
    if st.session_state.tasks:
        index = st.number_input("Task number to remove", 1, len(st.session_state.tasks), step=1)
        if st.button("Remove"):
            removed = st.session_state.tasks.pop(index - 1)
            st.success(f"Removed: {removed['name']}")
    else:
        st.info("No tasks to remove.")

elif menu == "Search Task":
    st.subheader("Search Tasks")
    keyword = st.text_input("Enter keyword")
    if keyword:
        results = [t for t in st.session_state.tasks if keyword.lower() in t['name'].lower()]
        if results:
            for i, task in enumerate(results, 1):
                st.markdown(f"""
                    <div class="highlight">
                        <div class="task-title">{i}. {task['name']}</div>
                        <div>Deadline: <span class="info-label">{task['deadline']}</span></div>
                        <div>Priority: <span class="info-label">{task['priority']}</span></div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matching tasks found.")
    else:
        st.info("Type something to search.")

elif menu == "Task Count":
    st.subheader("Total Tasks")
    st.info(f"You have {len(st.session_state.tasks)} tasks.")

st.markdown("</div>", unsafe_allow_html=True)
