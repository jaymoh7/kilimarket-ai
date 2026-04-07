# 🌽 Kilimarket AI

**AI-Powered Market Price Predictor & Advisor for Kenyan Farmers**

Built in **5 days** while completely broke in Nairobi, using only free tools on Pop OS.

### Problem It Solves
Small-scale farmers in Kenya often get exploited by middlemen because they don't know current market prices. This app gives them:
- Real-time market prices for major commodities
- AI-generated practical advice (in simple English/Swahili)
- Price trend visualization

### Features
- Clean, mobile-friendly interface
- Live price data for 10+ commodities
- Interactive AI insights powered by Gemini
- Price trend bar charts
- Farmer-friendly tips

### Tech Stack
- Python + Streamlit
- Pandas for data handling
- Google Gemini (for AI insights)
- Deployed on Render

### Live Demo
[→ Open Kilimarket AI](https://kilimarket-ai.onrender.com)  

### Screenshots
(Add 2-3 screenshots here later)

### My Story
I’m a Computer Science graduate from Nairobi who felt like university was a waste of time and I had no real skills.  
In just 5 days, using free tools and consistent daily work, I built and deployed this useful AI tool.

This project proves that with discipline and the right approach, you can create real value even when starting from zero.

### How to Run Locally
```bash
git clone https://github.com/jaymoh7/kilimarket-ai.git
cd kilimarket-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py