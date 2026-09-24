import streamlit as st

st.title("🏀 GameIQ")
st.subheader("NBA Analytics Dashboard")

st.write("Welcome to GameIQ!")
st.write("Explore NBA players, statistics and performance.")

player = st.selectbox(
    "Choose a player:",
    ["LeBron James", "Stephen Curry", "Nikola Jokic"]
)

st.write("You selected:", player)

if player == "LeBron James":
    st.write("Position: Forward")
    st.write("Team: Philadelphia 76ers")

elif player == "Stephen Curry":
    st.write("Position: Guard")
    st.write("Team: Golden State Warriors")

elif player == "Nikola Jokic":
    st.write("Position: Center")
    st.write("Team: Denver Nuggets")