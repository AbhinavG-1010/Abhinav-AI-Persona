# Railway Deployment Guide

## 🚀 Quick Deploy to Railway

### 1. Environment Variables to Set in Railway

Go to your Railway project → Variables tab and add:

```
OPENAI_API_KEY=your_actual_api_key_here
SECRET_KEY=any_random_string_here
JWT_SECRET_KEY=any_random_string_here
```

### 2. Railway Configuration

**IMPORTANT**: Use the `railway-deploy/` directory for deployment to avoid size limits.

The following files are configured:
- ✅ `railway-deploy/Procfile` - Start command for Railway
- ✅ `railway-deploy/requirements.txt` - Python dependencies
- ✅ Optimized size: 552KB (well under 4GB limit)

### 3. Deployment Steps

1. **Go to Railway**: https://railway.app
2. **Sign up/Login** with GitHub
3. **Click "Deploy from GitHub"**
4. **Select repository**: `AbhinavG-1010/Abhinav-AI-Persona`
5. **Set Root Directory**: `railway-deploy` (IMPORTANT!)
6. **Railway will auto-detect** Python and start building
7. **Add environment variables** (see step 1)
8. **Deploy!**

### 4. After Deployment

- ✅ **Backend API** will be available at Railway's provided URL
- ✅ **Health check** available at `/health`
- ✅ **Personal info** available at `/personal-info`
- ✅ **Chat endpoint** available at `/conversation`

### 5. Frontend Deployment (Optional)

For the React frontend, you can:
1. **Deploy to Vercel** (recommended for React)
2. **Update API URL** in frontend to point to Railway backend
3. **Deploy frontend** separately

### 6. Custom Domain (Optional)

1. **Go to Railway project settings**
2. **Add custom domain**
3. **Update DNS** records
4. **SSL certificate** will be auto-generated

## 🔧 Troubleshooting

### Common Issues:
- **Build fails**: Check environment variables are set
- **API not responding**: Verify OPENAI_API_KEY is correct
- **Port issues**: Railway automatically sets PORT environment variable

### Logs:
- Check Railway build logs for errors
- Check Railway deploy logs for runtime issues

## 📱 Your AI Abhinav will be live at:
`https://your-railway-app.railway.app`

Perfect for sharing with recruiters! 🎯
