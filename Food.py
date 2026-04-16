import streamlit as st
import datetime

with st.form("Food Application Form"):
    st.title("Food Application", text_alignment="center")

    d1, d2 = st.columns(2)

    FirstName = d1.text_input(label="First Name", placeholder="Enter your first name")

    LastName = d2.text_input(label="Last Name", placeholder="Enter your last name")

    City = st.selectbox(label="City", placeholder="Select your city", options=["Vadodara", "Surat", "Ahemdabad", "Rajkot", "Godhra"])

    Food_Pref = st.multiselect(label="Food Categories", options=["Gujarati", "Mexican", "North Indian", "Chinese", "Italian", "South Indian"])

    Order_freq = st.slider("How many times have you ordered the food?", min_value=0, max_value=10, value=0, step=1)

    Gender = st.radio(label="Gender", options=["Male", "Female"], horizontal=True)

    DOB = st.date_input("Date Of Birth", datetime.date.today())

    b1, b2 = st.columns(2)

    Food = b1.multiselect(label="Food Items", options=["Khichdi", "Pizza", "Burger", "Paneer Tikka Masala", "Chow-mein", "Tacos", "Dosa"])

    Beverages = b2.multiselect(label="Beverages Items", options=["Water","Coca-cola", "Fanta", "Sprite", "Soda", "lemon juice"])

    Audio_message = st.audio_input("Record your message")
    
    Feedback = st.text_area("Share your review", height=100, placeholder="Start writing here...")

    Agreement = st.checkbox("I agree")

    Submit = st.form_submit_button("Submit", use_container_width=True)


if (Submit):
    if (Agreement == False):
        st.error("You must agree to the terms and conditions")
    else:
        st.toast("🎉You have registered successfully!")
        st.balloons()
        st.header("Order Details Summary")
        st.write(f"First Name: {FirstName}")
        st.write(f"Last Name: {LastName}")
        st.write(f"City: {City}")
        st.write(f"Food Category: {Food_Pref}")
        st.write(f"Order Frequency: {Order_freq}")
        st.write(f"Food Items: {Food}")
        st.write(f"Beverages Items: {Beverages}")
        if Audio_message:
                st.write("Message recorded successfully")
                st.audio(Audio_message)
        if (Feedback):
             st.write("Thank you for your valuable feedback!")
             st.write("Your Feedback:", Feedback)

        st.success("Your order has been placed successfully!")


    