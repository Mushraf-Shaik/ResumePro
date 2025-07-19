# ResumePro - AI Resume Analyzer 🚀

A sophisticated AI-powered resume analyzer that provides comprehensive ATS compatibility scoring, keyword matching, and actionable feedback to help job seekers optimize their resumes for better job application success.

![ResumePro](https://img.shields.io/badge/ResumePro-AI%20Resume%20Analyzer-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-Styling-blue)

## ✨ Features

### 🎯 **Core Functionality**
- **AI-Powered Resume Analysis**: Advanced natural language processing for comprehensive resume evaluation
- **ATS Compatibility Scoring**: Detailed analysis of how well your resume works with Applicant Tracking Systems
- **Job Description Matching**: Compare your resume against specific job requirements
- **Keyword Analysis**: Identify matched and missing keywords with one-click copy functionality
- **Skills Assessment**: Comprehensive skills matching and gap analysis
- **Experience & Education Matching**: Evaluate how your background aligns with job requirements

### 🎨 **Modern UI/UX**
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Interactive Animations**: Smooth progress bars, score counting, and visual feedback
- **Professional Styling**: Clean, modern interface built with Tailwind CSS
- **Intuitive Navigation**: User-friendly flow from upload to results
- **Visual Score Presentation**: Circular progress indicators and color-coded feedback

### 📊 **Advanced Analytics**
- **Two-Phase Analysis System**: Document parsing + job matching phases
- **Weighted Scoring Algorithm**: Comprehensive scoring based on multiple factors
- **Detailed Breakdown**: ATS compatibility, keyword matching, skills analysis
- **Actionable Suggestions**: Specific recommendations for resume improvement
- **Copy-to-Clipboard**: Easy copying of missing keywords for resume updates

## 🏗️ Architecture

### **Backend (Flask)**
```
backend/
├── app.py              # Main Flask application
├── analyzer.py         # AI analysis engine
├── requirements.txt    # Python dependencies
└── uploads/           # Temporary file storage
```

### **Frontend (HTML/CSS/JS)**
```
frontend/
├── landing.html       # Landing page with feature overview
├── upload.html        # Resume upload and job description input
├── results.html       # Analysis results display
├── js/
│   ├── upload.js      # Upload functionality and form handling
│   └── results.js     # Results display and animations
└── css/              # Custom styles (uses Tailwind CSS CDN)
```

## 🚀 Getting Started

### **Prerequisites**
- Python 3.8 or higher
- Modern web browser
- Internet connection (for Tailwind CSS CDN)

### **Installation**

1. **Clone the repository**
```bash
git clone https://github.com/Mushraf-Shaik/ResumePro.git
cd ResumePro
```

2. **Set up the backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Access the application**
Open your browser and navigate to `http://localhost:5000`

### **Usage**

1. **Upload Resume**: Upload your resume in PDF, DOC, or DOCX format
2. **Add Job Description**: Paste the job description for targeted analysis
3. **Get Analysis**: Receive comprehensive ATS scoring and feedback
4. **Review Results**: See matched/missing keywords, skills analysis, and suggestions
5. **Improve Resume**: Use the copy feature to add missing keywords to your resume

## 🎯 Analysis Components

### **ATS Compatibility Score**
- Document parsing and formatting analysis
- ATS-friendly structure evaluation
- Readability and parsing success rate

### **Keyword Matching**
- Job-specific keyword identification
- Industry-standard terminology matching
- Missing keyword suggestions with copy functionality

### **Skills Analysis**
- Technical and soft skills evaluation
- Skills gap identification
- Competency level assessment

### **Experience & Education Match**
- Work experience relevance scoring
- Educational background alignment
- Career progression analysis

## 🛠️ Technology Stack

### **Backend**
- **Flask**: Web framework for Python
- **Natural Language Processing**: Text analysis and keyword extraction
- **File Processing**: PDF, DOC, DOCX parsing capabilities
- **RESTful API**: Clean API endpoints for frontend integration

### **Frontend**
- **HTML5**: Semantic markup and accessibility
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Vanilla JavaScript**: Interactive functionality and animations
- **Responsive Design**: Mobile-first approach

### **Features**
- **Drag & Drop Upload**: Intuitive file upload interface
- **Real-time Feedback**: Instant visual feedback during analysis
- **Progressive Enhancement**: Works without JavaScript (basic functionality)
- **Cross-browser Compatibility**: Supports all modern browsers

## 📈 Future Enhancements

- [ ] User authentication and resume history
- [ ] Multiple resume format support
- [ ] Industry-specific analysis templates
- [ ] Resume builder integration
- [ ] API rate limiting and caching
- [ ] Advanced NLP models integration
- [ ] Resume comparison features
- [ ] Export analysis reports (PDF)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Mushraf Shaik**
- GitHub: [@Mushraf-Shaik](https://github.com/Mushraf-Shaik)
- LinkedIn: [Connect with me](https://linkedin.com/in/mushraf-shaik)

## 🙏 Acknowledgments

- Thanks to the open-source community for the amazing tools and libraries
- Inspired by the need for better resume optimization tools
- Built with modern web development best practices

---

**Made with ❤️ for job seekers everywhere**

*ResumePro - Empowering your job search with AI-driven insights*
