import streamlit as st
from groq import Groq

# -----------------------------
# 🔑 SET API KEY
# -----------------------------
import os
client = Groq(api_key=st.secrets["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"])

# -----------------------------
# 🌍 UI
# -----------------------------
st.title("🌍 AI Carbon Footprint Assistant (Groq)")

st.write("Answer questions to estimate your carbon footprint.")

# -----------------------------
# 📋 INPUT
# -----------------------------
transport = st.selectbox(
    "🚗 Transport",
    ["Car (alone)", "Carpool", "Public Transport", "Bike/Walk"]
)

diet = st.selectbox(
    "🍽️ Diet",
    ["Daily", "Few times/week", "Rarely", "Vegetarian/Vegan"]
)

flights = st.selectbox(
    "✈️ Flights per year",
    ["0", "1-2", "3-5", "5+"]
)

shopping = st.selectbox(
    "🛍️ Shopping",
    ["Frequent", "Moderate", "Rare"]
)

energy = st.selectbox(
    "💡 Energy usage",
    ["High", "Medium", "Low"]
)

# -----------------------------
# 🧮 SCORE
# -----------------------------
def calculate_score():
    score = 0

    if transport == "Car (alone)": score += 10
    elif transport == "Carpool": score += 7
    elif transport == "Public Transport": score += 5
    else: score += 2

    if diet == "Daily": score += 10
    elif diet == "Few times/week": score += 7
    elif diet == "Rarely": score += 4
    else: score += 2

    if flights == "5+": score += 15
    elif flights == "3-5": score += 10
    elif flights == "1-2": score += 5

    if shopping == "Frequent": score += 10
    elif shopping == "Moderate": score += 5
    else: score += 2

    if energy == "High": score += 10
    elif energy == "Medium": score += 5
    else: score += 2

    return score

def get_level(score):
    if score <= 20:
        return "Low"
    elif score <= 40:
        return "Medium"
    else:
        return "High"

# -----------------------------
# 🤖 GROQ AI FUNCTION
# -----------------------------
def get_ai_response():
    score = calculate_score()
    level = get_level(score)

    prompt = f"""
    User lifestyle:
    Transport: {transport}
    Diet: {diet}
    Flights: {flights}
    Shopping: {shopping}
    Energy: {energy}
    Score: {score} ({level})

    Tasks:
    - Estimate carbon footprint (rough)
    - Identify biggest emission source
    - Give 5 practical ways to reduce it
    - Suggest one high-impact action

    Keep it simple.
    """

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}]
)

    return response.choices[0].message.content

# -----------------------------
# 🚀 BUTTON
# -----------------------------
if st.button("Calculate & Get AI Advice"):

    score = calculate_score()
    level = get_level(score)

    st.subheader("📊 Results")
    st.write(f"Score: {score}")
    st.write(f"Impact Level: {level}")

    st.subheader("🤖 AI Suggestions")

    with st.spinner("Analyzing..."):
        result = get_ai_response()

    st.write(result)
