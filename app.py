import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import plotly.express as px

load_dotenv()

# Enhanced Dark Green Agriculture Theme with better UX
st.set_page_config(
    page_title="Kilimarket AI", 
    page_icon="🌾", 
    layout="wide",
    initial_sidebar_state="expanded"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY is missing. Please add it to your .env file.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# Enhanced CSS for better UI/UX
st.markdown("""
    <style>
    .main, .stApp { 
        background: linear-gradient(135deg, #0a1f0f 0%, #1a2e1a 100%);
        color: #e0f2e0; 
    }
    .stButton>button {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 16px 32px;
        font-size: 1.1rem;
        border: none;
        box-shadow: 0 4px 15px rgba(27, 94, 32, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(27, 94, 32, 0.4);
    }
    .stButton>button:active {
        transform: translateY(0px);
    }
    h1, h2, h3 { 
        color: #81c784; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .stDataFrame { 
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stMetric {
        background: rgba(129, 199, 132, 0.1);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(129, 199, 132, 0.3);
    }
    .sidebar .sidebar-content {
        background: rgba(10, 31, 15, 0.95);
        backdrop-filter: blur(10px);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(129, 199, 132, 0.1);
        border-radius: 10px;
        padding: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #e0f2e0;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: #1b5e20 !important;
        color: white !important;
    }
    .stSuccess, .stInfo, .stWarning {
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stSpinner > div > div {
        border-color: #81c784 transparent transparent transparent;
    }
    </style>
""", unsafe_allow_html=True)

# ===================== DATA LOADING =====================
@st.cache_data(ttl=1800)
def load_market_data():
    try:
        df = pd.read_csv("wfp_food_prices_ken.csv")
        df = df[df['pricetype'].str.contains('Retail', case=False, na=False)]
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        latest = df.groupby(['commodity', 'market']).last().reset_index()
        latest['Commodity'] = latest['commodity'].str.title()
        latest = latest.rename(columns={'price': 'Current_Price_KSh_per_kg', 'market': 'Market'})
        
        useful = ['Maize', 'Beans', 'Potatoes', 'Cabbage', 'Tomatoes', 'Rice', 'Onions', 'Kale', 'Sukuma', 'Carrots']
        latest = latest[latest['Commodity'].str.contains('|'.join(useful), case=False, na=False)]
        
        return latest[['Commodity', 'Market', 'Current_Price_KSh_per_kg']], df
        
    except:
        fallback = {
            "Commodity": ["Maize Grain", "Beans Rosecoco", "Sukuma Wiki", "Irish Potatoes", "Cabbage", "Tomatoes"],
            "Current_Price_KSh_per_kg": [71, 120, 102, 98, 71, 85],
            "Market": ["Nairobi", "Eldoret", "Nakuru", "Kisumu", "Mombasa", "Nairobi"]
        }
        return pd.DataFrame(fallback), pd.DataFrame()

latest_prices, full_history = load_market_data()

# ===================== SIDEBAR FILTERS =====================
with st.sidebar:
    st.markdown("🌾 **Kilimarket AI**")
    st.markdown("---")
    
    markets = ["All Markets"] + sorted(latest_prices['Market'].unique())
    selected_market = st.selectbox("🌍 Select Market", markets, help="Filter prices by market location")
    
    if not latest_prices.empty:
        commodities = sorted(latest_prices['Commodity'].unique())
        selected_commodity = st.selectbox("🌽 Select Commodity", commodities, help="Choose a commodity to analyze")
    
    st.markdown("---")
    st.caption("💡 Tip: Select a commodity to unlock AI insights and predictions!")

display_df = latest_prices if selected_market == "All Markets" else latest_prices[latest_prices['Market'] == selected_market]

# ===================== HEADER =====================
st.title("🌾 Kilimarket AI")
st.markdown("**Real Market Prices & AI-Powered Insights for Kenyan Farmers**")
st.caption("🌱 Empowering farmers with data-driven decisions and predictive analytics")

st.markdown("---")

# ===================== MAIN TABS =====================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Prices", "📈 Price Trends", "🤖 AI Insights", "🔮 Predictions"])

with tab1:
    st.subheader("📊 Current Market Prices")
    
    # Main display
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if 'selected_commodity' in locals() and not display_df.empty:
            # Sort so selected commodity appears first
            sorted_df = display_df.copy()
            sorted_df['is_selected'] = sorted_df['Commodity'] == selected_commodity
            sorted_df = sorted_df.sort_values(by=['is_selected', 'Commodity'], ascending=[False, True])
            
            st.dataframe(
                sorted_df[['Commodity', 'Market', 'Current_Price_KSh_per_kg']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Current_Price_KSh_per_kg": st.column_config.NumberColumn(
                        "Price (KSh/kg)",
                        format="%.0f"
                    )
                }
            )
        else:
            st.dataframe(
                display_df[['Commodity', 'Market', 'Current_Price_KSh_per_kg']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Current_Price_KSh_per_kg": st.column_config.NumberColumn(
                        "Price (KSh/kg)",
                        format="%.0f"
                    )
                }
            )
    
    with col2:
        if 'selected_commodity' in locals() and not display_df.empty:
            row = display_df[display_df['Commodity'] == selected_commodity].iloc[0]
            
            st.metric(
                label=f"**{selected_commodity}**",
                value=f"KSh {row['Current_Price_KSh_per_kg']:.0f} / kg",
                delta=f"Market: {row['Market']}"
            )
            
            # Quick Stats - Always visible when commodity is selected
            st.markdown("### 📈 Quick Stats")
            commodity_data = full_history[full_history['commodity'].str.title() == selected_commodity]
            
            if not commodity_data.empty:
                latest_price = row['Current_Price_KSh_per_kg']
                avg_price = commodity_data['price'].mean()
                max_price = commodity_data['price'].max()
                min_price = commodity_data['price'].min()
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Average Price", f"KSh {avg_price:.0f}")
                    st.metric("Highest Price", f"KSh {max_price:.0f}")
                with col_b:
                    st.metric("Lowest Price", f"KSh {min_price:.0f}")
                    st.metric("Current vs Avg", f"{((latest_price - avg_price) / avg_price * 100):+.1f}%")
            else:
                st.info("No historical data available for stats.")
        else:
            st.info("Select a commodity from the sidebar to see detailed stats.")

    # Download button
    if not display_df.empty:
        st.download_button(
            label="📥 Export Current Prices to CSV",
            data=display_df.to_csv(index=False),
            file_name=f'market_prices_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            key='download-csv'
        )

