# PythonAnywhere Deployment Guide

## 🚀 Deploy AI Abhinav to PythonAnywhere (Simplest Option)

### 1. Create PythonAnywhere Account
1. Go to https://pythonanywhere.com
2. Sign up for free account
3. Verify your email

### 2. Upload Your Code
1. Go to "Files" tab
2. Create folder: `ai-abhinav`
3. Upload all files from `railway-deploy/` folder
4. Or use Git: `git clone https://github.com/AbhinavG-1010/Abhinav-AI-Persona.git`

### 3. Install Dependencies
1. Go to "Consoles" tab
2. Open "Bash" console
3. Run:
```bash
cd ai-abhinav/railway-deploy
pip3.10 install --user -r requirements.txt
```

### 4. Create Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Choose Python 3.10
5. Click "Next"

### 5. Configure Web App
1. In "Code" section, set:
   - **Source code**: `/home/yourusername/ai-abhinav/railway-deploy`
2. In "WSGI configuration file", edit the file:
```python
import sys
path = '/home/yourusername/ai-abhinav/railway-deploy'
if path not in sys.path:
    sys.path.append(path)

from main import app
application = app
```

### 6. Set Environment Variables
1. In "Web" tab, go to "Environment variables"
2. Add:
```
OPENAI_API_KEY=your_actual_api_key_here
SECRET_KEY=any_random_string_here
JWT_SECRET_KEY=any_random_string_here
```

### 7. Reload Web App
1. Click "Reload" button
2. Your AI Abhinav will be live at: `https://yourusername.pythonanywhere.com`

## ✅ Why PythonAnywhere:
- No Docker complexity
- Simple file upload
- Free tier available
- Reliable hosting
- Easy to debug

## 🔧 Troubleshooting:
- Check "Error log" in Web tab
- Check "Server log" for runtime errors
- Make sure all dependencies are installed
