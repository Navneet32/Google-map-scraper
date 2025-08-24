# 🚀 Railway Deployment Guide

## 📋 **Deployment Files Overview**

This project includes all necessary files for seamless Railway deployment:

### **Core Files:**
- `simple_app.py` - Main FastAPI application
- `google_maps_scraper.py` - Clean Google Maps scraper (no external DB dependencies)
- `requirements.txt` - All Python dependencies with exact versions

### **Railway Configuration:**
- `railway.json` - Railway deployment settings (uses Nixpacks)
- `nixpacks.toml` - Nixpacks configuration for Python + Chrome
- `Procfile` - Process definition for Railway
- `start.sh` - Startup script with dependency verification

## 🔧 **Automatic Dependency Installation**

### **What Gets Installed Automatically:**
✅ **Python 3.11** - Latest stable Python version  
✅ **Chromium Browser** - System-level Chrome installation  
✅ **ChromeDriver** - WebDriver for Selenium  
✅ **All Python packages** - FastAPI, Selenium, lxml, etc.  

### **No More Manual Installation:**
❌ No need to run `/install-selenium` endpoint  
❌ No need to manually install dependencies after deployment  
❌ No more "module not found" errors  

## 🚀 **Deployment Process**

### **Step 1: Push to GitHub**
Upload these files to your GitHub repository:
```
Google-map-scraper/
├── simple_app.py          # Main API
├── google_maps_scraper.py  # Clean scraper
├── requirements.txt        # Dependencies
├── railway.json           # Railway config
├── nixpacks.toml          # Build config
├── Procfile              # Process config
└── start.sh              # Startup script
```

### **Step 2: Railway Auto-Deploy**
Railway will automatically:
1. **Detect Python project** via `requirements.txt`
2. **Install system packages** (Chrome, ChromeDriver) via `nixpacks.toml`
3. **Install Python dependencies** via `requirements.txt`
4. **Start the application** via `Procfile`

### **Step 3: Verify Deployment**
Test these endpoints after deployment:
```bash
# Health check
curl https://your-app.railway.app/health

# Dependency verification
curl https://your-app.railway.app/test-dependencies

# Chrome functionality
curl https://your-app.railway.app/test-chrome

# Google Maps scraping
curl https://your-app.railway.app/test-google-maps
```

## 🔍 **Troubleshooting**

### **If Dependencies Are Missing:**
1. Check Railway build logs for errors
2. Verify `requirements.txt` is properly formatted
3. Ensure `nixpacks.toml` is in the root directory

### **If Chrome Fails:**
1. Check that `nixpacks.toml` includes `chromium` and `chromedriver`
2. Verify Chrome options in `google_maps_scraper.py`
3. Test with `/test-chrome` endpoint

### **Build Logs Location:**
- Railway Dashboard → Your Project → Deployments → Build Logs

## ⚡ **Performance Optimizations**

### **Memory Usage:**
- Chrome runs in headless mode with memory optimizations
- Single-process mode for Railway's resource limits
- Automatic cleanup after each scraping session

### **Build Time:**
- Cached dependencies for faster rebuilds
- Optimized Nixpacks configuration
- Minimal Docker layers

## 🎯 **Expected Results**

After successful deployment:
- ✅ All endpoints working without manual intervention
- ✅ Chrome browser fully functional
- ✅ Google Maps scraping operational
- ✅ No dependency installation required
- ✅ Automatic restarts on failure

## 📊 **Monitoring**

### **Health Checks:**
- Railway automatically monitors `/health` endpoint
- 300-second timeout for scraping operations
- Auto-restart on failure (max 3 retries)

### **Logs:**
- Real-time logs available in Railway dashboard
- Detailed error reporting for debugging
- Performance metrics tracking

## 🔄 **Updates and Maintenance**

### **To Update Dependencies:**
1. Modify `requirements.txt`
2. Push to GitHub
3. Railway auto-deploys with new dependencies

### **To Update Chrome Configuration:**
1. Modify `google_maps_scraper.py`
2. Test locally first
3. Deploy via GitHub push

## 🎉 **Success Indicators**

Your deployment is successful when:
- ✅ `/health` returns `{"status": "healthy"}`
- ✅ `/test-chrome` returns `{"status": "success"}`
- ✅ `/test-google-maps` returns sample business data
- ✅ No "module not found" errors in logs
- ✅ Scraping completes without Chrome crashes