with tab2:
    st.subheader("📈 Price Trend Analysis")
    
    if 'selected_commodity' in locals():
        commodity_history = full_history[full_history['commodity'].str.title() == selected_commodity]
        
        if not commodity_history.empty and len(commodity_history) > 5:
            # Date range selector
            col1, col2 = st.columns(2)
            with col1:
                days_back = st.slider("Days to analyze", 30, 365, 90, help="Select how many days of historical data to show")
            with col2:
                show_ma = st.checkbox("Show Moving Average", value=True, help="Display 7-day moving average line")
            
            history = commodity_history.sort_values('date').tail(days_back).copy()
            
            # Enhanced chart
            fig = go.Figure()
            
            # Main price line with better styling
            fig.add_trace(go.Scatter(
                x=history['date'],
                y=history['price'],
                mode='lines+markers',
                name='Daily Price',
                line=dict(color='#22c55e', width=3),
                marker=dict(size=6, color='#22c55e', symbol='circle'),
                fill='tonexty',
                fillcolor='rgba(34, 197, 94, 0.1)'
            ))
            
            if show_ma:
                # Moving averages
                history['MA7'] = history['price'].rolling(window=7).mean()
                history['MA30'] = history['price'].rolling(window=30).mean()
                
                fig.add_trace(go.Scatter(
                    x=history['date'],
                    y=history['MA7'],
                    mode='lines',
                    name='7-Day MA',
                    line=dict(color='#eab308', width=2, dash='dash')
                ))
                
                if days_back >= 60:
                    fig.add_trace(go.Scatter(
                        x=history['date'],
                        y=history['MA30'],
                        mode='lines',
                        name='30-Day MA',
                        line=dict(color='#f97316', width=2, dash='dot')
                    ))
            
            # Add trend line
            if len(history) > 10:
                import numpy as np
                x = np.arange(len(history))
                y = history['price'].values
                slope, intercept = np.polyfit(x, y, 1)
                trend_line = intercept + slope * x
                r_squared = 1 - (np.sum((y - trend_line)**2) / np.sum((y - np.mean(y))**2))
                
                fig.add_trace(go.Scatter(
                    x=history['date'],
                    y=trend_line,
                    mode='lines',
                    name=f'Trend (R²={r_squared:.2f})',
                    line=dict(color='#8b5cf6', width=2, dash='longdash')
                ))
            
            fig.update_layout(
                title=f"{selected_commodity} Price Movement (Last {days_back} Days)",
                xaxis_title="Date",
                yaxis_title="Price (KSh per kg)",
                template="plotly_dark",
                height=500,
                plot_bgcolor='rgba(10, 31, 15, 0.8)',
                paper_bgcolor='rgba(10, 31, 15, 0.8)',
                font=dict(color='#e0f2e0'),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                xaxis=dict(gridcolor='#1f3a29'),
                yaxis=dict(gridcolor='#1f3a29'),
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            # Additional insights
            st.markdown("### 📊 Trend Insights")
            latest_price = history['price'].iloc[-1]
            earliest_price = history['price'].iloc[0]
            change = ((latest_price - earliest_price) / earliest_price) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Period Change", f"{change:+.1f}%", 
                         delta=f"{latest_price - earliest_price:+.0f} KSh")
            with col2:
                st.metric("Volatility", f"{history['price'].std():.1f} KSh")
            with col3:
                st.metric("Data Points", len(history))
                
        else:
            st.info("📊 Not enough historical data for trend analysis. Try selecting a different commodity.")
    else:
        st.warning("⚠️ Please select a commodity from the sidebar to view trends.")

