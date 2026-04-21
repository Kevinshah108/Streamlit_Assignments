import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta

st.title("🌍Travel & Investment Planner")

st.write("Welcome to the **Smart Planning Portal**. Plan your *travel and investments* efficiently.")

if "visited" not in st.session_state:
    st.success("Welcome to the portal!")
    st.session_state.visited = True

st.sidebar.header("User Preferences")

user_level = st.sidebar.radio("Select User Level:", ["Beginner", "Intermediate", "Advanced"])

continent = st.sidebar.selectbox(
    "Target Continent:",
    ["Africa", "Asia", "Europe", "North America", "South America", "Australia"]
)

interests = st.sidebar.multiselect(
    "Select Interests:",
    ["Tech", "Finance", "Travel", "Food"]
)

budget = st.sidebar.slider("Investment Budget", 0, 10000, 1000)

if not interests:
    st.sidebar.warning("Please select at least one interest.")


col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Project Start Date", value=date.today())

with col2:
    st.write("Selected Budget:", budget)

np.random.seed(42)

dates = pd.date_range(start=start_date, periods=20)

data = pd.DataFrame({
    "Date": dates,
    "Category": np.random.choice(["Tech", "Finance", "Travel", "Food"], 20),
    "Continent": np.random.choice(["Africa", "Asia", "Europe", "North America", "South America", "Australia"], 20),
    "Amount": np.random.randint(100, 1000, 20),
    "Status": np.random.choice(["Planned", "Completed"], 20),
    "Growth": np.random.uniform(1.0, 5.0, 20).round(2)
})


filtered_data = data[data["Continent"] == continent]

st.subheader("Filtered Financial Data")
st.dataframe(filtered_data)

name = st.text_input("Enter your name:")

if st.button("Process Report"):
    if name:
        if not interests:
            st.error('Please select your interests')
        else:
            if budget > 0:
                daily_budget = budget / 30
                st.write(f"User `{name}` wants to travel to `{continent}` starting `{start_date}`.")
                st.write(f"Daily Budget: {daily_budget:.2f}")
                st.balloons()
            else:
                st.warning("Budget must be greater than 0 to process report.")

    else:
        st.error("Name is compulsory!")

if budget == 0:
    st.info("Your budget is 0. Please increase it to proceed.")


