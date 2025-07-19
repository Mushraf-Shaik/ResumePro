from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import logging
import json
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from analyzer import ResumeAnalyzer
from gemini_analyzer import GeminiAnalyzer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
           static_folder='../frontend',
           template_folder='templates')

# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                            os.getenv('UPLOAD_FOLDER', 'uploads'))
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# App configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))  # 16MB default
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# Enable CORS
CORS(app)

# Initialize analyzers
resume_analyzer = ResumeAnalyzer()
gemini_analyzer = GeminiAnalyzer()

@app.route('/')
def index():
    """Serve the main application page."""
    return send_from_directory('../frontend', 'landing.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from the frontend directory."""
    return send_from_directory('../frontend', path)

@app.route('/upload')
def upload_page():
    """Serve the resume upload page."""
    return send_from_directory('../frontend', 'upload.html')

@app.route('/results.html')
def results_page():
    """Serve the results page."""
    return send_from_directory('../frontend', 'results.html')

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload for resume."""
    try:
        logger.info(f"Upload request received: {request.method}")
        logger.info(f"Request files: {request.files}")
        logger.info(f"Request form: {request.form}")
        
        # Check if the post request has the file part
        if 'file' not in request.files:
            if request.form.get('resume_text'):
                # Handle text input instead of file
                resume_text = request.form.get('resume_text')
                job_description = request.form.get('job_description', '')
                
                # Return the text for analysis
                return jsonify({
                    'success': True,
                    'message': 'Text received successfully',
                    'resume_text': resume_text,
                    'job_description': job_description
                })
            else:
                return jsonify({
                    'error': 'No file part or text input'
                }), 400
        
        file = request.files['file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({
                'error': 'No selected file'
            }), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract text from file based on file type
            try:
                file_ext = filename.rsplit('.', 1)[1].lower()
                resume_text = ""
                
                if file_ext == 'txt':
                    # Simple text file
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        resume_text = f.read()
                elif file_ext in ['doc', 'docx']:
                    # Try to extract text from Word documents
                    try:
                        import docx
                        doc = docx.Document(filepath)
                        resume_text = '\n'.join([para.text for para in doc.paragraphs])
                    except ImportError:
                        logger.warning("python-docx not installed, falling back to basic text extraction")
                        with open(filepath, 'rb') as f:
                            resume_text = str(f.read())
                elif file_ext == 'pdf':
                    # Try to extract text from PDF
                    try:
                        import PyPDF2
                        with open(filepath, 'rb') as f:
                            pdf_reader = PyPDF2.PdfReader(f)
                            resume_text = '\n'.join([page.extract_text() for page in pdf_reader.pages])
                    except ImportError:
                        logger.warning("PyPDF2 not installed, falling back to basic text extraction")
                        with open(filepath, 'rb') as f:
                            resume_text = str(f.read())
                else:
                    # Default fallback
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        resume_text = f.read()
                        
                logger.info(f"Extracted {len(resume_text)} characters from {filename}")
            except Exception as e:
                logger.error(f"Error extracting text from file: {str(e)}")
                resume_text = ""
            
            # Get job description if provided
            job_description = request.form.get('job_description', '')
            
            return jsonify({
                'success': True,
                'message': 'File uploaded successfully',
                'filename': filename,
                'resume_text': resume_text,
                'job_description': job_description
            })
        else:
            return jsonify({
                'error': 'File type not allowed'
            }), 400
            
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}", exc_info=True)
        return jsonify({
            'error': f"An error occurred during file upload: {str(e)}"
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """Analyze resume against job description."""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input
        if not data or 'resume_text' not in data or 'job_description' not in data:
            return jsonify({
                'error': 'Missing required fields: resume_text and job_description'
            }), 400
            
        resume_text = data['resume_text']
        job_description = data['job_description']
        
        # Check if texts are not empty
        if not resume_text.strip() or not job_description.strip():
            return jsonify({
                'error': 'Resume text and job description cannot be empty'
            }), 400
        
        # Log analysis request (without full text for privacy)
        logger.info(f"Analyzing resume (length: {len(resume_text)}) against job description (length: {len(job_description)})")
        
        # Check if we should use Gemini API
        use_gemini = data.get('use_gemini', False)
        
        # Perform analysis
        if use_gemini:
            try:
                logger.info("Using Gemini API for analysis")
                analysis_result = gemini_analyzer.analyze(resume_text, job_description)
            except Exception as e:
                logger.error(f"Gemini API analysis failed: {str(e)}, falling back to rule-based analysis")
                analysis_result = resume_analyzer.analyze(resume_text, job_description)
        else:
            analysis_result = resume_analyzer.analyze(resume_text, job_description)
        
        # Return results
        return jsonify(analysis_result)
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        return jsonify({
            'error': f"An error occurred during analysis: {str(e)}"
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'ai-resume-analyzer'
    })

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)
