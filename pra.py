import streamlit as st
import random

# --- 1. QUIZ DATA (Consolidated 40 Questions) ---
# The correct answers are stored in the 'a' key and are used for checking.
ALL_QUIZ_DATA = {
    "AI Basics, Data, Information": [
        {"q": "What is the fundamental component that an AI system primarily needs to learn and make decisions?", "a": "data", "options": ["Code", "Energy", "Data", "The Internet"]},
        {"q": "Data that has been processed, organized, and structured to provide context and meaning is called?", "a": "information", "options": ["Raw Data", "Information", "Algorithm", "Wisdom"]},
        {"q": "Which term is defined as the simulation of human intelligence processes by machines?", "a": "artificial intelligence", "options": ["Machine Learning", "Data Mining", "Artificial Intelligence", "Cognitive Science"]},
        {"q": "Which of the following best represents **raw data**?", "a": "a list of gps coordinates", "options": ["A sales report", "A list of GPS coordinates", "A chart showing averages", "A newspaper article"]},
        {"q": "The process of converting raw data into information is often called?", "a": "data processing", "options": ["Machine Vision", "Data Processing", "Neural Networking", "Algorithmic Guessing"]},
        {"q": "A machine learning model predicting a house price is using: (Information or Raw Data?)", "a": "information", "options": ["Information", "Raw Data"]},
        {"q": "Which characteristic is essential for data to be considered high-quality input for AI training? (Accuracy or Volume?)", "a": "accuracy", "options": ["Volume", "Accuracy"]},
        {"q": "In the hierarchy of knowledge (Data → Information → ? → Wisdom), what level comes next?", "a": "knowledge", "options": ["Wisdom", "Knowledge", "Facts", "Experience"]},
        {"q": "Why is a large volume of data important for AI systems? (To reduce bias or to simplify the algorithm?)", "a": "to reduce bias", "options": ["To run faster", "To simplify the algorithm", "To reduce bias", "To decrease memory"]},
        {"q": "What term describes the ability of an AI system to take the derived information and use it to solve a problem or guide action?", "a": "intelligence", "options": ["Processing", "Intelligence", "Storage", "Feature Extraction"]},
    ],
    "Narrow vs. General AI": [
        {"q": "Which type of AI is capable of performing only a single, specific task?", "a": "narrow ai", "options": ["General AI", "Superintelligence", "Narrow AI", "Cognitive AI"]},
        {"q": "What is the current status of Artificial General Intelligence (AGI)?", "a": "theoretical concept that does not yet exist", "options": ["Widely used", "Theoretical concept that does not yet exist", "Achieved in the 1990s", "Confined to academic labs"]},
        {"q": "A system that can master chess, stock market, and spontaneously learn to cook would be an example of:", "a": "general ai (agi)", "options": ["Narrow AI", "Artificial Superintelligence", "General AI (AGI)", "Hybrid AI"]},
        {"q": "Which example below is a clear instance of Narrow AI?", "a": "an algorithm that recommends products", "options": ["A robot that can write a novel", "An algorithm that recommends products", "A self-aware machine", "A machine that passes the Turing test"]},
        {"q": "The ability to exhibit self-awareness and independent reasoning is a defining trait of which theoretical AI level?", "a": "artificial general intelligence (agi)", "options": ["Artificial Superintelligence", "Narrow AI", "Artificial General Intelligence (AGI)", "Machine Learning"]},
        {"q": "Why are current voice assistants (like Siri or Alexa) considered Narrow AI?", "a": "they rely on pre-programmed algorithms for specific tasks", "options": ["Cannot connect to the internet", "Can learn any new skill instantly", "They rely on pre-programmed algorithms for specific tasks", "Only used by a small fraction"]},
        {"q": "Which type of AI is sometimes referred to as 'Weak AI'?", "a": "narrow ai", "options": ["Narrow AI", "General AI", "Superintelligence", "Reinforcement Learning"]},
        {"q": "The concept of an AI system vastly exceeding human intelligence in all intellectual domains is known as:", "a": "artificial superintelligence (asi)", "options": ["Artificial General Intelligence", "Artificial Superintelligence (ASI)", "Hypothetical AI", "Deep Learning"]},
        {"q": "What is the main limitation of Narrow AI systems?", "a": "they cannot adapt or generalize knowledge to new problems", "options": ["Require continuous human supervision", "Too expensive to be commercially viable", "They cannot adapt or generalize knowledge to new problems", "Only operate with text"]},
        {"q": "A system designed specifically for diagnosing a single disease from X-rays is best categorized as:", "a": "narrow ai", "options": ["General AI", "Narrow AI", "Autonomous AI", "Learning AI"]},
    ],
    "Core Concepts of AI": [
        {"q": "What is the primary focus of **Machine Learning (ML)**?", "a": "enabling systems to learn from data without explicit programming", "options": ["Writing explicit code", "Enabling systems to learn from data without explicit programming", "Simulating the entire human brain", "Creating specialized hardware"]},
        {"q": "What is a **Neural Network** primarily modeled after?", "a": "the structure and function of the human brain", "options": ["A spider web", "A computer chip", "The structure and function of the human brain", "Water flow in a river"]},
        {"q": "The raw, labeled data used to teach a Machine Learning model is known as the:", "a": "training data", "options": ["Testing Data", "Training Data", "Feature Set", "Hyperparameters"]},
        {"q": "What distinguishes **Deep Learning (DL)** from traditional Machine Learning?", "a": "dl uses neural networks with multiple (deep) hidden layers", "options": ["Used only for image processing", "Does not use data", "DL uses neural networks with multiple (deep) hidden layers", "Requires only one line of code"]},
        {"q": "In supervised learning, what is the 'target' variable that the model is trying to predict or classify?", "a": "label", "options": ["Input", "Feature", "Bias", "Label"]},
        {"q": "What is an **Algorithm** in the context of AI?", "a": "a set of well-defined instructions for a task, which a computer follows", "options": ["Physical hardware", "Type of training data", "A set of well-defined instructions for a task, which a computer follows", "The final result or output of the model"]},
        {"q": "The distinct, measurable properties or attributes of a phenomenon being observed are called:", "a": "features", "options": ["Features", "Weights", "Metrics", "Biases"]},
        {"q": "Which type of Machine Learning involves the model exploring an environment and receiving rewards or penalties for its actions?", "a": "reinforcement learning", "options": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Transfer Learning"]},
        {"q": "What does the term **'Unsupervised Learning'** imply about the training data?", "a": "the data does not contain any pre-labeled outputs or answers", "options": ["Data is labeled", "Output is always wrong", "The data does not contain any pre-labeled outputs or answers", "Taught by a human teacher"]},
        {"q": "The process of fine-tuning the weights and biases in a neural network to minimize errors is known as:", "a": "training", "options": ["Deployment", "Training", "Validation", "Feature Selection"]},
    ],
    "Human and AI Centered Design": [
        {"q": "What is the core principle of **Human-Centered Design (HCD)** when applied to AI?", "a": "focusing on the needs, goals, and context of the end-user", "options": ["Maximizing accuracy", "Focusing on the needs, goals, and context of the end-user", "Building deep neural networks", "Automating every single task"]},
        {"q": "A system that provides clear, simple explanations for its outputs is demonstrating the design principle of:", "a": "explainability", "options": ["Opacity", "Automation", "Explainability", "Clustering"]},
        {"q": "Mitigating 'algorithmic bias' is primarily a concern related to which HCD ethical pillar?", "a": "fairness", "options": ["Efficiency", "Autonomy", "Fairness", "Complexity"]},
        {"q": "What is meant by 'AI Augmentation' in design?", "a": "the ai assists the human to make the human more effective", "options": ["AI completely replaces human", "The AI assists the human to make the human more effective", "Making the data set larger", "Allowing user to train the AI with custom code"]},
        {"q": "To ensure **'user control'** in an AI system, a designer should include which feature?", "a": "a simple 'on/off' switch to immediately disable the ai's function", "options": ["An on/off switch to disable the AI", "Making the source code public", "Hiding internal processes", "Automatic updates without user input"]},
        {"q": "Why is **Privacy** a major concern in AI design?", "a": "ai systems often require vast amounts of personal, sensitive data", "options": ["AI needs to keep its algorithms secret", "AI systems often require vast amounts of personal, sensitive data", "Privacy laws require less accuracy", "Privacy ensures the AI gives the correct answer"]},
        {"q": "In the 'Human-in-the-Loop' approach, what is the human's primary role?", "a": "to provide critical oversight, correct errors, and handle edge cases", "options": ["To passively observe", "To provide critical oversight, correct errors, and handle edge cases", "To write the initial code", "To provide electricity and maintenance"]},
        {"q": "When an AI fails to identify a user group due to underrepresentation in the training data, this is a failure of:", "a": "data representativeness", "options": ["High Recall", "Data Robustness", "Data Representativeness", "Algorithmic Complexity"]},
        {"q": "Which of these is **NOT** a key ethical consideration in AI-Centered Design?", "a": "the price of the cloud computing resources", "options": ["Accountability", "The price of the cloud computing resources", "Transparency", "Fairness"]},
        {"q": "Choosing to brake suddenly to save 10 pedestrians at the risk of occupant injury is navigating a design **___________**.", "a": "ethical dilemma", "options": ["Augmentation", "Bias Check", "Ethical Dilemma", "Clustering Problem"]},
    ]
}


# --- 2. STREAMLIT APP SETUP ---

def initialize_state():
    """Initializes session state variables for scores and quiz tracking."""
    if 'scores' not in st.session_state:
        st.session_state.scores = {'Team Alpha': 0, 'Team Beta': 0, 'Team Gamma': 0}
    if 'current_team' not in st.session_state:
        st.session_state.current_team = 'Team Alpha'
    if 'quiz_topic' not in st.session_state:
        st.session_state.quiz_topic = list(ALL_QUIZ_DATA.keys())[0]
    if 'quiz_state' not in st.session_state or 'quiz_topic' not in st.session_state or st.session_state.quiz_topic != st.session_state.get('last_topic'):
        # State holds the shuffled questions for the current topic
        st.session_state.quiz_state = random.sample(ALL_QUIZ_DATA[st.session_state.quiz_topic], len(ALL_QUIZ_DATA[st.session_state.quiz_topic]))
        st.session_state.last_topic = st.session_state.quiz_topic
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    # Temporary state to hold submission result
    if 'answer_submitted' not in st.session_state:
        st.session_state.answer_submitted = False
    if 'is_correct' not in st.session_state:
        st.session_state.is_correct = None


def check_answer(user_answer, correct_answer):
    """Checks the answer and sets session state flags for feedback."""
    st.session_state.answer_submitted = True
    
    if user_answer.lower() == correct_answer.lower():
        st.session_state.scores[st.session_state.current_team] += 1
        st.session_state.is_correct = True
        return True
    else:
        st.session_state.is_correct = False
        return False

def reset_quiz():
    """Resets the quiz state for the new topic selection."""
    st.session_state.current_question_index = 0
    st.session_state.quiz_state = random.sample(ALL_QUIZ_DATA[st.session_state.quiz_topic], len(ALL_QUIZ_DATA[st.session_state.quiz_topic]))
    st.session_state.last_topic = st.session_state.quiz_topic
    st.session_state.answer_submitted = False
    st.session_state.is_correct = None
    st.experimental_rerun()


# --- 3. MAIN APPLICATION FUNCTION ---

def team_quiz_app():
    st.set_page_config(layout="wide", page_title="AI Concepts Team Quiz")
    st.title("🏆 AI Concepts Team Quiz")
    st.caption("Answer questions to earn points for your team!")

    initialize_state()
    
    col_score, col_main = st.columns([1, 3])

    # --- Scoreboard Sidebar ---
    with col_score:
        st.header("Scoreboard")
        
        # Display Scores
        sorted_scores = sorted(st.session_state.scores.items(), key=lambda item: item[1], reverse=True)
        for team, score in sorted_scores:
            score_text = f"### 🥇 **{team}**: {score} Pts" if team == st.session_state.current_team else f"#### {team}: {score} Pts"
            st.markdown(score_text)
        
        st.markdown("---")

        # Team Selection
        st.subheader("Current Team Answering")
        team_options = list(st.session_state.scores.keys())
        st.session_state.current_team = st.selectbox("Select Team:", team_options, index=team_options.index(st.session_state.current_team))
        
        st.subheader("Topic Selection")
        # Topic Selector and Reset Button
        new_topic = st.selectbox("Choose Quiz Topic:", list(ALL_QUIZ_DATA.keys()))
        
        # Handle topic change logic outside of the quiz form submission
        if new_topic != st.session_state.quiz_topic:
            st.session_state.quiz_topic = new_topic
            st.info(f"Quiz topic changed to **{st.session_state.quiz_topic}**. Press 'Next Question' to start.")
            reset_quiz()


    # --- Main Quiz Area ---
    with col_main:
        st.header(f"Topic: {st.session_state.quiz_topic}")
        
        # Check if the quiz is finished
        if st.session_state.current_question_index >= len(st.session_state.quiz_state):
            st.balloons()
            st.success("🎉 QUIZ COMPLETED! All questions answered for this topic.")
            st.button("Start New Quiz / Reset Topic", on_click=reset_quiz)
            return

        # Get the current question
        q_index = st.session_state.current_question_index
        current_q = st.session_state.quiz_state[q_index]

        st.subheader(f"Question {q_index + 1} of {len(st.session_state.quiz_state)}")
        
        # Display the question
        st.markdown(f"### {current_q['q']}")
        
        # Logic to display results and next button after submission
        if st.session_state.answer_submitted:
            correct_answer = current_q['a']
            if st.session_state.is_correct:
                st.success(f"✅ Correct! **{st.session_state.current_team}** gets 1 point!")
            else:
                # *** Explicitly showing the correct answer here ***
                st.error(f"❌ Incorrect. The correct answer was: **{correct_answer}**.")
            
            # Button to move to the next question, which clears the feedback state
            if st.button("Next Question >>"):
                st.session_state.current_question_index += 1
                st.session_state.answer_submitted = False
                st.session_state.is_correct = None
                st.experimental_rerun()
            return # Stop processing the form part until 'Next Question' is clicked

        
        # Determine the input type (Multiple Choice or Simple Short Answer)
        if 'options' in current_q and len(current_q['options']) > 1:
            # Multiple Choice (Radio Buttons)
            with st.form(key=f"q_form_{q_index}"):
                user_answer = st.radio("Choose the best answer:", current_q['options'], index=None)
                submitted = st.form_submit_button("Submit Answer")

                if submitted:
                    if user_answer is not None:
                        check_answer(user_answer, current_q['a'])
                        # Rerun to show feedback and 'Next Question' button
                        st.experimental_rerun() 
                    else:
                        st.warning("Please select an answer before submitting.")
        else:
            # Simple Short Answer (Text Input)
            with st.form(key=f"q_form_{q_index}"):
                user_answer = st.text_input("Your Answer (Type the key term/phrase):")
                submitted = st.form_submit_button("Submit Answer")

                if submitted:
                    if user_answer.strip() != "":
                        check_answer(user_answer, current_q['a'])
                        # Rerun to show feedback and 'Next Question' button
                        st.experimental_rerun()
                    else:
                        st.warning("Please enter an answer before submitting.")

# --- 4. RUN THE APP ---

if __name__ == "__main__":
    team_quiz_app()