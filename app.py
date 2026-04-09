import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Kilimarket AI", page_icon="🌽", layout="wide")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY is missing. Please check your .env file.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# ===================== LOAD REAL DATA =====================
@st.cache_data(ttl=3600)
def load_market_data():
    try:
        df = pd.read_csv("wfp_food_prices_ken.csv")
        df = df[df['pricetype'].str.contains('Retail', case=False, na=False)]
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        
        latest = df.groupby(['commodity', 'market']).first().reset_index()
        
        latest['Commodity'] = latest['commodity'].str.title()
        latest = latest.rename(columns={
            'price': 'Current_Price_KSh_per_kg',
            'market': 'Market'
        })
        
        useful = ['Maize', 'Beans', 'Potatoes', 'Cabbage', 'Tomatoes', 'Rice', 
                 'Onions', 'Kale', 'Sukuma', 'Carrots', 'Capsicum']
        latest = latest[latest['Commodity'].str.contains('|'.join(useful), case=False, na=False)]
        
        return latest[['Commodity', 'Market', 'Current_Price_KSh_per_kg']], df
        
    except:
        st.warning("Using simulated data")
        fallback = {
            "Commodity": ["Maize Grain", "Beans Rosecoco", "Sukuma Wiki", "Irish Potatoes", "Cabbage", "Tomatoes"],
            "Current_Price_KSh_per_kg": [71, 120, 102, 98, 71, 85],
            "Market": ["Nairobi", "Eldoret", "Nakuru", "Kisumu", "Mombasa", "Nairobi"]
        }
        return pd.DataFrame(fallback), pd.DataFrame()

latest_prices, full_history = load_market_data()

# ===================== CUSTOM STYLING =====================
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { background-color: #00cc66; color: white; font-weight: bold; }
    .metric-label { font-size: 1.1rem; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.title("🌽 Kilimarket AI")
st.markdown("**Real-time Market Prices & AI-Powered Advice for Kenyan Farmers**")
st.caption("Helping small-scale farmers avoid middlemen exploitation")

st.markdown("---")

# ===================== FILTERS =====================
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    markets = ["All Markets"] + sorted(latest_prices['Market'].unique())
    selected_market = st.selectbox("🌍 Filter by Market", markets)

with col2:
    if not latest_prices.empty:
        commodities = sorted(latest_prices['Commodity'].unique())
        selected_commodity = st.selectbox("🌾 Select Commodity", commodities)

# Filter data
display_df = latest_prices if selected_market == "All Markets" else latest_prices[latest_prices['Market'] == selected_market]

# ===================== MAIN CONTENT =====================
col_left, col_right = st.columns([2.2, 1])

with col_left:
    st.subheader("📊 Current Market Prices")
    st.dataframe(display_df[['Commodity', 'Market', 'Current_Price_KSh_per_kg']], 
                 use_container_width=True, hide_index=True)

with col_right:
    if 'selected_commodity' in locals() and not display_df.empty:
        row = display_df[display_df['Commodity'] == selected_commodity].iloc[0]
        
        st.metric(
            label=f"**{selected_commodity}**",
            value=f"KSh {row['Current_Price_KSh_per_kg']:.0f} / kg",
            delta=None
        )
        st.caption(f"📍 Market: {row['Market']}")

        # Price Trend
        st.subheader("📈 90-Day Price Trend")
        commodity_history = full_history[full_history['commodity'].str.title() == selected_commodity]
        if not commodity_history.empty:
            recent = commodity_history.sort_values('date').tail(90)
            st.line_chart(recent.set_index('date')['price'], use_container_width=True)

# ===================== AI SECTION =====================
st.subheader("🤖 AI Market Insight")

if st.button("Get Personalized Farmer Advice", type="primary", use_container_width=True):
    with st.spinner("Analyzing market trends for you..."):
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            You are a friendly Kenyan agricultural expert speaking to a small-scale farmer.

            Today: {datetime.now().strftime('%d %B %Y')}
            Commodity: {selected_commodity}
            Current Price: KSh {row['Current_Price_KSh_per_kg']} per kg
            Market: {row['Market']}

            Give warm, practical advice in simple Swahili or English (maximum 5-6 sentences).
            Include:
            - Is this a good time to sell or hold?
            - Any risks or opportunities
            - Clear action the farmer can take this week
            """

            response = model.generate_content(prompt)
            insight = response.text.strip()

            st.success("✅ Here is your advice:")
            st.write(insight)

        except Exception as e:
            st.error(f"AI Error: {str(e)}")

# ===================== FOOTER =====================
st.markdown("---")
st.caption(f"Data Source: World Food Programme (WFP) • Last checked: {datetime.now().strftime('%d %B %Y')}")
st.caption("Built with determination in Nairobi, Kenya | CS Graduate Portfolio Project")