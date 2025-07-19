import requests
import json
import logging
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GeminiAnalyzer:
    """
    A class to analyze resumes against job descriptions using the Gemini API.
    """
    
    def __init__(self, api_key=None):
        """Initialize the GeminiAnalyzer with API key."""
        # Load environment variables
        load_dotenv()
        
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "AIzaSyCPxs9vFYMKxUCr91dplmwR495ipFxUzj8")
        
        if not self.api_key:
            logger.warning("No Gemini API key provided. Gemini analysis will not work.")
        
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    def analyze(self, resume_text, job_description):
        """
        Analyze resume against job description using Gemini API.
        
        Args:
            resume_text (str): Resume text
            job_description (str): Job description text
            
        Returns:
            dict: Analysis results
        """
        try:
            if not self.api_key:
                raise ValueError("Gemini API key not provided")
            
            # Prepare prompt for Gemini
            prompt = self._prepare_prompt(resume_text, job_description)
            
            # Call Gemini API
            response = self._call_gemini_api(prompt)
            
            # Parse and format response
            results = self._parse_response(response)
            
            return results
            
        except Exception as e:
            logger.error(f"Error during Gemini analysis: {str(e)}", exc_info=True)
            raise
    
    def _prepare_prompt(self, resume_text, job_description):
        """
        Prepare prompt for Gemini API.
        
        Args:
            resume_text (str): Resume text
            job_description (str): Job description text
            
        Returns:
            str: Formatted prompt
        """
        # Limit text length to avoid token limits
        max_length = 10000
        resume_text = resume_text[:max_length] if len(resume_text) > max_length else resume_text
        job_description = job_description[:max_length] if len(job_description) > max_length else job_description
        
        prompt = f"""
        You are an AI Resume Analyzer. Analyze the resume against the job description provided below.
        
        Resume:
        {resume_text}
        
        Job Description:
        {job_description}
        
        Provide a detailed analysis with the following:
        1. Overall match score (percentage)
        2. Skills match (percentage and details)
        3. Experience match (percentage and details)
        4. Education match (percentage and details)
        5. Keywords match (percentage, matched keywords, and missing keywords)
        6. Improvement suggestions
        
        Format your response as a JSON object with the following structure:
        {{
            "overall_score": <percentage>,
            "skills_score": <percentage>,
            "skills_details": {{
                "matched": [<list of matched skills>],
                "missing": [<list of missing skills>]
            }},
            "experience_score": <percentage>,
            "experience_details": [<list of experience match details>],
            "education_score": <percentage>,
            "education_details": [<list of education match details>],
            "keywords_score": <percentage>,
            "keywords_details": {{
                "matched": [<list of matched keywords>],
                "missing": [<list of missing keywords>]
            }},
            "suggestions": [<list of improvement suggestions>]
        }}
        
        Ensure all scores are integers between 0 and 100.
        """
        
        return prompt
    
    def _call_gemini_api(self, prompt):
        """
        Call Gemini API with the prepared prompt.
        
        Args:
            prompt (str): Prepared prompt
            
        Returns:
            dict: API response
        """
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(
            self.api_url,
            headers=headers,
            data=json.dumps(data)
        )
        
        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.status_code} - {response.text}")
        
        return response.json()
    
    def _parse_response(self, response):
        """
        Parse and format Gemini API response.
        
        Args:
            response (dict): API response
            
        Returns:
            dict: Formatted analysis results
        """
        try:
            # Extract text from response
            response_text = response["candidates"][0]["content"]["parts"][0]["text"]
            
            # Find JSON in response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in Gemini response")
            
            json_str = response_text[json_start:json_end]
            
            # Parse JSON
            results = json.loads(json_str)
            
            # Ensure all required fields are present
            required_fields = [
                "overall_score", "skills_score", "skills_details",
                "experience_score", "experience_details", "education_score",
                "education_details", "keywords_score", "keywords_details", "suggestions"
            ]
            
            for field in required_fields:
                if field not in results:
                    results[field] = 0 if "score" in field else [] if field == "suggestions" or "details" in field else {}
            
            return results
            
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {str(e)}", exc_info=True)
            
            # Return fallback results
            return {
                "overall_score": 0,
                "skills_score": 0,
                "skills_details": {"matched": [], "missing": []},
                "experience_score": 0,
                "experience_details": ["Error analyzing experience"],
                "education_score": 0,
                "education_details": ["Error analyzing education"],
                "keywords_score": 0,
                "keywords_details": {"matched": [], "missing": []},
                "suggestions": ["Error generating suggestions"]
            }
