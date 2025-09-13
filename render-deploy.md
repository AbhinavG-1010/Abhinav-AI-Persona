# Render Deployment Guide

## 🚀 Deploy AI Abhinav to Render (Free & Reliable)

### 1. Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Verify your email

### 2. Deploy Backend
1. Click "New +" → "Web Service"
2. Connect GitHub repository: `AbhinavG-1010/Abhinav-AI-Persona`
3. **Root Directory**: `railway-deploy`
4. **Environment**: Python 3
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. Environment Variables
Add these in Render dashboard:
```
OPENAI_API_KEY=your_actual_api_key_here
SECRET_KEY=any_random_string_here
JWT_SECRET_KEY=any_random_string_here
```

### 4. Deploy Frontend (Optional)
1. Go to Vercel.com
2. Import your GitHub repo
3. Set **Root Directory**: `frontend`
4. Deploy!

### 5. Your AI Abhinav will be live at:
- **Backend**: `https://your-app.onrender.com`
- **Frontend**: `https://your-app.vercel.app` (if deployed)

## ✅ Why Render is Better:
- More reliable than Railway
- Better error messages
- No size limits on free tier
- Automatic HTTPS
- Custom domains available
- 750 hours/month free

## 🔧 If Render Fails:
Try PythonAnywhere (simpler, no Docker):
1. Go to https://pythonanywhere.com
2. Upload your `railway-deploy` folder
3. Set up web app with Flask/FastAPI
4. Add environment variables
