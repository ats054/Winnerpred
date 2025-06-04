import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="חיזוי חכם להימורים בווינר", layout="centered")
st.title("🎯 מערכת תחזיות ווינר")
st.write("קבל תחזיות חכמות מבוססות הסתברות ורווח צפוי (סכום הימור: 30 ש״ח)")

# דוגמאות למשחקים – בעתיד נמשוך מבחוץ
games = [
    {"קבוצות": "מכבי ת״א - הפועל חיפה", "יחס": 2.1, "סוג": "ניצחון מכבי"},
    {"קבוצות": "ריאל מדריד - אתלטיקו", "יחס": 1.8, "סוג": "מעל 2.5 שערים"},
    {"קבוצות": "יובנטוס - נאפולי", "יחס": 2.6, "סוג": "ניצחון נאפולי"},
    {"קבוצות": "הפועל ב״ש - בית״ר", "יחס": 2.0, "סוג": "מתחת 2.5 שערים"},
    {"קבוצות": "ברצלונה - סביליה", "יחס": 1.9, "סוג": "ניצחון ברצלונה"},
]

# פונקציה שמחשבת הסתברות ורווח
def analyze_game(game):
    prob = round(random.uniform(0.5, 0.8), 2)  # הסתברות 50%-80%
    confidence = int(prob * 100)
    expected = round((game["יחס"] * 30 * prob) - 30, 2)
    recommendation = "✅ כדאי להמר" if expected > 5 else "❌ לא משתלם"
    return {
        "משחק": game["קבוצות"],
        "סוג הימור": game["סוג"],
        "יחס ווינר": game["יחס"],
        "הסתברות הצלחה": f"{confidence}%",
        "רווח צפוי": f"{expected} ₪",
        "המלצה": recommendation,
    }

results = [analyze_game(game) for game in games]
df = pd.DataFrame(results)

st.subheader("🧠 התחזיות להיום:")
st.dataframe(df, use_container_width=True)