with tab3:
    st.subheader("🤖 AI Farmer Advisor")
    
    if 'selected_commodity' in locals() and not display_df.empty:
        row = display_df[display_df['Commodity'] == selected_commodity].iloc[0]
        
        insight_type = st.radio(
            "Choose Insight Type:",
            ["General Advice", "Selling Strategy", "Risk Assessment"],
            horizontal=True
        )
        
        if st.button("🚀 Generate AI Insight", type="primary", use_container_width=True):
            with st.spinner("🤖 Analyzing market data with AI..."):
                try:
                    # Updated model name for 2026
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    
                    prompts = {
                        "General Advice": f"""
                            You are an experienced agricultural advisor in Kenya. Today is {datetime.now().strftime('%d %B %Y')}.
                            Commodity: {selected_commodity}
                            Current Price: KSh {row['Current_Price_KSh_per_kg']} per kg in {row['Market']} market.

                            Provide practical, friendly advice in simple English/Swahili mix (maximum 5 sentences).
                            Cover current market situation, potential risks, and actionable recommendations for a small-scale farmer.
                            """,
                        "Selling Strategy": f"""
                            You are a market strategist for Kenyan agriculture. Today is {datetime.now().strftime('%d %B %Y')}.
                            Commodity: {selected_commodity}
                            Current Price: KSh {row['Current_Price_KSh_per_kg']} per kg in {row['Market']} market.

                            Give strategic selling advice (maximum 5 sentences).
                            Include best time to sell, quantity suggestions, and market considerations.
                            """,
                        "Risk Assessment": f"""
                            You are a risk analyst for Kenyan agricultural markets. Today is {datetime.now().strftime('%d %B %Y')}.
                            Commodity: {selected_commodity}
                            Current Price: KSh {row['Current_Price_KSh_per_kg']} per kg in {row['Market']} market.

                            Assess risks and provide mitigation strategies (maximum 5 sentences).
                            Cover price volatility, supply issues, and protective measures.
                            """
                    }
                    
                    response = model.generate_content(prompts[insight_type])
                    insight = response.text.strip()
                    
                    st.success(f"✅ {insight_type}")
                    st.write(insight)
                    
                except Exception as e:
                    error_msg = str(e).lower()
                    if "429" in error_msg or "quota" in error_msg:
                        st.warning("⏳ Free tier quota limit reached. Please wait 30-60 seconds and try again.")
                    elif "404" in error_msg or "not found" in error_msg:
                        st.error("❌ Model not available. Trying a different model...")
                        # Fallback model
                        try:
                            model = genai.GenerativeModel('gemini-2.0-flash-exp')
                            response = model.generate_content(prompts[insight_type])
                            insight = response.text.strip()
                            st.success(f"✅ {insight_type}")
                            st.write(insight)
                        except:
                            st.error("AI service is currently unavailable. Please try again later.")
                    else:
                        st.error(f"❌ AI Error: {str(e)}")
    else:
        st.warning("⚠️ Please select a commodity from the sidebar to get AI insights.")

