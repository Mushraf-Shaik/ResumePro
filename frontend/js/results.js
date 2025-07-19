document.addEventListener('DOMContentLoaded', function() {
    // Get analysis results from localStorage
    const analysisResults = JSON.parse(localStorage.getItem('analysisResults') || '{}');
    
    // If no results, redirect to upload page
    if (!analysisResults || Object.keys(analysisResults).length === 0) {
        console.warn('No analysis results found, redirecting to upload page');
        window.location.href = 'upload.html';
        return;
    }
    
    console.log('Analysis Results:', analysisResults);
    
    // Display overall score with animation
    displayOverallScore(analysisResults);
    
    // Display ATS compatibility score
    displayATSScore(analysisResults);
    
    // Display keyword matching score
    displayKeywordScore(analysisResults);
    
    // Display skills analysis
    displaySkillsAnalysis(analysisResults);
    
    // Display keywords analysis
    displayKeywordsAnalysis(analysisResults);
    
    // Display experience match
    displayExperienceMatch(analysisResults);
    
    // Display education match
    displayEducationMatch(analysisResults);
    
    // Display improvement suggestions
    displaySuggestions(analysisResults);
});

// Function to display overall score with circular progress animation
function displayOverallScore(results) {
    const overallScore = results.overall_score || 0;
    const scoreElement = document.getElementById('overall-score');
    const circleElement = document.getElementById('score-circle');
    const interpretationElement = document.getElementById('score-interpretation');
    
    if (scoreElement) {
        // Animate score counting up
        animateScore(scoreElement, 0, overallScore, 1500);
        
        // Animate circular progress
        if (circleElement) {
            const circumference = 2 * Math.PI * 40; // radius = 40
            const offset = circumference - (overallScore / 100) * circumference;
            
            setTimeout(() => {
                circleElement.style.strokeDashoffset = offset;
            }, 500);
        }
        
        // Update interpretation
        if (interpretationElement) {
            let interpretation = '';
            let className = '';
            
            if (overallScore >= 85) {
                interpretation = 'Excellent match! Your resume is perfectly aligned with this job.';
                className = 'score-excellent';
            } else if (overallScore >= 70) {
                interpretation = 'Great match! Your resume shows strong alignment with the requirements.';
                className = 'score-good';
            } else if (overallScore >= 55) {
                interpretation = 'Good match. Some improvements could make your resume even stronger.';
                className = 'score-fair';
            } else {
                interpretation = 'Your resume needs significant improvements to match this job.';
                className = 'score-poor';
            }
            
            setTimeout(() => {
                interpretationElement.innerHTML = `
                    <p class="text-lg font-semibold ${className} mb-2">${interpretation}</p>
                    <p class="text-gray-600">Based on comprehensive ATS analysis and job matching.</p>
                `;
            }, 1000);
        }
    }
}

// Function to display ATS compatibility score
function displayATSScore(results) {
    const atsScore = results.ats_score || results.parsing_score || 75; // Default fallback
    const scoreElement = document.getElementById('ats-score');
    const progressElement = document.getElementById('ats-progress');
    const detailsElement = document.getElementById('ats-details');
    
    if (scoreElement) {
        animateScore(scoreElement, 0, atsScore, 1000, '/100');
    }
    
    if (progressElement) {
        setTimeout(() => {
            progressElement.style.width = `${atsScore}%`;
        }, 300);
    }
    
    if (detailsElement) {
        let details = '';
        if (atsScore >= 80) {
            details = 'Excellent! Your resume is highly compatible with ATS systems.';
        } else if (atsScore >= 60) {
            details = 'Good ATS compatibility. Minor formatting improvements recommended.';
        } else {
            details = 'ATS compatibility needs improvement. Consider simplifying formatting.';
        }
        
        setTimeout(() => {
            detailsElement.innerHTML = `<p>${details}</p>`;
        }, 800);
    }
}

// Function to display keyword matching score
function displayKeywordScore(results) {
    const keywordScore = results.keyword_score || results.skills_score || 65; // Default fallback
    const scoreElement = document.getElementById('keyword-score');
    const progressElement = document.getElementById('keyword-progress');
    const detailsElement = document.getElementById('keyword-details');
    
    if (scoreElement) {
        animateScore(scoreElement, 0, keywordScore, 1200, '/100');
    }
    
    if (progressElement) {
        setTimeout(() => {
            progressElement.style.width = `${keywordScore}%`;
        }, 400);
    }
    
    if (detailsElement) {
        let details = '';
        if (keywordScore >= 80) {
            details = 'Excellent keyword alignment with job requirements.';
        } else if (keywordScore >= 60) {
            details = 'Good keyword match. Consider adding more relevant terms.';
        } else {
            details = 'Low keyword match. Add more job-specific keywords to your resume.';
        }
        
        setTimeout(() => {
            detailsElement.innerHTML = `<p>${details}</p>`;
        }, 900);
    }
}

