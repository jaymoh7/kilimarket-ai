# 🌽 Kilimarket AI

**Real-time Market Prices + AI Advice for Kenyan Farmers**

Built in **9 days** while completely broke in Nairobi using only free tools.

### 🎯 The Problem It Solves
Small-scale farmers in Kenya are often exploited by middlemen because they don’t know current market prices. They end up selling cheap and losing money.

**Kilimarket AI** helps them:
- See real market prices (from World Food Programme data)
- Get practical AI-generated advice in simple English or Swahili
- View price trends over time
- Make better decisions on when to sell or hold

### 🚀 Live Demo
[👉 Open Kilimarket AI](https://kilimarket-ai.onrender.com)  
*(Replace with your actual Render URL)*

### ✨ Features
- Real WFP retail price data
- Market filter (Nairobi, Eldoret, Nakuru, etc.)
- Interactive 90-day price trend charts
- Smart AI insights powered by Gemini
- Clean, mobile-friendly design
- Safe API key handling using `.env`

### 🛠️ Tech Stack
- **Python** + **Streamlit**
- **Pandas** for data processing
- **Google Gemini** for AI advice
- **python-dotenv** for secure API key management
- Deployed on **Render** (free tier)

### 📸 Screenshots

![Kilimarket AI Dashboard](screenshots/main-dashboard.png)
![AI Market Insight](screenshots/ai-insight.png)
![Price Trend Chart](screenshots/price-trend.png)

*Click on images to enlarge*

### 💪 My Story
I’m a Computer Science graduate from Nairobi who felt completely lost after university.  
I was tired, broke, and felt like I had wasted years in school with no real skills.

Instead of giving up, I decided to build something useful.

In just **9 days**, while having almost no money, I learned to:
- Use real-world data (WFP CSV)
- Integrate AI (Gemini)
- Deploy a live web app
- Handle API keys securely

This project is proof that consistent daily effort can turn “I have no skills” into “I built something that can help people.”

Kilimarket AI is my first real step toward becoming a self-taught developer who creates value.

### 🏠 How to Run Locally

```bash
git clone https://github.com/jaymoh7/kilimarket-ai.git
cd kilimarket-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your Gemini API key
# Then run:
streamlit run app.py