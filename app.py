import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

st.set_page_config(page_title="תחזיות ווינר - משחקים אמיתיים", layout="centered")
st.title("⚽ תחזיות ווינר עם משחקים אמיתיים (SofaScore)")
st.write("שליפת משחקים ל-3 ימים קדימה מ-SofaScore וניתוח הסתברות")

investment = st.number_input("בחר סכום הימור (₪)", min_value=10, max_value=1000, value=30, step=10)

# פונקציית סקרייפינג בסיסית – נדרש לשפר בהתאם למבנה האתר בפועל
def get_matches():
    matches = []
    today = datetime.today()
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for i in range(3):  # היום + 2 קדימה
        date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
        url = f"https://www.sofascore.com/football//{date}"  # לינק כללי – דורש התאמה
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # כאן תכניס שליפה אמיתית לפי תגיות של הקבוצות, שעה, ממוצע שערים וכו'
            matches.append({
                "league": "לדוגמה",
                "teams": "קבוצה א - קבוצה ב",
                "avg_goals": 2.6,
                "odds": 2.1,
                "bet_type": "ניצחון קבוצה א"
            })
        else:
            st.error(f"שגיאה בטעינה ליום {date} - קוד {response.status_code}")
    return matches

# חישוב הסתברות ורווח צפוי
def calculate_value(game):
    prob = round(min(max(game["avg_goals"] / 4, 0.4), 0.85), 2)
    confidence = int(prob * 100)
    expected_profit = round((game["odds"] * investment * prob) - investment, 2)
    recommendation = "✅ כדאי להמר" if expected_profit > 5 else "❌ לא משתלם"
    icon = "🟢" if expected_profit > 5 else "🔴"
    return {
        "ליגה": game["league"],
        "משחק": game["teams"],
        "סוג הימור": game["bet_type"],
        "יחס": game["odds"],
        "שערים ממוצע": game["avg_goals"],
        "הסתברות הצלחה": f"{confidence}%",
        "רווח צפוי": f"{expected_profit} ₪",
        "המלצה": f"{icon} {recommendation}"
    }

games = get_matches()
results = [calculate_value(game) for game in games]
df = pd.DataFrame(results)
st.subheader("📊 תחזיות משחקים:")
st.dataframe(df, use_container_width=True)