// Function to display skills analysis
function displaySkillsAnalysis(results) {
    const matchedSkillsElement = document.getElementById('matched-skills');
    const missingSkillsElement = document.getElementById('missing-skills');
    
    // Handle matched skills
    if (matchedSkillsElement) {
        let matchedSkills = [];
        
        if (results.skills_details && results.skills_details.matched) {
            matchedSkills = results.skills_details.matched;
        } else if (results.skills && results.skills.matched) {
            matchedSkills = results.skills.matched;
        } else {
            // Default matched skills for demo
            matchedSkills = ['JavaScript', 'Python', 'React', 'Node.js', 'SQL'];
        }
        
        setTimeout(() => {
            if (matchedSkills.length > 0) {
                matchedSkillsElement.innerHTML = matchedSkills.map(skill => 
                    `<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">${skill}</span>`
                ).join('');
            } else {
                matchedSkillsElement.innerHTML = '<span class="text-gray-500">No matched skills found</span>';
            }
        }, 600);
    }
    
    // Handle missing skills
    if (missingSkillsElement) {
        let missingSkills = [];
        
        if (results.skills_details && results.skills_details.missing) {
            missingSkills = results.skills_details.missing;
        } else if (results.skills && results.skills.missing) {
            missingSkills = results.skills.missing;
        } else {
            // Default missing skills for demo
            missingSkills = ['Docker', 'Kubernetes', 'AWS', 'MongoDB'];
        }
        
        setTimeout(() => {
            if (missingSkills.length > 0) {
                missingSkillsElement.innerHTML = missingSkills.map(skill => 
                    `<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800">${skill}</span>`
                ).join('');
            } else {
                missingSkillsElement.innerHTML = '<span class="text-gray-500">No missing skills identified</span>';
            }
        }, 700);
    }
}

// Function to display keywords analysis
function displayKeywordsAnalysis(results) {
    const matchedKeywordsElement = document.getElementById('matched-keywords');
    const missingKeywordsElement = document.getElementById('missing-keywords');
    
    // Handle matched keywords
    if (matchedKeywordsElement) {
        let matchedKeywords = [];
        
        if (results.keywords_details && results.keywords_details.matched) {
            matchedKeywords = results.keywords_details.matched;
        } else if (results.keywords && results.keywords.matched) {
            matchedKeywords = results.keywords.matched;
        } else if (results.matched_keywords) {
            matchedKeywords = results.matched_keywords;
        } else {
            // Default matched keywords for demo
            matchedKeywords = ['JavaScript', 'Python', 'React', 'Node.js', 'SQL', 'Git', 'Agile', 'API', 'Database', 'Frontend'];
        }
        
        setTimeout(() => {
            if (matchedKeywords.length > 0) {
                matchedKeywordsElement.innerHTML = matchedKeywords.map(keyword => 
                    `<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">${keyword}</span>`
                ).join('');
            } else {
                matchedKeywordsElement.innerHTML = '<span class="text-gray-500">No matched keywords found</span>';
            }
        }, 800);
    }
    
    // Handle missing keywords
    if (missingKeywordsElement) {
        let missingKeywords = [];
        
        if (results.keywords_details && results.keywords_details.missing) {
            missingKeywords = results.keywords_details.missing;
        } else if (results.keywords && results.keywords.missing) {
            missingKeywords = results.keywords.missing;
        } else if (results.missing_keywords) {
            missingKeywords = results.missing_keywords;
        } else {
            // Default missing keywords for demo
            missingKeywords = ['Docker', 'Kubernetes', 'AWS', 'MongoDB', 'TypeScript', 'GraphQL', 'Redis', 'Microservices'];
        }
        
        setTimeout(() => {
            if (missingKeywords.length > 0) {
                missingKeywordsElement.innerHTML = missingKeywords.map(keyword => 
                    `<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800">${keyword}</span>`
                ).join('');
                
                // Store missing keywords globally for copy function
                window.missingKeywordsList = missingKeywords;
            } else {
                missingKeywordsElement.innerHTML = '<span class="text-gray-500">No missing keywords identified</span>';
                window.missingKeywordsList = [];
            }
        }, 900);
    }
}

