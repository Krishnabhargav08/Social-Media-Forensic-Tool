# 🚀 Real API Integration & Advanced AI Guide

## Overview
This forensic tool now supports **optional** real-time scraping and advanced AI analysis. By default, it runs in **simulated mode** for demonstration. Enable real APIs when you're ready!

---

## 📊 Feature Status

| Feature | Default Mode | With API Keys |
|---------|-------------|---------------|
| **Data Scraping** | ✅ Simulated (Demo) | ⚡ Real-time via APIs |
| **Sentiment Analysis** | ✅ Basic (TextBlob) | 🧠 Advanced (GPT-4/BERT) |
| **Risk Detection** | ✅ Rule-based | 🤖 AI-powered |

---

## 🔧 Setup Instructions

### 1️⃣ Install Optional Dependencies

```bash
# For Real API Scraping
pip install tweepy instaloader praw

# For Advanced AI Analysis
pip install openai transformers torch sentencepiece
```

Or install all at once:
```bash
pip install tweepy instaloader praw openai transformers torch sentencepiece
```

---

### 2️⃣ Get API Keys

#### 🐦 Twitter API (FREE Tier Available)
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a new App
3. Get your **Bearer Token** from the Keys section
4. Optional: Get API Key, API Secret, Access Token, Access Secret

#### 📸 Instagram API (Requires Facebook Developer Account)
1. Go to https://developers.facebook.com/apps/
2. Create a new app
3. Add Instagram Basic Display or Instagram Graph API
4. Get your **Access Token**

⚠️ **Note**: Instagram scraping has limitations. Consider using official Instagram Graph API.

#### 🔴 Reddit API (FREE)
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Select "script" type
4. Get your **Client ID** and **Client Secret**

#### 🤖 OpenAI API (Paid - $0.03 per 1K tokens for GPT-4)
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add credits to your account (minimum $5)

---

### 3️⃣ Configure Environment Variables

Edit `backend/.env` file:

```bash
# Enable real scraping
USE_REAL_SCRAPING=True

# Twitter API
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAxxxxxxx
TWITTER_API_KEY=xxxxxxxxxxxxxxxxxxxx
TWITTER_API_SECRET=xxxxxxxxxxxxxxxxxxxx
TWITTER_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxx
TWITTER_ACCESS_SECRET=xxxxxxxxxxxxxxxxxxxx

# Reddit API
REDDIT_CLIENT_ID=xxxxxxxxxxxxxxxxxxxx
REDDIT_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxx
REDDIT_USER_AGENT=ForensicTool/1.0

# Instagram API (Optional)
INSTAGRAM_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxx

# Enable Advanced AI
USE_ADVANCED_AI=True

# OpenAI API
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

---

### 4️⃣ Restart Backend

```bash
cd backend
python app.py
```

You should see:
```
✅ Twitter API initialized
✅ Reddit API initialized
✅ OpenAI GPT-4 initialized
✅ HuggingFace transformers initialized
```

---

## 🎯 Usage Examples

### Real Twitter Scraping
```python
# Create case with username: @elonmusk
# Click "Scrape Data"
# Real tweets will be fetched using Twitter API
```

### Real Reddit Scraping
```python
# Create case with username: spez
# Select platform: Reddit
# Click "Scrape Data"
# Real Reddit posts/comments will be fetched
```

### GPT-4 Analysis
```python
# After scraping real data
# Click "Analyze Data"
# GPT-4 will provide detailed forensic analysis
# Sentiment analysis using BERT transformers
```

---

## 💰 Cost Estimates

### Twitter API
- **FREE Tier**: 500K tweets/month
- **Basic Tier**: $100/month for 2M tweets

### Reddit API
- **100% FREE** (rate limited to 60 requests/minute)

### OpenAI GPT-4
- **Input**: $0.03 per 1K tokens (~750 words)
- **Output**: $0.06 per 1K tokens
- **Average cost per analysis**: $0.05 - $0.20

### HuggingFace Transformers
- **100% FREE** (runs locally on your machine)
- Requires: 2GB RAM minimum

---

## 🛡️ Legal & Ethical Considerations

### ⚠️ Important Disclaimers:

1. **Terms of Service**
   - Twitter API: Must comply with Twitter Developer Agreement
   - Instagram: Scraping may violate ToS (use official API only)
   - Reddit: Follow API usage guidelines

2. **Privacy Laws**
   - Ensure compliance with GDPR, CCPA, and local data protection laws
   - Only collect publicly available data
   - Obtain necessary permissions for forensic investigations

3. **Ethical Usage**
   - Use for legitimate forensic investigations only
   - Respect user privacy
   - Follow law enforcement procedures

4. **Academic/Research Use**
   - Clearly state this is for educational purposes
   - Include disclaimers in project documentation
   - Follow institutional ethics guidelines

---

## 🔄 Fallback Behavior

The tool automatically handles API failures:

```
1. Try Real API → If available and configured
2. Fall Back to Simulated Data → If API fails or not configured
3. Basic Analysis → If advanced AI not available
```

This ensures your tool always works, even without API keys!

---

## 🧪 Testing

### Test Real Scraping (Twitter)
```bash
# 1. Set valid Twitter Bearer Token in .env
# 2. Set USE_REAL_SCRAPING=True
# 3. Create case for @twitter (official Twitter account)
# 4. Check console for "✅ Twitter API initialized"
# 5. Scrape data - should get real tweets
```

### Test Advanced AI
```bash
# 1. Set valid OpenAI API key in .env
# 2. Set USE_ADVANCED_AI=True
# 3. Analyze any case
# 4. Check for GPT-4 insights in analysis results
```

---

## 📝 Development Tips

### Run in Hybrid Mode
```bash
# Use real Twitter + simulated Instagram
TWITTER_BEARER_TOKEN=xxx
USE_REAL_SCRAPING=True
# Leave Instagram keys empty - will use simulated data
```

### Debug API Issues
```bash
# Backend will log API status
python app.py
# Look for:
# ✅ Twitter API initialized
# ⚠️  Instagram API error: ...
```

---

## 🆘 Troubleshooting

### "tweepy not installed"
```bash
pip install tweepy
```

### "OpenAI API key invalid"
```bash
# Check your key at: https://platform.openai.com/api-keys
# Ensure billing is enabled
```

### "Rate limit exceeded"
```bash
# Twitter: Wait 15 minutes or upgrade plan
# Reddit: Wait 1 minute
# OpenAI: Add more credits
```

---

## 📚 Additional Resources

- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [Reddit API Documentation](https://www.reddit.com/dev/api)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [HuggingFace Transformers Guide](https://huggingface.co/docs/transformers)

---

## ✅ Project Presentation Tips

For your BTech project demonstration:

1. **Default Mode (No API Keys)**
   - Show simulated data scraping
   - Explain it's for demonstration
   - Mention real API support is available

2. **With API Keys (Optional)**
   - Demo real Twitter scraping
   - Show GPT-4 analysis results
   - Highlight advanced AI capabilities

3. **Future Work Section**
   - Mention real-time API integration
   - Discuss advanced AI enhancements
   - Note ethical considerations

---

**Remember**: The tool works perfectly in simulated mode for your BTech project. Real APIs are optional enhancements!
