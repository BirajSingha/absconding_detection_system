# .env Setup Guide for Absconding Detection System

## ✅ What I Did

1. **Created comprehensive `.env.example`** - Template with all configurations
2. **Checked existing `.env`** - You already have one!
3. **Created this guide** - Step-by-step setup instructions

---

## 🔧 How to Configure Your `.env` File

### Step 1: Open `.env` File

Open `backend/.env` in your editor

### Step 2: Required Configurations

#### **Minimum to Run** (Basic functionality):

```bash
# Database (this is fine for development)
DATABASE_URL=sqlite:///absconding.db

# Flask Secret (generate a new one)
SECRET_KEY=dev-secret-key-change-this

# These can stay commented out for testing without AI features
# ANTHROPIC_API_KEY=
# CHROMA_API_KEY=
```

#### **For Full AI Features** (RAG + Semantic Search):

```bash
# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-api03-...your-key-here

# Get from: https://www.trychroma.com/
CHROMA_API_KEY=your-chroma-key
CHROMA_TENANT=your-tenant-id
CHROMA_DATABASE=absconding-detection-system
```

#### **For Slack Notifications** (Optional):

```bash
# Get from: https://api.slack.com/apps
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_CHANNEL_ID=C0123456789
```

#### **For Email Notifications** (Optional - New!):

```bash
# For Gmail (recommended for testing)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password  # NOT your Gmail password!
HR_TEAM_EMAILS=hr@company.com,manager@company.com
```

---

## 📧 Email Setup Guide (Gmail)

### Step-by-Step: Get Gmail App Password

1. **Go to Google Account**

   - Visit: https://myaccount.google.com/

2. **Enable 2-Step Verification**

   - Security → 2-Step Verification
   - Follow prompts to enable

3. **Generate App Password**

   - Security → 2-Step Verification → App Passwords
   - Select "Mail" and "Other (Custom name)"
   - Name it: "Absconding Detection System"
   - Click "Generate"
   - Copy the 16-character password

4. **Add to `.env`**
   ```bash
   SENDER_EMAIL=youremail@gmail.com
   SENDER_PASSWORD=abcd efgh ijkl mnop  # (spaces don't matter)
   HR_TEAM_EMAILS=recipient1@email.com,recipient2@email.com
   ```

---

## 🎯 Quick Testing Configurations

### Config 1: **Demo Mode** (No External Services)

```bash
DATABASE_URL=sqlite:///absconding.db
SECRET_KEY=demo-secret-key
# Everything else commented out
# System will work but use mock data for RAG/Slack/Email
```

### Config 2: **AI Enabled** (RAG working)

```bash
DATABASE_URL=sqlite:///absconding.db
SECRET_KEY=your-secret-key
ANTHROPIC_API_KEY=sk-ant-...
CHROMA_API_KEY=your-chroma-key
CHROMA_TENANT=your-tenant
CHROMA_DATABASE=absconding-detection-system
# Notifications still mocked
```

### Config 3: **Full Production** (Everything)

```bash
DATABASE_URL=sqlite:///absconding.db
SECRET_KEY=your-secret-key
ANTHROPIC_API_KEY=sk-ant-...
CHROMA_API_KEY=your-chroma-key
CHROMA_TENANT=your-tenant
CHROMA_DATABASE=absconding-detection-system
SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL_ID=C01...
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=youremail@gmail.com
SENDER_PASSWORD=your-app-password
HR_TEAM_EMAILS=hr@company.com
```

---

## 🔐 Security Best Practices

### ✅ DO:

- ✅ Keep `.env` file private (never commit to git)
- ✅ Use App Passwords for Gmail (not account password)
- ✅ Generate strong SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
- ✅ Rotate API keys regularly
- ✅ Use different `.env` for dev/staging/production

### ❌ DON'T:

- ❌ Commit `.env` to version control
- ❌ Share `.env` file publicly
- ❌ Use production API keys in development
- ❌ Use your actual Gmail password (use App Password!)
- ❌ Leave default SECRET_KEY in production

---

## 🧪 Testing Your Configuration

### Test 1: Database Connection

```bash
cd backend
python -c "from app import create_app; app = create_app(); print('✓ Database connected!')"
```

### Test 2: RAG Service (if configured)

```bash
python -c "from app.services.rag_service import get_rag_service; rag = get_rag_service(); print('✓ RAG service initialized!')"
```

### Test 3: Email Service

```bash
python -c "from app.services.email_service import get_email_service; email = get_email_service(); print('✓ Email service ready!')"
```

### Test 4: Full System

```bash
python test_integration.py
```

---

## 📋 Current Status Check

Run this to see what's configured:

```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

print('Environment Configuration Status:')
print('=' * 50)
print(f'Database: {'✓' if os.getenv('DATABASE_URL') else '✗'} {os.getenv('DATABASE_URL', 'Not set')[:30]}...')
print(f'Secret Key: {'✓' if os.getenv('SECRET_KEY') else '✗'} {'Set' if os.getenv('SECRET_KEY') else 'Not set'}')
print(f'Anthropic: {'✓' if os.getenv('ANTHROPIC_API_KEY') else '✗'} {'Set' if os.getenv('ANTHROPIC_API_KEY') else 'Not set'}')
print(f'ChromaDB: {'✓' if os.getenv('CHROMA_API_KEY') else '✗'} {'Set' if os.getenv('CHROMA_API_KEY') else 'Not set'}')
print(f'Slack: {'✓' if os.getenv('SLACK_BOT_TOKEN') else '✗'} {'Set' if os.getenv('SLACK_BOT_TOKEN') else 'Not set'}')
print(f'Email: {'✓' if os.getenv('SENDER_EMAIL') else '✗'} {'Set' if os.getenv('SENDER_EMAIL') else 'Not set'}')
print('=' * 50)
"
```

---

## 🚨 Troubleshooting

### Issue: "Module 'dotenv' not found"

```bash
pip install python-dotenv
```

### Issue: ".env file not loading"

- Check file is named `.env` (not `.env.txt`)
- Check it's in `backend/` directory
- Restart Flask server after editing

### Issue: "Gmail authentication failed"

- Use App Password, not account password
- Enable 2-Step Verification first
- Check for typos in email/password

### Issue: "Anthropic API key invalid"

- Verify key starts with `sk-ant-`
- Check for extra spaces
- Ensure key is active at https://console.anthropic.com/

---

## 💡 Recommended Setup for Hackathon

**For quick demo** (minimal setup):

```bash
# Copy this to your .env file:
DATABASE_URL=sqlite:///absconding.db
SECRET_KEY=hackathon-demo-secret-key
# Leave AI services commented out - system will use mock mode
```

**For full features** (requires API keys):

1. Get Anthropic API key (free trial available)
2. Set up ChromaDB Cloud (free tier)
3. Configure Gmail App Password for email
4. Update `.env` with all credentials

---

## ✅ Next Steps

1. **Edit `.env`** with your chosen configuration
2. **Restart Flask server** if running
3. **Test with**: `python test_integration.py`
4. **Check startup logs** for service initialization messages

---

**Your `.env` file location**: `backend/.env`  
**Template with all options**: `backend/.env.example`

Need help with any specific service setup? Let me know! 🚀