with tab4:
    st.subheader("🔮 AI Price Prediction")
    
    if 'selected_commodity' in locals() and not display_df.empty:
        row = display_df[display_df['Commodity'] == selected_commodity].iloc[0]
        
        # Prediction options
        prediction_period = st.selectbox(
            "Prediction Timeframe:",
            ["Next 7 Days", "Next 30 Days", "Next 90 Days"],
            help="Choose how far ahead you want the AI to predict"
        )
        
        confidence_level = st.slider(
            "Confidence Level",
            60, 95, 75,
            help="How confident should the AI be in its prediction?"
        )
        
        if st.button("🔍 Generate Price Prediction", type="primary", use_container_width=True):
            with st.spinner("🔮 Analyzing historical patterns and generating prediction..."):
                try:
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    
                    # Get historical data for better context
                    commodity_history = full_history[full_history['commodity'].str.title() == selected_commodity]
                    
                    if not commodity_history.empty and len(commodity_history) >= 15:
                        history = commodity_history.sort_values('date').tail(60)  # Last 60 data points
                        recent_prices = history['price'].tolist()[-20:]  # Last 20 prices for prompt
                        recent_dates = history['date'].dt.strftime('%Y-%m-%d').tolist()[-20:]
                        
                        prompt = f"""
                        You are an expert agricultural economist and market analyst for Kenyan commodities.

                        Commodity: {selected_commodity}
                        Current Price: KSh {row['Current_Price_KSh_per_kg']} per kg in {row['Market']} market.
                        Today: {datetime.now().strftime('%d %B %Y')}

                        Recent price history (last 20 data points):
                        Dates: {recent_dates}
                        Prices (KSh/kg): {recent_prices}

                        Predict the likely price range for {prediction_period.lower()} from now.
                        Provide the following in a clear, farmer-friendly format:
                        1. Predicted price range (low - high) in KSh per kg
                        2. Expected direction (Up, Down, or Stable)
                        3. Key factors that may influence the price
                        4. Risk level (Low/Medium/High)
                        5. Practical recommendation for a small-scale farmer

                        Be realistic and data-driven. Use a confidence level of approximately {confidence_level}%.
                        """

                        response = model.generate_content(prompt)
                        prediction_text = response.text.strip()

                        st.success(f"🔮 {prediction_period} Price Prediction")
                        st.write(prediction_text)

                        # Visual confidence indicator
                        st.markdown("### 📊 Prediction Confidence")
                        st.progress(confidence_level / 100, text=f"Confidence: {confidence_level}%")

                    else:
                        st.info("📊 Not enough historical data for accurate prediction. Try selecting a different commodity or shorter timeframe.")

                except Exception as e:
                    error_msg = str(e).lower()
                    if "429" in error_msg or "quota" in error_msg:
                        st.warning("⏳ Free tier quota reached. Please wait 30-60 seconds and try again.")
                    else:
                        st.error(f"❌ Prediction Error: {str(e)}")
                    st.info("💡 AI predictions work best with sufficient historical data.")
    else:
        st.warning("⚠️ Please select a commodity from the sidebar to generate predictions.")

# Footer
st.markdown("---")
st.caption("🏗️ Built in Nairobi, Kenya | Portfolio Project | Last updated: " + datetime.now().strftime("%d %b %Y"))