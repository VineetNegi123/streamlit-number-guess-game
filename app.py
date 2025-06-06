import streamlit as st
import random
import time

# Set page config
st.set_page_config(page_title="Number Master", page_icon="🎯", layout="centered")

# Initialize session state
if "number" not in st.session_state:
    st.session_state.number = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "max_time" not in st.session_state:
    st.session_state.max_time = 30
if "message" not in st.session_state:
    st.session_state.message = ""

# Title
st.title("🎯 Number Master: Guess & Win")

# Difficulty selection
st.sidebar.title("⚙️ Settings")
difficulty = st.sidebar.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
if difficulty != st.session_state.difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.message = ""

# Set number range and timer
if difficulty == "Easy":
    number_range = 1, 20
    st.session_state.max_time = 30
elif difficulty == "Medium":
    number_range = 1, 50
    st.session_state.max_time = 45
else:
    number_range = 1, 100
    st.session_state.max_time = 60

# Start new round
if st.session_state.number == 0:
    st.session_state.number = random.randint(*number_range)
    st.session_state.start_time = time.time()

# Timer display
elapsed = int(time.time() - st.session_state.start_time)
remaining = st.session_state.max_time - elapsed
if remaining <= 0:
    st.warning("⏰ Time's up! The number was: " + str(st.session_state.number))
    st.session_state.number = 0
    st.session_state.streak = 0
else:
    st.write(f"⏱️ Time Remaining: **{remaining}** seconds")

# Game input
guess = st.number_input(f"Guess the number ({number_range[0]} - {number_range[1]}):", min_value=number_range[0], max_value=number_range[1], step=1)

if st.button("🎯 Submit Guess"):
    if remaining <= 0:
        st.warning("⏰ Time's up! Start a new round.")
    else:
        if guess < st.session_state.number:
            st.session_state.message = "🔽 Too low!"
        elif guess > st.session_state.number:
            st.session_state.message = "🔼 Too high!"
        else:
            st.session_state.message = "✅ Correct!"
            st.session_state.score += 10
            st.session_state.streak += 1
            st.balloons()
            st.session_state.number = 0  # Start new round

st.markdown(f"### 📢 {st.session_state.message}")

# Stats
st.markdown("---")
st.subheader("📊 Game Stats")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Score", st.session_state.score)
col2.metric("🔥 Streak", st.session_state.streak)
col3.metric("🎯 Difficulty", st.session_state.difficulty)

# Reset Button
if st.button("🔁 Reset Game"):
    for key in st.session_state.keys():
        st.session_state[key] = 0
    st.session_state.difficulty = difficulty
    st.session_state.message = ""
    st.rerun()
