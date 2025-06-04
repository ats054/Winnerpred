import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="מערכת תחזיות ווינר", layout="centered")
st.title("🎯 מערכת חיזוי חכמה לווינר")
st.write("תחזיות חכמות מבוססות סטטיסטיקה ורווח צפוי (בהתאם לסכום הימור שתבחר).")

# סכום הימור לבחירת המשתמש
investment = st.number_input("בחר סכום הימור (₪)", min_value=10, max_value=1000, value=30, step=10)

# נתוני משחקים לדוגמה (נכניס API בשלב הבא)
games_data = [
    {"קבוצות": "מכבי ת״א - הפועל חיפה", "יחס": 2.1, "שערים ממוצע": 2.7, "סוג": "ניצחון מכבי"},
    {"קבוצות": "ריאל מדריד - אתלטיקו", "יחס": 1.8, "שערים ממוצע": 3.1, "סוג": "מעל 2.5 שערים"},
    {"קבוצות": "יובנטוס - נאפולי", "יחס": 2.6, "שערים ממוצע": 1.9, "סוג": "ניצחון נאפולי"},
    {"קבוצות": "הפועל ב״ש - בית״ר", "יחס": 2.0, "שערים ממוצע": 2.3, "סוג": "מתחת 2.5 שערים"},
    {"קבוצות": "ברצלונה - סביליה", "יחס": 1.9, "שערים ממוצע": 2.9, "סוג": "ניצחון ברצלונה"},
]

def analyze_game(game):
    # חישוב הסתברות לפי שערים ממוצעים (פשטני לשלב ראשון)
    prob = round(min(max(game["שערים ממוצע"] / 4, 0.4), 0.85), 2)
    confidence = int(prob * 100)
    expected_profit = round((game["יחס"] * investment * prob) - investment, 2)
    recommendation = "✅ כדאי להמר" if expected_profit > 5 else "❌ לא משתלם"
    icon = "🟢" if expected_profit > 5 else "🔴"
    return {
        "משחק": game["קבוצות"],
        "סוג הימור": game["סוג"],
        "יחס": game["יחס"],
        "שערים ממוצע": game["שערים ממוצע"],
        "הסתברות הצלחה": f"{confidence}%",
        "רווח צפוי": f"{expected_profit} ₪",
        "המלצה": f"{icon} {recommendation}"
    }

# עיבוד כל המשחקים
results = [analyze_game(game) for game in games_data]
df = pd.DataFrame(results)

# תצוגה
st.subheader("📊 התחזיות להיום:")
st.dataframe(df, use_container_width=True)
