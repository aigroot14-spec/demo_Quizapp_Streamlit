import streamlit as st

# 1. Page Configuration - Wide layout to utilize more space
st.set_page_config(
    page_title="Streamlit Master Quiz",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for better aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize Session State
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_complete = False

# 4. Quiz Data
quiz_data = [
    {
        "question": "Which Python library is primarily used for Streamlit's data handling?",
        "options": ["Pandas", "Django", "Flask", "TensorFlow"],
        "answer": "Pandas",
        "fact": "Pandas is the backbone of data manipulation in Python!"
    },
    {
        "question": "What is the default port for a Streamlit app?",
        "options": ["8080", "5000", "8501", "3000"],
        "answer": "8501",
        "fact": "You can change this using the --server.port command."
    },
    {
        "question": "Which keyword is used to store data across reruns in Streamlit?",
        "options": ["st.cache", "st.session_state", "st.store", "st.save"],
        "answer": "st.session_state",
        "fact": "Session State is vital for building interactive web apps."
    }
]

def restart_quiz():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_complete = False

# --- SIDEBAR (Fills the left space) ---
with st.sidebar:
    st.title("🎮 Quiz Dashboard")
    st.info("Level: **Intermediate**")
    st.markdown("---")
    st.write("### User Profile")
    st.text_input("Player Name", placeholder="Enter name...")
    st.markdown("---")
    if st.button("Reset / Restart Quiz"):
        restart_quiz()
        st.rerun()

# --- MAIN UI (Fills the center and right space) ---
if not st.session_state.quiz_complete:
    # Use columns to center the quiz and add a stats sidebar on the right
    col_main, col_spacer, col_stats = st.columns([3, 0.5, 1.2])

    with col_main:
        st.title("🧠 Tech Trivia Challenge")
        st.write("Test your knowledge of the Python ecosystem!")
        
        # Progress bar
        progress_val = (st.session_state.current_question) / len(quiz_data)
        st.progress(progress_val)
        
        # Question Card
        q_idx = st.session_state.current_question
        item = quiz_data[q_idx]
        
        with st.container(border=True):
            st.subheader(f"Question {q_idx + 1} of {len(quiz_data)}")
            st.markdown(f"### {item['question']}")
            
            with st.form(key=f"q_{q_idx}"):
                user_choice = st.radio("Select your answer:", item['options'], index=None)
                submitted = st.form_submit_button("Submit Answer →")
                
                if submitted:
                    if user_choice == item['answer']:
                        st.session_state.score += 1
                        st.success("Correct!")
                    else:
                        st.error(f"Incorrect! The answer was {item['answer']}")
                    
                    if st.session_state.current_question < len(quiz_data) - 1:
                        st.session_state.current_question += 1
                        st.rerun()
                    else:
                        st.session_state.quiz_complete = True
                        st.rerun()

    with col_stats:
        st.write("### 📊 Live Stats")
        st.metric("Current Score", st.session_state.score)
        st.metric("Questions Left", len(quiz_data) - st.session_state.current_question)
        
        st.markdown("---")
        st.write("💡 **Did you know?**")
        st.caption(quiz_data[st.session_state.current_question]['fact'])

else:
    # --- FINAL SCREEN ---
    st.balloons()
    center_col_1, center_col_2, center_col_3 = st.columns([1, 2, 1])
    
    with center_col_2:
        st.success("🎉 **Quiz Completed Successfully!**")
        final_percent = (st.session_state.score / len(quiz_data)) * 100
        
        st.write("### Your Performance")
        c1, c2 = st.columns(2)
        c1.metric("Final Score", f"{st.session_state.score}/{len(quiz_data)}")
        c2.metric("Accuracy", f"{final_percent:.0f}%")
        
        if st.button("Play Again", use_container_width=True):
            restart_quiz()
            st.rerun()