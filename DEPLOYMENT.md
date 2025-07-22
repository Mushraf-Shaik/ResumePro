# Deployment Guide for ResumePro on Render

## Prerequisites
1. A Render account (sign up at https://render.com)
2. Your code pushed to a GitHub repository
3. A Gemini API key from Google AI Studio

## Step-by-Step Deployment

### 1. Push Your Code to GitHub
Make sure your project is in a GitHub repository with all the files we just created.

### 2. Create a New Web Service on Render
1. Go to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Choose the repository containing your ResumePro project

### 3. Configure the Web Service
Use these settings:
- **Name**: `resumepro` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && gunicorn --bind 0.0.0.0:$PORT app:app`
- **Instance Type**: Free tier is fine for testing

### 4. Set Environment Variables
In the Render dashboard, add these environment variables:
- `GEMINI_API_KEY`: Your actual Gemini API key
- `FLASK_ENV`: `production`
- `FLASK_DEBUG`: `False`
- `UPLOAD_FOLDER`: `uploads`
- `MAX_CONTENT_LENGTH`: `16777216`
- `SECRET_KEY`: Generate a secure random string

### 5. Deploy
Click "Create Web Service" and Render will automatically deploy your application.

## Important Notes

### File Uploads
- Render's free tier has ephemeral storage, meaning uploaded files will be deleted when the service restarts
- For production, consider using cloud storage (AWS S3, Google Cloud Storage, etc.)

### Environment Variables
- Never commit your `.env` file to GitHub
- Always use Render's environment variable settings for sensitive data

### Monitoring
- Check the Render logs if deployment fails
- The health check endpoint is available at `/health`

## Troubleshooting

### Common Issues
1. **Build fails**: Check that all dependencies are in requirements.txt
2. **App won't start**: Verify the start command and port configuration
3. **API errors**: Ensure GEMINI_API_KEY is set correctly

### Logs
Access logs through the Render dashboard to debug issues.

## Next Steps
After successful deployment:
1. Test all functionality on the live URL
2. Set up a custom domain (optional)
3. Consider upgrading to a paid plan for better performance
4. Implement proper file storage for production use
