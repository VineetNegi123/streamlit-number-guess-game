import streamlit as st
import random

# Initialize session state for the number and attempts
if "number" not in st.session_state:
    st.session_state.number = random.randint(1, 100)
    st.session_state.attempts = 0

st.title("🎯 Guess the Number!")
st.write("I'm thinking of a number between 1 and 100. Can you guess it?")

# User input
guess = st.number_input("Enter your guess", min_value=1, max_value=100, step=1)

if st.button("Submit Guess"):
    st.session_state.attempts += 1
    if guess < st.session_state.number:
        st.warning("Too low! Try a higher number.")
    elif guess > st.session_state.number:
        st.warning("Too high! Try a lower number.")
    else:
        st.success(f"🎉 Correct! The number was {st.session_state.number}.")
        st.balloons()
        st.info(f"You took {st.session_state.attempts} attempts.")
        if st.button("Play Again"):
            st.session_state.number = random.randint(1, 100)
            st.session_state.attempts = 0
