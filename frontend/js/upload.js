document.addEventListener('DOMContentLoaded', function() {
    console.log('Upload script loaded');
    
    // Elements
    const dropArea = document.getElementById('drop-area');
    const browseText = document.getElementById('browse-text');
    const pasteTextBtn = document.getElementById('paste-text-btn');
    const jobDescTextarea = document.getElementById('job-description');
    const analyzeBtn = document.getElementById('analyze-resume-btn');
    const uploadStatus = document.getElementById('upload-status');
    const uploadMessage = document.getElementById('upload-message');
    const loadingModal = document.getElementById('loading-modal');
    
    // Debug element detection
    console.log('Drop area:', dropArea);
    console.log('Browse text:', browseText);
    console.log('Paste text button:', pasteTextBtn);
    console.log('Job description textarea:', jobDescTextarea);
    console.log('Analyze button:', analyzeBtn);
    
    // Check if all required elements are found
    if (!dropArea) console.error('Drop area not found');
    if (!browseText) console.error('Browse text element not found');
    if (!pasteTextBtn) console.error('Paste text button not found');
    if (!jobDescTextarea) console.error('Job description textarea not found');
    if (!analyzeBtn) console.error('Analyze button not found');
    
    let resumeText = '';
    let resumeFile = null;
    let isTextMode = false;
    
    // Hidden file input for browse functionality
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.pdf,.doc,.docx,.txt';
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);
    
    // Event listeners for drag and drop
    if (dropArea) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, unhighlight, false);
        });
        
        // Handle file drop
        dropArea.addEventListener('drop', handleDrop, false);
    }
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight() {
        dropArea.classList.add('border-blue-500');
    }
    
    function unhighlight() {
        dropArea.classList.remove('border-blue-500');
    }
    
    function handleDrop(e) {
        console.log('File dropped');
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length) {
            handleFiles(files);
        }
    }
    
    // Handle file selection
    fileInput.addEventListener('change', function() {
        console.log('File selected via input');
        if (this.files.length) {
            handleFiles(this.files);
        }
    });
    
    // Click on browse text to trigger file input
    if (browseText) {
        browseText.addEventListener('click', function() {
            console.log('Browse text clicked');
            fileInput.click();
        });
    }
    
    // Handle the selected files
    function handleFiles(files) {
        resumeFile = files[0];
        isTextMode = false;
        console.log('File handled:', resumeFile.name);
        updateDropAreaUI(`File selected: ${resumeFile.name}`);
    }
    
    // Paste text button functionality
    if (pasteTextBtn) {
        pasteTextBtn.addEventListener('click', function() {
            console.log('Paste text button clicked');
            isTextMode = true;
            resumeFile = null;
            
            // Create textarea for resume text
            const textareaContainer = document.createElement('div');
            textareaContainer.className = 'flex flex-col w-full';
            
            const textarea = document.createElement('textarea');
            textarea.placeholder = 'Paste your resume text here';
            textarea.className = 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111418] focus:outline-0 focus:ring-0 border border-[#dbe0e6] bg-white focus:border-[#dbe0e6] min-h-36 placeholder:text-[#60758a] p-[15px] text-base font-normal leading-normal';
            
            textareaContainer.appendChild(textarea);
            
            // Replace drop area content
            if (dropArea) {
                dropArea.innerHTML = '';
                dropArea.appendChild(textareaContainer);
            }
            
            // Update resume text when textarea changes
            textarea.addEventListener('input', function() {
                resumeText = this.value;
                console.log('Resume text updated:', resumeText.substring(0, 50) + '...');
            });
        });
    }
    
    // Update the UI of the drop area
    function updateDropAreaUI(message) {
        console.log('Updating drop area UI with message:', message);
        
        // Show upload status
        if (uploadStatus && uploadMessage) {
            uploadMessage.textContent = message;
            uploadStatus.classList.remove('hidden');
        }
        
        // Enable analyze button if file is uploaded
        if (analyzeBtn && (resumeFile || resumeText)) {
            analyzeBtn.disabled = false;
            analyzeBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    }
    
    // Analyze button functionality
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', function() {
            console.log('Analyze button clicked');
            
            const jobDescription = jobDescTextarea ? jobDescTextarea.value : '';
            
            if (!resumeFile && !resumeText) {
                alert('Please upload a resume file or paste resume text first.');
                return;
            }
            
            console.log('Preparing form data');
            console.log('Is text mode:', isTextMode);
            console.log('Resume file:', resumeFile ? resumeFile.name : 'none');
            console.log('Resume text length:', resumeText ? resumeText.length : 0);
            console.log('Job description length:', jobDescription ? jobDescription.length : 0);
            
            // Create FormData object
            const formData = new FormData();
            
            if (isTextMode) {
                formData.append('resume_text', resumeText);
            } else if (resumeFile) {
                formData.append('file', resumeFile);
            } else {
                alert('No resume content available');
                return;
            }
            
            if (jobDescription) {
                formData.append('job_description', jobDescription);
            }
            
            // Show loading modal
            if (loadingModal) {
                loadingModal.classList.remove('hidden');
            }
            
            // Show loading state on button
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = `
                <svg class="animate-spin w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Analyzing...</span>
            `;
            
            console.log('Sending form data to server');
            
            // Send to server
            fetch('/api/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                console.log('Upload response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Upload response data:', data);
                
                if (data.success) {
                    console.log('Upload successful, sending to analyze endpoint');
                    // Now analyze the resume
                    return fetch('/api/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            resume_text: data.resume_text,
                            job_description: data.job_description || '',
                            use_gemini: true
                        })
                    });
                } else {
                    throw new Error(data.error || 'Upload failed');
                }
            })
            .then(response => {
                console.log('Analysis response status:', response.status);
                return response.json();
            })
            .then(analysisData => {
                // Redirect to results page or display results
                console.log('Analysis results:', analysisData);
                
                // Store results in localStorage for the results page
                localStorage.setItem('analysisResults', JSON.stringify(analysisData));
                
                // Redirect to results page
                window.location.href = '/results.html';
            })
            .catch(error => {
                console.error('Error:', error);
                
                // Hide loading modal
                if (loadingModal) {
                    loadingModal.classList.add('hidden');
                }
                
                alert('An error occurred: ' + error.message);
            })
            .finally(() => {
                // Reset button state
                analyzeBtn.disabled = false;
                analyzeBtn.innerHTML = `
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                    </svg>
                    <span>Analyze Resume</span>
                `;
            });
        });
    }
});