// Function to copy missing keywords to clipboard
function copyMissingKeywords() {
    if (!window.missingKeywordsList || window.missingKeywordsList.length === 0) {
        return;
    }
    
    const keywordsText = window.missingKeywordsList.join(', ');
    
    // Try to use the modern clipboard API
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(keywordsText).then(() => {
            showCopySuccess();
        }).catch(() => {
            // Fallback to older method
            fallbackCopyToClipboard(keywordsText);
        });
    } else {
        // Fallback for older browsers or non-secure contexts
        fallbackCopyToClipboard(keywordsText);
    }
}

// Fallback copy method for older browsers
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopySuccess();
    } catch (err) {
        console.error('Failed to copy keywords:', err);
    }
    
    document.body.removeChild(textArea);
}

// Show copy success message
function showCopySuccess() {
    const successElement = document.getElementById('copy-success');
    if (successElement) {
        successElement.classList.remove('hidden');
        setTimeout(() => {
            successElement.classList.add('hidden');
        }, 3000);
    }
}

// Function to display experience match
function displayExperienceMatch(results) {
    const experienceScore = results.experience_score || (results.experience && results.experience.score) || 70;
    const scoreElement = document.getElementById('experience-score');
    const progressElement = document.getElementById('experience-progress');
    const detailsElement = document.getElementById('experience-details');
    
    if (scoreElement) {
        animateScore(scoreElement, 0, experienceScore, 1300, '/100');
    }
    
    if (progressElement) {
        setTimeout(() => {
            progressElement.style.width = `${experienceScore}%`;
        }, 500);
    }
    
    if (detailsElement) {
        let details = results.experience_details || (results.experience && results.experience.details) || 
            'Your experience shows good alignment with the job requirements.';
        
        setTimeout(() => {
            detailsElement.innerHTML = `<p>${details}</p>`;
        }, 1000);
    }
}

// Function to display education match
function displayEducationMatch(results) {
    const educationScore = results.education_score || (results.education && results.education.score) || 80;
    const scoreElement = document.getElementById('education-score');
    const progressElement = document.getElementById('education-progress');
    const detailsElement = document.getElementById('education-details');
    
    if (scoreElement) {
        animateScore(scoreElement, 0, educationScore, 1400, '/100');
    }
    
    if (progressElement) {
        setTimeout(() => {
            progressElement.style.width = `${educationScore}%`;
        }, 600);
    }
    
    if (detailsElement) {
        let details = results.education_details || (results.education && results.education.details) || 
            'Your educational background aligns well with the job requirements.';
        
        setTimeout(() => {
            detailsElement.innerHTML = `<p>${details}</p>`;
        }, 1100);
    }
}

// Function to display improvement suggestions
function displaySuggestions(results) {
    const suggestionsElement = document.getElementById('suggestions-list');
    
    if (suggestionsElement) {
        let suggestions = [];
        
        if (results.suggestions && Array.isArray(results.suggestions)) {
            suggestions = results.suggestions;
        } else if (results.improvement_suggestions) {
            suggestions = results.improvement_suggestions;
        } else {
            // Default suggestions
            suggestions = [
                'Add more quantifiable achievements with specific metrics',
                'Include relevant keywords from the job description',
                'Highlight experience with required technologies',
                'Improve resume formatting for better ATS compatibility'
            ];
        }
        
        setTimeout(() => {
            if (suggestions.length > 0) {
                suggestionsElement.innerHTML = suggestions.map(suggestion => `
                    <div class="flex items-start space-x-3">
                        <div class="w-6 h-6 bg-yellow-100 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                            <svg class="w-4 h-4 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <p class="text-gray-600">${suggestion}</p>
                    </div>
                `).join('');
            } else {
                suggestionsElement.innerHTML = '<p class="text-gray-500">No specific suggestions available.</p>';
            }
        }, 1200);
    }
}

// Helper function to animate score counting
function animateScore(element, start, end, duration, suffix) {
    if (!suffix) suffix = '';
    const startTime = performance.now();
    
    function updateScore(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const currentScore = Math.round(start + (end - start) * easeOutQuart);
        
        element.textContent = currentScore + suffix;
        
        if (progress < 1) {
            requestAnimationFrame(updateScore);
        }
    }
    
    requestAnimationFrame(updateScore);
}
