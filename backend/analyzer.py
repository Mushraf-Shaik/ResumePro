import re
import string
import logging
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    """
    A class to analyze resumes against job descriptions.
    Uses NLP techniques to compare and score the match.
    """
    
    def __init__(self):
        """Initialize the ResumeAnalyzer with necessary NLTK resources."""
        # Download required NLTK resources
        try:
            self._download_nltk_resources()
        except Exception as e:
            logger.warning(f"Failed to download NLTK resources: {str(e)}. Some features may not work properly.")
        
        # Initialize lemmatizer
        self.lemmatizer = WordNetLemmatizer()
        
        # Get stopwords
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            # Fallback stopwords if NLTK download fails
            self.stop_words = {
                'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
                'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 
                'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 
                'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 
                'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 
                'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 
                'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
                'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 
                'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
                'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
                'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 
                'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 
                'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 
                't', 'can', 'will', 'just', 'don', 'should', 'now'
            }
        
        # Define section patterns
        self.section_patterns = {
            'skills': r'(?i)(skills|technical skills|core competencies|expertise|proficiencies|qualifications|technologies|tools)',
            'education': r'(?i)(education|academic|degree|university|college|school|certification)',
            'experience': r'(?i)(experience|work experience|employment|job history|professional experience|career)'
        }
        
        # Define common skills and education keywords
        self.common_skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust', 'typescript'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'asp.net'],
            'data': ['sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'oracle', 'sqlite', 'redis', 'elasticsearch'],
            'cloud': ['aws', 'azure', 'gcp', 'cloud', 'docker', 'kubernetes', 'terraform', 'serverless'],
            'ml_ai': ['machine learning', 'deep learning', 'ai', 'artificial intelligence', 'nlp', 'computer vision', 'tensorflow', 'pytorch', 'scikit-learn'],
            'tools': ['git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'jenkins', 'travis', 'circleci']
        }
    
    def _download_nltk_resources(self):
        """Download required NLTK resources."""
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
    
    def preprocess_text(self, text):
        """
        Preprocess text by converting to lowercase, removing punctuation,
        tokenizing, removing stopwords, and lemmatizing.
        
        Args:
            text (str): The text to preprocess
            
        Returns:
            list: List of preprocessed tokens
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        
        return tokens
    
    def extract_sections(self, text):
        """
        Extract different sections from the text.
        
        Args:
            text (str): The text to extract sections from
            
        Returns:
            dict: Dictionary containing extracted sections
        """
        sections = {}
        
        # Split text into lines
        lines = text.split('\n')
        
        current_section = None
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header
            is_header = False
            for section, pattern in self.section_patterns.items():
                if re.search(pattern, line) and len(line) < 50:  # Assume headers are relatively short
                    if current_section:
                        sections[current_section] = '\n'.join(section_content)
                    current_section = section
                    section_content = []
                    is_header = True
                    break
            
            if not is_header and current_section:
                section_content.append(line)
        
        # Add the last section
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        # If no sections were found, use the entire text
        if not sections:
            sections['full_text'] = text
            
        return sections
    
    def extract_keywords(self, text, n=30):
        """
        Extract important keywords from text.
        
        Args:
            text (str): The text to extract keywords from
            n (int): Number of keywords to extract
            
        Returns:
            list: List of extracted keywords
        """
        # Preprocess text
        tokens = self.preprocess_text(text)
        
        # Count token frequencies
        token_counts = Counter(tokens)
        
        # Filter out single character tokens and numbers
        token_counts = {token: count for token, count in token_counts.items() 
                      if len(token) > 1 and not token.isdigit()}
        
        # Get most common tokens
        keywords = [token for token, _ in token_counts.most_common(n)]
        
        return keywords
    
    def calculate_keyword_match(self, resume_keywords, job_keywords):
        """
        Calculate keyword match score.
        
        Args:
            resume_keywords (list): Keywords from resume
            job_keywords (list): Keywords from job description
            
        Returns:
            tuple: (score, matched_keywords, missing_keywords)
        """
        # Convert to sets for easier operations
        resume_set = set(resume_keywords)
        job_set = set(job_keywords)
        
        # Find matched and missing keywords
        matched_keywords = resume_set.intersection(job_set)
        missing_keywords = job_set.difference(resume_set)
        
        # Calculate score
        if not job_set:
            return 100, list(matched_keywords), []
        
        score = (len(matched_keywords) / len(job_set)) * 100
        
        return round(score), list(matched_keywords), list(missing_keywords)
    
    def analyze_skills(self, resume_text, job_text):
        """
        Analyze skills match between resume and job description.
        
        Args:
            resume_text (str): Resume text
            job_text (str): Job description text
            
        Returns:
            tuple: (score, details)
        """
        # Extract skills section if available
        resume_sections = self.extract_sections(resume_text)
        job_sections = self.extract_sections(job_text)
        
        # Use skills section if available, otherwise use full text
        resume_skills_text = resume_sections.get('skills', resume_text)
        job_skills_text = job_sections.get('skills', job_text)
        
        # Extract keywords
        resume_skills = self.extract_keywords(resume_skills_text, n=50)
        job_skills = self.extract_keywords(job_skills_text, n=50)
        
        # Calculate match
        score, matched_skills, missing_skills = self.calculate_keyword_match(resume_skills, job_skills)
        
        # Prepare details
        details = {
            'matched': matched_skills[:10],  # Limit to top 10 for display
            'missing': missing_skills[:10]   # Limit to top 10 for display
        }
        
        return score, details
    
    def analyze_experience(self, resume_text, job_text):
        """
        Analyze experience match between resume and job description.
        
        Args:
            resume_text (str): Resume text
            job_text (str): Job description text
            
        Returns:
            tuple: (score, details)
        """
        # Extract experience section if available
        resume_sections = self.extract_sections(resume_text)
        job_sections = self.extract_sections(job_text)
        
        # Use experience section if available, otherwise use full text
        resume_exp_text = resume_sections.get('experience', resume_text)
        job_exp_text = job_sections.get('experience', job_text)
        
        # Extract keywords
        resume_exp_keywords = self.extract_keywords(resume_exp_text, n=50)
        job_exp_keywords = self.extract_keywords(job_exp_text, n=50)
        
        # Calculate match
        score, matched_exp, _ = self.calculate_keyword_match(resume_exp_keywords, job_exp_keywords)
        
        # Look for years of experience in job description
        years_pattern = r'(\d+)[\+]?\s*(?:years|yrs|yr)(?:\s*of)?\s*(?:experience|exp)'
        years_match = re.search(years_pattern, job_text, re.IGNORECASE)
        
        required_years = 0
        if years_match:
            required_years = int(years_match.group(1))
        
        # Look for years of experience in resume
        resume_years_match = re.search(years_pattern, resume_text, re.IGNORECASE)
        resume_years = 0
        if resume_years_match:
            resume_years = int(resume_years_match.group(1))
        
        # Adjust score based on years of experience
        years_score = 100
        years_detail = ""
        if required_years > 0:
            if resume_years >= required_years:
                years_score = 100
                years_detail = f"You meet the required {required_years}+ years of experience."
            else:
                years_score = (resume_years / required_years) * 100
                years_detail = f"The job requires {required_years}+ years of experience, but your resume shows {resume_years}."
        
        # Combine keyword match score with years score
        final_score = round((score + years_score) / 2) if required_years > 0 else score
        
        # Prepare details
        details = []
        if years_detail:
            details.append(years_detail)
        
        if matched_exp:
            details.append(f"Your experience matches key requirements: {', '.join(matched_exp[:5])}...")
        
        return final_score, details
    
    def analyze_education(self, resume_text, job_text):
        """
        Analyze education match between resume and job description.
        
        Args:
            resume_text (str): Resume text
            job_text (str): Job description text
            
        Returns:
            tuple: (score, details)
        """
        # Extract education section if available
        resume_sections = self.extract_sections(resume_text)
        job_sections = self.extract_sections(job_text)
        
        # Use education section if available, otherwise use full text
        resume_edu_text = resume_sections.get('education', resume_text)
        job_edu_text = job_sections.get('education', job_text)
        
        # Common degree patterns
        degree_patterns = {
            'phd': r'(?i)(phd|ph\.d|doctor of philosophy|doctorate)',
            'masters': r'(?i)(master|ms|m\.s|m\.a|mba|m\.b\.a)',
            'bachelors': r'(?i)(bachelor|bs|b\.s|ba|b\.a|undergraduate)',
            'associate': r'(?i)(associate|a\.a|a\.s)',
            'highschool': r'(?i)(high school|diploma|ged)'
        }
        
        # Check for required degree in job description
        required_degree = None
        for degree, pattern in degree_patterns.items():
            if re.search(pattern, job_edu_text) or re.search(pattern, job_text):
                required_degree = degree
                break
        
        # Check for degree in resume
        resume_degree = None
        for degree, pattern in degree_patterns.items():
            if re.search(pattern, resume_edu_text) or re.search(pattern, resume_text):
                resume_degree = degree
                break
        
        # Degree hierarchy for scoring
        degree_hierarchy = {
            'phd': 5,
            'masters': 4,
            'bachelors': 3,
            'associate': 2,
            'highschool': 1,
            None: 0
        }
        
        # Calculate education score
        score = 100
        details = []
        
        if required_degree:
            if resume_degree:
                if degree_hierarchy[resume_degree] >= degree_hierarchy[required_degree]:
                    score = 100
                    details.append(f"Your {resume_degree}'s degree meets or exceeds the required {required_degree}'s degree.")
                else:
                    # Score based on how close the degrees are
                    score = (degree_hierarchy[resume_degree] / degree_hierarchy[required_degree]) * 100
                    details.append(f"The job requires a {required_degree}'s degree, but your resume shows a {resume_degree}'s degree.")
            else:
                score = 0
                details.append(f"The job requires a {required_degree}'s degree, but no degree was detected in your resume.")
        else:
            if resume_degree:
                details.append(f"No specific degree requirement found in job description. Your {resume_degree}'s degree is a plus.")
            else:
                details.append("No specific degree requirements found in job description or resume.")
        
        # Extract field of study from job description
        field_patterns = [
            r'(?i)degree in ([^,.]+)',
            r'(?i)background in ([^,.]+)',
            r'(?i)(computer science|engineering|business|marketing|finance|accounting|economics|mathematics|statistics)'
        ]
        
        required_field = None
        for pattern in field_patterns:
            field_match = re.search(pattern, job_text)
            if field_match:
                required_field = field_match.group(1).strip().lower()
                break
        
        # Check if field is in resume
        field_in_resume = False
        if required_field and (required_field in resume_text.lower() or required_field in resume_edu_text.lower()):
            field_in_resume = True
            details.append(f"Your education matches the required field: {required_field}.")
        elif required_field:
            details.append(f"The job requires education in {required_field}, which was not clearly found in your resume.")
            # Reduce score if field not found
            score = max(score - 20, 0)
        
        return round(score), details
    
    def generate_suggestions(self, resume_text, job_text, analysis_results):
        """
        Generate improvement suggestions based on analysis results.
        
        Args:
            resume_text (str): Resume text
            job_text (str): Job description text
            analysis_results (dict): Results from previous analyses
            
        Returns:
            list: List of suggestions
        """
        suggestions = []
        
        # Skills suggestions
        skills_score = analysis_results.get('skills_score', 0)
        skills_details = analysis_results.get('skills_details', {})
        
        if skills_score < 70 and 'missing' in skills_details:
            missing_skills = skills_details['missing']
            if missing_skills:
                suggestions.append(f"Add these key skills to your resume: {', '.join(missing_skills[:5])}")
        
        # Experience suggestions
        experience_score = analysis_results.get('experience_score', 0)
        if experience_score < 70:
            suggestions.append("Highlight more relevant experience that aligns with job requirements.")
            
            # Look for specific experience requirements
            exp_patterns = [
                r'(?i)experience (?:in|with) ([^,.]+)',
                r'(?i)knowledge of ([^,.]+)',
                r'(?i)familiarity with ([^,.]+)'
            ]
            
            for pattern in exp_patterns:
                matches = re.finditer(pattern, job_text)
                for match in matches:
                    req = match.group(1).strip()
                    if req.lower() not in resume_text.lower():
                        suggestions.append(f"Consider adding experience with {req} if you have it.")
                        break
        
        # Education suggestions
        education_score = analysis_results.get('education_score', 0)
        if education_score < 70:
            suggestions.append("Your education section may need improvement to better match job requirements.")
        
        # General suggestions
        # Check resume length by word count
        resume_word_count = len(resume_text.split())
        if resume_word_count < 300:
            suggestions.append("Your resume seems short. Consider adding more details about your experience and skills.")
        elif resume_word_count > 1000:
            suggestions.append("Your resume is quite long. Consider focusing on the most relevant information.")
        
        # Check for contact information
        contact_patterns = [
            r'(?i)(?:\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)',  # Email
            r'(?i)(?:\+\d{1,3}[-\s]?)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}',    # Phone
            r'(?i)linkedin\.com/in/[\w-]+'                                    # LinkedIn
        ]
        
        has_contact = any(re.search(pattern, resume_text) for pattern in contact_patterns)
        if not has_contact:
            suggestions.append("Add your contact information (email, phone) to your resume.")
        
        # Check for achievements and metrics
        achievement_patterns = [
            r'(?i)increased|improved|reduced|saved|achieved|won|delivered|managed|led'
        ]
        
        has_achievements = any(re.search(pattern, resume_text) for pattern in achievement_patterns)
        if not has_achievements:
            suggestions.append("Add specific achievements with metrics to strengthen your experience section.")
        
        # Check for ATS-friendly formatting
        if len(re.findall(r'[^\x00-\x7F]', resume_text)) > 5:  # Non-ASCII characters
            suggestions.append("Use standard characters and formatting for better ATS compatibility.")
        
        # Limit suggestions to avoid overwhelming
        if not suggestions:
            suggestions.append("Your resume appears to be well-aligned with the job description. Consider tailoring specific achievements to match job requirements even more closely.")
        
        return suggestions[:7]  # Limit to top 7 suggestions
    
    def analyze(self, resume_text, job_description):
        """
        Analyze resume against job description.
        
        Args:
            resume_text (str): Resume text
            job_description (str): Job description text
            
        Returns:
            dict: Analysis results
        """
        try:
            # Analyze skills
            skills_score, skills_details = self.analyze_skills(resume_text, job_description)
            
            # Analyze experience
            experience_score, experience_details = self.analyze_experience(resume_text, job_description)
            
            # Analyze education
            education_score, education_details = self.analyze_education(resume_text, job_description)
            
            # Extract keywords for general matching
            resume_keywords = self.extract_keywords(resume_text, n=100)
            job_keywords = self.extract_keywords(job_description, n=100)
            
            # Calculate keyword match
            keywords_score, matched_keywords, missing_keywords = self.calculate_keyword_match(resume_keywords, job_keywords)
            keywords_details = {
                'matched': matched_keywords[:15],
                'missing': missing_keywords[:15]
            }
            
            # Calculate overall score
            # Weights: skills (35%), experience (35%), education (20%), keywords (10%)
            overall_score = round(
                (skills_score * 0.35) + 
                (experience_score * 0.35) + 
                (education_score * 0.20) + 
                (keywords_score * 0.10)
            )
            
            # Prepare results
            results = {
                'overall_score': overall_score,
                'skills_score': skills_score,
                'skills_details': skills_details,
                'experience_score': experience_score,
                'experience_details': experience_details,
                'education_score': education_score,
                'education_details': education_details,
                'keywords_score': keywords_score,
                'keywords_details': keywords_details
            }
            
            # Generate suggestions
            results['suggestions'] = self.generate_suggestions(resume_text, job_description, results)
            
            return results
            
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}", exc_info=True)
            raise
