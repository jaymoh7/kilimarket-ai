import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai

st.set_page_config(page_title="Kilimarket AI", page_icon="🌽", layout="wide")

# ===================== CONFIG =====================
GEMINI_API_KEY = "AIzaSyAa7TIa-A4DFEEyp0h-UFqHL_HnkYp4Ke4"   # ← Keep your key here

genai.configure(api_key=GEMINI_API_KEY)

# Expanded & realistic Kenyan market data (March 2026)
data = {
    "Commodity": [
        "Maize Grain (Loose)", "Beans (Rosecoco)", "Sukuma Wiki (Kale)", 
        "Irish Potatoes", "Cabbage", "Tomatoes", "Rice (Pishori)", 
        "Onions (Red)", "Carrots", "Capsicum (Green)"
    ],
    "Current_Price_KSh_per_kg": [71, 120, 102, 98, 71, 85, 145, 110, 95, 130],
    "Last_Week_Price": [69, 115, 98, 95, 65, 80, 142, 105, 92, 125],
    "Market": ["Nairobi", "Eldoret", "Nakuru", "Kisumu", "Mombasa", "Nairobi", "Eldoret", "Nakuru", "Kisumu", "Mombasa"],
    "Trend": ["Slight Increase", "Increasing", "Increasing", "Stable", "Increasing", "Increasing", "Stable", "Increasing", "Stable", "Increasing"]
}

df = pd.DataFrame(data)

# ===================== HEADER =====================
st.title("🌽 Kilimarket AI")
st.markdown("**Helping Kenyan Farmers Get Fair Market Prices & Smart Advice**")

st.markdown("---")

# ===================== MAIN LAYOUT =====================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Today's Market Prices")
    st.dataframe(df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("🌾 Select Commodity")
    commodity = st.selectbox("Choose a crop", df["Commodity"])
    
    selected_row = df[df["Commodity"] == commodity].iloc[0]
    
    st.metric(
        label=f"**{commodity}**",
        value=f"KSh {selected_row['Current_Price_KSh_per_kg']} / kg",
        delta=f"{selected_row['Current_Price_KSh_per_kg'] - selected_row['Last_Week_Price']} KSh from last week"
    )

    st.info("💡 Tip: Use current prices to negotiate with buyers or decide when to sell.")

# Price Trend Chart
st.subheader("📈 Price Trend (Last Week vs This Week)")
chart_data = pd.DataFrame({
    "Period": ["Last Week", "This Week"],
    "Price (KSh/kg)": [selected_row['Last_Week_Price'], selected_row['Current_Price_KSh_per_kg']]
})
st.bar_chart(chart_data.set_index("Period"))

# ===================== AI INSIGHT =====================
st.subheader("🤖 AI Market Insight for Farmers")

if st.button("Get AI Advice", type="primary", use_container_width=True):
    with st.spinner("Gemini anafikiria ushauri bora kwa mkulima..."):
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            Wewe ni mtaalamu wa masoko ya kilimo nchini Kenya. 
            Tarehe ya leo ni {datetime.now().strftime('%d %B %Y')}.

            Bei ya sasa ya:
            Bidhaa: {selected_row['Commodity']}
            Bei ya leo: KSh {selected_row['Current_Price_KSh_per_kg']} kwa kilo
            Bei wiki iliyopita: KSh {selected_row['Last_Week_Price']} kwa kilo
            Soko: {selected_row['Market']}

            Andika ushauri mfupi, wa vitendo na wa kirafiki (maximum 5-6 sentences).
            Tumia Kiswahili rahisi au English iliyochanganywa kama inavyofaa.
            Eleza wazi:
            - Ni wakati mzuri wa kuuza au kushika bidhaa?
            - Kuna hatari au fursa gani?
            - Ushauri wa moja kwa moja ambao mkulima mdogo anaweza kufuata leo.

            Sauti yako iwe kama unazungumza moja kwa moja na mkulima mdogo wa Kenya.
            """

            response = model.generate_content(prompt)
            insight = response.text.strip()

            st.success("✅ Ushauri wa AI umetolewa")
            st.write(insight)

        except Exception as e:
            st.error(f"Hitilafu kidogo: {str(e)}")
            st.info("Jaribu tena baada ya sekunde 10-20.")
else:
    st.write("Bonyeza kitufe hapo juu kupata ushauri maalum wa AI.")

# ===================== FARMER TIPS SECTION =====================
st.subheader("💡 General Farmer Tips")
st.write("""
- Bei huwa na mabadiliko makubwa msimu wa mvua na ukame. Fuatilia bei kila wiki.
- Ikiwa una hifadhi salama, unaweza kushika mazao kidogo ili uuze wakati bei iko juu.
- Usiuzwe kwa haraka kwa middlemen bila kujua bei ya soko.
- Tumia Kilimarket AI kila wiki kabla ya kupeleka mazao sokoni.
""")

# ===================== FOOTER =====================
st.markdown("---")
st.caption(f"Built on {datetime.now().strftime('%d %B %Y')} | By a Broke CS Graduate in Nairobi")
st.caption("This is a portfolio project built in 5 days using free tools on Pop OS to help Kenyan farmers.")
st.caption("Live Demo: Helping small-scale farmers avoid exploitation by middlemen.")
