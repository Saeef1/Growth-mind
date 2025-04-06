import streamlit as st
import pandas as pd
import csv
import os
import datetime

MOOD_FILE = "mood.csv"

def load_moods():
    if not os.path.exists(MOOD_FILE):
        return pd.DataFrame(columns=["Date", "Mood"])
    return pd.read_csv(MOOD_FILE)

def save_mood_data(date,mood):
    with open(MOOD_FILE,"a") as file:
        writer = csv.writer(file)
        writer.writerow([date,mood])

st.title("Mood tracker")

today = datetime.date.today()

st.subheader("How are you feeling today?")

mood = st.selectbox("Select your mood",["Happy","Sad","Angry","Stressed","Anxious","Neutral"])

if st.button("Save"):
    save_mood_data(today,mood)
    st.success("Mood saved successfully!")

data = load_moods()

if not data.empty:
    st.subheader("Mood History")

    data["Date"] = pd.to_datetime(data["Date"])

    mood_chart = data.groupby("Mood").count()["Date"]

    st.bar_chart(mood_chart)


    
    
