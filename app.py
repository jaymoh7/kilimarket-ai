import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai

st.set_page_config(page_title="Kilimarket AI", page_icon="🌽", layout="wide")

# ===================== CONFIG =====================
GEMINI_API_KEY = "AIzaSyAa7TIa-A4DFEEyp0h-UFqHL_HnkYp4Ke4"   # Make sure your key is still here

genai.configure(api_key=GEMINI_API_KEY)

# Expanded realistic data (March 2026)
data = {
    "Commodity": ["Maize Grain (Loose)", "Beans (Rosecoco)", "Sukuma Wiki", 
                  "Irish Potatoes", "Cabbage", "Tomatoes", "Rice", "Onions"],
    "Current_Price_KSh_per_kg": [71, 120, 102, 98, 71, 85, 145, 110],
    "Last_Week_Price": [69, 115, 98, 95, 65, 80, 142, 105],
    "Market": ["Nairobi", "Eldoret", "Nakuru", "Kisumu", "Mombasa", "Nairobi", "Eldoret", "Nakuru"],
    "Trend": ["Slight Increase", "Increasing", "Increasing", "Stable", "Increasing", "Increasing", "Stable", "Increasing"]
}

df = pd.DataFrame(data)

# ===================== HEADER =====================
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🌽 Kilimarket AI")
    st.markdown("**Market Prices + AI Insights for Kenyan Farmers**")
with col2:
    st.image("https://img.icons8.com/color/96/000000/kenya.png", width=80)  # Optional flag

st.markdown("---")

# ===================== MAIN CONTENT =====================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Today's Market Prices")
    st.dataframe(df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("Select Commodity")
    commodity = st.selectbox("Choose a crop", df["Commodity"])
    
    selected_row = df[df["Commodity"] == commodity].iloc[0]
    
    st.metric(
        label=f"**{commodity}**",
        value=f"KSh {selected_row['Current_Price_KSh_per_kg']} / kg",
        delta=f"{selected_row['Current_Price_KSh_per_kg'] - selected_row['Last_Week_Price']} from last week"
    )
    
    st.info("💡 Use this to negotiate better with buyers or decide when to sell.")

# ===================== CHART =====================
st.subheader("Price Trend")
chart_data = pd.DataFrame({
    "Week": ["Last Week", "This Week"],
    "Price": [selected_row['Last_Week_Price'], selected_row['Current_Price_KSh_per_kg']]
})
st.bar_chart(chart_data.set_index("Week"))

# ===================== AI INSIGHT =====================
st.subheader("🤖 AI Market Insight")

if st.button("Generate AI Insight", type="primary", use_container_width=True):
    with st.spinner("Gemini anafikiria kwa mkulima..."):
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            Wewe ni mtaalamu wa soko la kilimo nchini Kenya. 
            Sasa ni {datetime.now().strftime('%d %B %Y')}.

            Bei ya sasa:
            Bidhaa: {selected_row['Commodity']}
            Bei ya leo: KSh {selected_row['Current_Price_KSh_per_kg']} kwa kilo
            Bei wiki iliyopita: KSh {selected_row['Last_Week_Price']} kwa kilo
            Soko: {selected_row['Market']}

            Andika ushauri mfupi, wa vitendo na wa kirafiki kwa mkulima mdogo (max 5 sentences).
            Tumia Kiswahili au English rahisi.
            Eleza:
            - Ni wakati mzuri wa kuuza au kushika?
            - Hatari au fursa gani?
            - Ushauri wa moja kwa moja.
            """

            response = model.generate_content(prompt)
            insight = response.text.strip()

            st.success("✅ Ushauri wa AI umetolewa")
            st.write(insight)

        except Exception as e:
            st.error(f"Hitilafu: {str(e)}")
            st.info("Jaribu tena baada ya sekunde chache.")
else:
    st.write("Bonyeza kitufe ili kupata ushauri wa AI.")

# ===================== FOOTER =====================
st.markdown("---")
st.caption(f"Built on {datetime.now().strftime('%d %B %Y')} | Broke CS Graduate in Nairobi | Using free AI tools on Pop OS")
st.caption("This is a portfolio project to help Kenyan farmers get better market information.")