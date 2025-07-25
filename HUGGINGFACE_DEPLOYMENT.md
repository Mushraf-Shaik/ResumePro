# 🚀 Hugging Face Spaces Deployment Guide

This guide will help you deploy ResumePro to Hugging Face Spaces, making your AI resume analyzer accessible to users worldwide.

## 📋 Prerequisites

1. **Hugging Face Account**: Create a free account at [huggingface.co](https://huggingface.co)
2. **Gemini API Key**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Git**: Ensure Git is installed on your system

## 🛠️ Deployment Steps

### Step 1: Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in the details:
   - **Space name**: `resumepro` (or your preferred name)
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: CPU basic (free tier)
   - **Visibility**: Public (or Private if preferred)

### Step 2: Clone Your Space Repository

```bash
# Clone the space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/resumepro
cd resumepro
```

### Step 3: Copy Project Files

Copy all files from your ResumePro project to the cloned space directory:

```bash
# Copy all project files (adjust paths as needed)
cp -r /path/to/your/resumepro/* ./
```

**Important Files for Hugging Face Spaces:**
- `README.md` (with Hugging Face header)
- `app.py` (entry point)
- `Dockerfile` (configured for port 7860)
- `requirements.txt`
- `backend/` directory (all backend files)
- `frontend/` directory (all frontend files)

### Step 4: Configure Environment Variables

1. In your Hugging Face Space settings, go to **"Settings" → "Variables and secrets"**
2. Add the following secrets:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `GEMINI_API_KEY` | `your_api_key_here` | Your Google Gemini API key |
| `SECRET_KEY` | `your_secret_key` | Flask secret key (generate a random string) |
| `FLASK_ENV` | `production` | Flask environment |

### Step 5: Push to Hugging Face

```bash
# Add all files
git add .

# Commit changes
git commit -m "Initial deployment of ResumePro"

# Push to Hugging Face Spaces
git push origin main
```

### Step 6: Monitor Deployment

1. Go to your Space page on Hugging Face
2. Watch the **"Logs"** tab for build progress
3. The deployment typically takes 5-10 minutes
4. Once complete, your app will be available at: `https://YOUR_USERNAME-resumepro.hf.space`

## 🔧 Configuration Details

### Dockerfile Configuration

The Dockerfile is configured for Hugging Face Spaces with:
- **Port 7860**: Standard port for Hugging Face Spaces
- **Python 3.11**: Stable Python version
- **NLTK data**: Pre-downloaded for text processing
- **Optimized build**: Efficient Docker layers

### App Structure

```
resumepro/
├── app.py                 # Hugging Face entry point
├── Dockerfile            # Container configuration
├── requirements.txt      # Python dependencies
├── README.md            # With Hugging Face header
├── backend/             # Flask application
│   ├── app.py          # Main Flask app
│   ├── analyzer.py     # Resume analysis logic
│   ├── gemini_analyzer.py
│   └── uploads/        # File uploads directory
└── frontend/           # Static web files
    ├── landing.html
    ├── results.html
    └── assets/
```

## 🚨 Troubleshooting

### Common Issues

1. **Build Fails**: Check the logs for missing dependencies or syntax errors
2. **App Won't Start**: Verify environment variables are set correctly
3. **Import Errors**: Ensure all Python paths are configured properly
4. **File Upload Issues**: Check file permissions and upload directory

### Debug Commands

```bash
# Check logs in Hugging Face Spaces
# Go to your Space → Logs tab

# Local testing with Docker
docker build -t resumepro .
docker run -p 7860:7860 --env-file .env resumepro
```

### Environment Variables Debug

Create a `.env` file locally for testing:

```bash
# Copy the example file
cp .env.example .env

# Edit with your values
nano .env
```

## 🎯 Post-Deployment

### Testing Your Deployment

1. Visit your Space URL
2. Upload a test resume (PDF/DOCX)
3. Enter a job description
4. Verify the analysis results

### Monitoring

- **Usage**: Monitor through Hugging Face Spaces dashboard
- **Logs**: Check application logs for errors
- **Performance**: Monitor response times and user feedback

### Updates

To update your deployed app:

```bash
# Make changes to your code
git add .
git commit -m "Update: description of changes"
git push origin main
```

## 🔒 Security Best Practices

1. **API Keys**: Always use environment variables, never hardcode
2. **File Uploads**: Validate file types and sizes
3. **Rate Limiting**: Consider implementing rate limiting for production
4. **CORS**: Configure CORS properly for your domain

## 📊 Scaling Considerations

### Free Tier Limitations
- **CPU**: Basic CPU (sufficient for most use cases)
- **Memory**: 16GB RAM limit
- **Storage**: Ephemeral storage (files are not persistent)
- **Concurrent Users**: Limited by hardware

### Upgrade Options
- **Hardware**: Upgrade to better CPU/GPU if needed
- **Persistent Storage**: Consider external storage for file persistence
- **Custom Domain**: Available with paid plans

## 🆘 Support

If you encounter issues:

1. **Hugging Face Community**: [Hugging Face Discord](https://discord.gg/hugging-face)
2. **Documentation**: [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
3. **GitHub Issues**: Create issues in your project repository

## 🎉 Success!

Once deployed, your ResumePro app will be:
- ✅ Publicly accessible via Hugging Face Spaces
- ✅ Automatically scaled and managed
- ✅ Integrated with Hugging Face ecosystem
- ✅ Free to use (on free tier)

Share your Space with the community and help job seekers optimize their resumes with AI! 🚀
